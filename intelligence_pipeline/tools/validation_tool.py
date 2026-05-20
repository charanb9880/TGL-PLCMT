import json
import importlib
import os
import sys

# Ensure validation suite (from pytests) is reachable
WORKSPACE_DIR = "/Users/charanb/Desktop/TGL_Customised/final_ui"
if WORKSPACE_DIR not in sys.path:
    sys.path.append(WORKSPACE_DIR)

def run_validation_suite(record: dict) -> dict:
    """Wraps the deterministic python validation rules (NOT LLM)"""
    errors = []
    warnings = []
    
    rules_path = os.path.join(WORKSPACE_DIR, "pytests", "rules", "rules.json")
    if not os.path.exists(rules_path):
        # Fallback if rules.json is missing
        if not record.get("Company Name"):
            errors.append("Company Name is missing")
        return {"errors": errors, "warnings": warnings}
        
    try:
        with open(rules_path, "r") as f:
            rules_config = json.load(f)
            
        for rule_id, config in rules_config.items():
            module_path = "pytests." + config["module"]
            try:
                module = importlib.import_module(module_path)
                for func_name in config["functions"]:
                    func = getattr(module, func_name, None)
                    if func:
                        errs, warns = func(record)
                        errors.extend([f"Rule {rule_id}: {e}" for e in errs])
                        warnings.extend([f"Rule {rule_id}: {w}" for w in warns])
            except Exception as e:
                pass
    except Exception as e:
        errors.append(f"Validation engine error: {str(e)}")
        
    return {"errors": errors, "warnings": warnings}
