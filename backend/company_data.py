import math
import os
import re
import shutil
import zipfile
from collections import Counter
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

from database import engine, is_database_configured


ROOT_DIR = Path(__file__).parent
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
MAIN_SHEET = "companies"
_CACHE: dict[str, Any] = {}

FIXED_CATEGORY_LABELS = {
    "Tech Giants": ["tech giant", "enterprise", "platform", "cloud", "data"],
    "Product Companies": ["product", "saas", "platform", "fintech"],
    "Service Companies": ["service", "consulting", "outsourcing", "agency"],
    "Startups": ["startup", "unicorn", "scale-up", "scale up"],
}

FILTER_COLUMNS = [
    "Category",
    "Focus Sectors / Industries",
    "Employee Size",
    "Profitability Status",
    "Remote Work Policy",
    "Hiring Velocity",
]

SORT_COLUMN_MAP = {
    "name": "Company Name",
    "employee_size": "Employee Size",
    "yoy_growth_rate": "Year-over-Year Growth Rate",
    "brand_value": "Brand value",
}


def clear_cache() -> None:
    _CACHE.clear()


def locate_workbook() -> Path:
    env_path = os.environ.get("PLACEMENT_EXCEL_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    candidates = [
        Path("/app/tmp_assets/scale_ai_extract/scale ai .xlsx"),
        *sorted(UPLOAD_DIR.glob("*.xlsx")),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("No Excel workbook available for placement data")


def workbook_signature() -> str:
    workbook = locate_workbook()
    return f"{workbook}:{workbook.stat().st_mtime_ns}"


def serialize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if hasattr(value, "item"):
        value = value.item()
    return value


def infer_type(series: pd.Series) -> str:
    sample = series.dropna()
    if sample.empty:
        return "text"
    if pd.api.types.is_bool_dtype(sample):
        return "boolean"
    if pd.api.types.is_integer_dtype(sample):
        return "integer"
    if pd.api.types.is_float_dtype(sample):
        return "number"
    if pd.api.types.is_datetime64_any_dtype(sample):
        return "datetime"
    return "text"


def get_workbook_overview() -> dict[str, Any]:
    try:
        signature = workbook_signature()
        cached = _CACHE.get("overview")
        if cached and cached["signature"] == signature:
            return cached

        workbook = locate_workbook()
    except FileNotFoundError:
        return {
            "signature": "",
            "path": "",
            "sheet_names": [],
            "columns": [],
            "records": [],
        }
    excel_file = pd.ExcelFile(workbook)
    company_frame = pd.read_excel(workbook, sheet_name=MAIN_SHEET)
    company_frame = company_frame.where(pd.notnull(company_frame), None)

    overview = {
        "signature": signature,
        "path": str(workbook),
        "sheet_names": excel_file.sheet_names,
        "columns": [
            {"name": column, "type": infer_type(company_frame[column])}
            for column in company_frame.columns
        ],
        "records": [
            {column: serialize_value(row[column]) for column in company_frame.columns}
            for _, row in company_frame.iterrows()
        ],
    }
    _CACHE["overview"] = overview
    return overview


async def has_database_company_table() -> bool:
    if not is_database_configured() or engine is None:
        return False

    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT to_regclass('public.company') AS table_name"))
            row = result.mappings().first()
            return bool(row and row["table_name"])
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


async def get_records() -> list[dict[str, Any]]:
    if is_database_configured() and engine is not None and await has_database_company_table():
        try:
            async with engine.connect() as connection:
                result = await connection.execute(text('SELECT * FROM public.company ORDER BY "company_id" ASC'))
                records = []
                for row in result.mappings().all():
                    clean_row = {}
                    for k, v in dict(row).items():
                        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                            clean_row[k] = None
                        else:
                            clean_row[k] = v
                    records.append(clean_row)
                return records
        except Exception as e:
            print(f"Database query failed: {e}")
            pass

    try:
        return get_workbook_overview()["records"]
    except FileNotFoundError:
        return []


def dedupe_options(values: list[Any]) -> list[str]:
    options = []
    seen = set()
    for value in values:
        if value is None:
            continue
        for part in re.split(r"[;,]", str(value)):
            cleaned = part.strip()
            if cleaned and cleaned.lower() not in seen:
                seen.add(cleaned.lower())
                options.append(cleaned)
    return sorted(options)


def normalize_for_match(value: Any) -> str:
    return str(value or "").strip().lower()


def parse_sort_value(value: Any) -> tuple[int, Any]:
    if value in (None, ""):
        return (2, 0, "")
    if isinstance(value, (int, float)):
        return (0, float(value), "")

    text_value = str(value).strip().lower()
    match = re.search(r"-?\d[\d,.]*", text_value)
    if match:
        numeric_value = float(match.group(0).replace(",", ""))
        if "b" in text_value:
            numeric_value *= 1_000_000_000
        elif "m" in text_value:
            numeric_value *= 1_000_000
        elif "k" in text_value:
            numeric_value *= 1_000
        return (0, numeric_value, text_value)

    return (1, 0, text_value)


def filter_records(
    records: list[dict[str, Any]],
    search: str = "",
    category: str | None = None,
    focus_sector: str | None = None,
    employee_size: str | None = None,
    profitability_status: str | None = None,
    remote_work_policy: str | None = None,
    hiring_velocity: str | None = None,
    sort_by: str = "name",
) -> list[dict[str, Any]]:
    filtered = records

    if search:
        query = search.lower().strip()
        filtered = [
            record
            for record in filtered
            if query in " ".join(
                normalize_for_match(record.get(field))
                for field in [
                    "Company Name",
                    "Short Name",
                    "Category",
                    "Focus Sectors / Industries",
                    "Services / Offerings / Products",
                ]
            )
        ]

    for column, value in {
        "Category": category,
        "Focus Sectors / Industries": focus_sector,
        "Employee Size": employee_size,
        "Profitability Status": profitability_status,
        "Remote Work Policy": remote_work_policy,
        "Hiring Velocity": hiring_velocity,
    }.items():
        if value:
            needle = value.lower().strip()
            filtered = [
                record
                for record in filtered
                if needle in normalize_for_match(record.get(column))
            ]

    sort_column = SORT_COLUMN_MAP.get(sort_by, "Company Name")
    return sorted(filtered, key=lambda record: parse_sort_value(record.get(sort_column)))


def get_company_by_id(records: list[dict[str, Any]], company_id: str) -> dict[str, Any] | None:
    normalized = company_id.strip().lower()
    for record in records:
        values = [
            record.get("company_id"),
            record.get("Company Name"),
            record.get("Short Name"),
        ]
        if any(normalize_for_match(value) == normalized for value in values if value is not None):
            return record
    return None


def build_filter_options(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        column: dedupe_options([record.get(column) for record in records])
        for column in FILTER_COLUMNS
    }


def bucket_fixed_categories(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    category_counts = []
    for label, keywords in FIXED_CATEGORY_LABELS.items():
        count = 0
        for record in records:
            category_value = normalize_for_match(record.get("Category"))
            if any(keyword in category_value for keyword in keywords):
                count += 1
        category_counts.append({"label": label, "count": count})
    return category_counts


def summarise_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    category_counter = Counter(normalize_for_match(record.get("Category")) for record in records if record.get("Category"))
    hiring_counter = Counter(normalize_for_match(record.get("Hiring Velocity")) for record in records if record.get("Hiring Velocity"))
    profitability_counter = Counter(normalize_for_match(record.get("Profitability Status")) for record in records if record.get("Profitability Status"))
    work_mode_counter = Counter(normalize_for_match(record.get("Remote Work Policy")) for record in records if record.get("Remote Work Policy"))

    def to_chart(counter: Counter) -> list[dict[str, Any]]:
        return [
            {"label": key.title(), "value": value}
            for key, value in counter.most_common()
        ]

    return {
        "total_companies": len(records),
        "category_distribution": to_chart(category_counter),
        "hiring_velocity_distribution": to_chart(hiring_counter),
        "profitability_mix": to_chart(profitability_counter),
        "work_mode_distribution": to_chart(work_mode_counter),
        "category_tiles": bucket_fixed_categories(records),
    }


def comparison_highlights(company: dict[str, Any]) -> dict[str, list[str]]:
    strengths = []
    risks = []

    if "high" in normalize_for_match(company.get("Brand value")):
        strengths.append(f"Brand value: {company.get('Brand value')}")
    if "profit" in normalize_for_match(company.get("Profitability Status")):
        strengths.append(f"Profitability: {company.get('Profitability Status')}")
    if "high" in normalize_for_match(company.get("AI/ML Adoption Level")):
        strengths.append(f"Technology adoption: {company.get('AI/ML Adoption Level')}")
    if "strong" in normalize_for_match(company.get("Learning culture")):
        strengths.append(f"Learning culture: {company.get('Learning culture')}")

    if "high" in normalize_for_match(company.get("Burnout risk")):
        risks.append(f"Burnout risk: {company.get('Burnout risk')}")
    if "not profitable" in normalize_for_match(company.get("Profitability Status")):
        risks.append(f"Profitability risk: {company.get('Profitability Status')}")
    if "yes" in normalize_for_match(company.get("Customer Concentration Risk")):
        risks.append(f"Customer concentration risk: {company.get('Customer Concentration Risk')}")
    if company.get("Legal Issues / Controversies"):
        risks.append(f"Legal issues / controversies: {company.get('Legal Issues / Controversies')}")

    return {
        "strengths": strengths[:4],
        "weaknesses": risks[:2],
        "risks": risks[:4],
    }


def save_uploaded_workbook(filename: str, file_bytes: bytes) -> Path:
    clear_cache()
    target_dir = UPLOAD_DIR / datetime.now().strftime("%Y%m%d%H%M%S")
    target_dir.mkdir(parents=True, exist_ok=True)

    incoming_path = target_dir / filename
    incoming_path.write_bytes(file_bytes)

    if filename.lower().endswith(".zip"):
        with zipfile.ZipFile(incoming_path, "r") as archive:
            archive.extractall(target_dir)
        for extracted in target_dir.rglob("*.xlsx"):
            final_path = UPLOAD_DIR / extracted.name
            shutil.copy2(extracted, final_path)
            os.environ["PLACEMENT_EXCEL_PATH"] = str(final_path)
            return final_path
        raise FileNotFoundError("No .xlsx file found inside uploaded zip archive")

    final_path = UPLOAD_DIR / filename
    shutil.copy2(incoming_path, final_path)
    os.environ["PLACEMENT_EXCEL_PATH"] = str(final_path)
    return final_path