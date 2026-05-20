from fastapi import FastAPI, APIRouter, File, HTTPException, Query, UploadFile
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field

from company_data import (
    build_filter_options,
    clear_cache,
    comparison_highlights,
    filter_records,
    get_company_by_id,
    get_records,
    get_workbook_overview,
    has_database_company_table,
    locate_workbook,
    save_uploaded_workbook,
    summarise_records,
)
from database import engine, is_database_configured
from skill_engine import evaluate_skill_match


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Placement Intelligence API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


class SkillMatchRequest(BaseModel):
    company_id: str
    skills: list[str] | str = Field(default_factory=list)

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Placement Intelligence API online"}

@api_router.get("/dataset/status")
async def dataset_status():
    overview = get_workbook_overview()
    records = await get_records()
    return {
        "workbook_path": overview["path"],
        "available_sheets": overview["sheet_names"],
        "column_count": len(overview["columns"]),
        "row_count": len(records),
        "columns": overview["columns"],
        "database_configured": is_database_configured(),
        "database_table_ready": await has_database_company_table(),
    }

@api_router.get("/import/preview")
async def import_preview():
    overview = get_workbook_overview()
    return {
        "sheet_name": "Companies",
        "workbook_path": overview["path"],
        "sheet_names": overview["sheet_names"],
        "column_count": len(overview["columns"]),
        "columns": overview["columns"],
        "sample_record": overview["records"][0] if overview["records"] else None,
        "database_configured": is_database_configured(),
    }


@api_router.post("/import/upload")
async def import_upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    if not file.filename.lower().endswith((".xlsx", ".zip")):
        raise HTTPException(status_code=400, detail="Upload a .xlsx file or a .zip containing .xlsx")

    saved_path = save_uploaded_workbook(file.filename, await file.read())
    clear_cache()
    overview = get_workbook_overview()
    return {
        "message": "Workbook uploaded successfully",
        "saved_path": str(saved_path),
        "sheet_name": "Companies",
        "column_count": len(overview["columns"]),
        "row_count": len(overview["records"]),
    }


@api_router.get("/companies")
async def list_companies(
    search: str = "",
    category: str | None = None,
    focus_sector: str | None = Query(default=None, alias="focusSector"),
    employee_size: str | None = Query(default=None, alias="employeeSize"),
    profitability_status: str | None = Query(default=None, alias="profitabilityStatus"),
    remote_work_policy: str | None = Query(default=None, alias="remoteWorkPolicy"),
    hiring_velocity: str | None = Query(default=None, alias="hiringVelocity"),
    sort_by: str = Query(default="name", alias="sortBy"),
):
    records = await get_records()
    filtered_records = filter_records(
        records,
        search=search,
        category=category,
        focus_sector=focus_sector,
        employee_size=employee_size,
        profitability_status=profitability_status,
        remote_work_policy=remote_work_policy,
        hiring_velocity=hiring_velocity,
        sort_by=sort_by,
    )
    return {
        "items": filtered_records,
        "total": len(filtered_records),
        "filters": build_filter_options(records),
        "sort_options": [
            {"label": "Name", "value": "name"},
            {"label": "Employee Size", "value": "employee_size"},
            {"label": "Year-over-Year Growth Rate", "value": "yoy_growth_rate"},
            {"label": "Brand Value", "value": "brand_value"},
        ],
    }


import json
import re

class SaveCompanyRequest(BaseModel):
    golden_record: dict

@api_router.post("/companies/save_generated")
async def save_generated_company(req: SaveCompanyRequest):
    golden = req.golden_record
    
    # Clean keys
    cleaned_data = {}
    for k, v in golden.items():
        clean_k = k.lower().strip()
        clean_k = re.sub(r'[^a-z0-9]', '_', clean_k)
        clean_k = re.sub(r'_+', '_', clean_k)
        clean_k = clean_k.strip('_')
        
        if clean_k == "company_name":
            clean_k = "name"
            
        # Serialize lists/dicts
        if isinstance(v, (dict, list)):
            v = json.dumps(v)
            
        cleaned_data[clean_k] = v
        
    async with engine.begin() as conn:
        from sqlalchemy import text
        col_res = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"))
        valid_cols = [r[0] for r in col_res.fetchall()]
        
        insert_data = {}
        for col in valid_cols:
            if col not in ("company_id", "created_at", "updated_at"):
                val = cleaned_data.get(col, None)
                if val is not None and not isinstance(val, str):
                    val = str(val)
                insert_data[col] = val
                
        # Generate new company ID safely
        res = await conn.execute(text("SELECT MAX(company_id) FROM public.company"))
        max_id = res.scalar() or 0
        new_id = max_id + 1
        
        insert_data["company_id"] = new_id
        
        cols = ", ".join([f'"{k}"' for k in insert_data.keys()])
        params_str = ", ".join([f":{k}" for k in insert_data.keys()])
        
        insert_query = text(f'INSERT INTO public.company ({cols}) VALUES ({params_str})')
        await conn.execute(insert_query, insert_data)
        
    clear_cache()
    return {"status": "success", "company_id": new_id, "name": cleaned_data.get("name")}


@api_router.get("/companies/{company_id}")
async def get_company(company_id: str):
    records = await get_records()
    company = get_company_by_id(records, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"company": company, "highlights": comparison_highlights(company)}


@api_router.get("/categories")
async def categories_summary():
    records = await get_records()
    return {"categories": summarise_records(records)["category_tiles"]}


@api_router.get("/analytics")
async def analytics_summary():
    records = await get_records()
    return summarise_records(records)


@api_router.get("/compare")
async def compare_companies(left_company_id: str, right_company_id: str):
    records = await get_records()
    left_company = get_company_by_id(records, left_company_id)
    right_company = get_company_by_id(records, right_company_id)

    if not left_company or not right_company:
        raise HTTPException(status_code=404, detail="One or both companies were not found")

    return {
        "left_company": left_company,
        "right_company": right_company,
        "left_highlights": comparison_highlights(left_company),
        "right_highlights": comparison_highlights(right_company),
    }


@api_router.post("/skill-match")
async def skill_match(payload: SkillMatchRequest):
    records = await get_records()
    company = get_company_by_id(records, payload.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return {
        "company_id": payload.company_id,
        "company_name": company.get("Company Name"),
        "result": evaluate_skill_match(company, payload.skills),
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    if engine is not None:
        await engine.dispose()