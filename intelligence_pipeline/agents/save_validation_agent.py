from tools.validation_tool import run_validation_suite
from tools.supabase_tool import save_to_supabase

def validate_and_save(record: dict) -> dict:
    """Runs deterministic validation and saves if passed."""
    val_result = run_validation_suite(record)
    
    if not val_result["errors"]:
        success = save_to_supabase(record)
        return {"status": "SUCCESS", "errors": [], "warnings": val_result["warnings"], "saved": success}
    else:
        return {"status": "FAIL", "errors": val_result["errors"], "warnings": val_result["warnings"], "saved": False}
