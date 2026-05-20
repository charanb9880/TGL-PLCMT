from fastapi import APIRouter, BackgroundTasks, HTTPException, Path
from typing import List

from app.models.api_models import GenerateRequest, GenerateResponse, RunStatusResponse
from app.storage.run_store import run_store
from app.service import workflow_service

router = APIRouter(prefix="/v1/agent", tags=["Agent"])

@router.post("/generate", response_model=RunStatusResponse, status_code=200)
async def generate_company_intelligence(
    request: GenerateRequest
):
    """
    Start a LangGraph intelligence pipeline for a specific company synchronously.
    Blocks until the 163 parameters are generated and returns them in the response.
    """
    try:
        # Create run state
        run_id = run_store.create_run(company_name=request.company_name)
        
        # Execute the pipeline synchronously (awaits completion)
        await workflow_service.execute_run(run_id=run_id, company_name=request.company_name)
        
        run_data = run_store.get_run(run_id)
        return RunStatusResponse(**run_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute run: {str(e)}")


@router.get("/status", response_model=List[RunStatusResponse])
async def list_all_runs():
    """
    Fetch all active and past runs.
    """
    runs = run_store.list_runs()
    return [RunStatusResponse(**run) for run in runs]


@router.get("/status/{run_id}", response_model=RunStatusResponse)
async def get_run_status(run_id: str = Path(..., description="The ID of the run")):
    """
    Fetch the execution status and output for a specific run.
    """
    run_data = run_store.get_run(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found.")
    
    return RunStatusResponse(**run_data)
