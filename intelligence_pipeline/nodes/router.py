from state.state import GraphState
from tools.validation_tool import run_validation_suite
from config.settings import MAX_RETRIES

from nodes.recovery_node import assert_no_nulls

def route_after_consolidation(state: GraphState) -> str:
    print("🚦  [ROUTER] Running Final Validation on Golden Record...")
    golden = state.get("golden_record", {})
    
    # 5. VALIDATION PATCH: Ensure no nulls in critical fields
    try:
        assert_no_nulls(golden)
    except ValueError as e:
        print(f"   ↳ ⚠️ Validation Patch FAILED: {str(e)}. Re-triggering NULLRecoveryNode.")
        # If we haven't reached max retries, we can try recovery again
        # But usually recovery_node should handle it. This is a safety loop.
        retries = state.get("retry_count", 0)
        if retries < MAX_RETRIES:
             return "recover" # This would create a loop, but LangGraph handles it if we add the edge
    
    val_result = run_validation_suite(golden)
    
    errors = val_result["errors"]
    
    if not errors:
        print("   ↳ ✅ Final Validation PASSED. Routing to SAVE.")
        return "save"
        
    retries = state.get("retry_count", 0)
    if retries >= MAX_RETRIES:
        print(f"   ↳ ❌ Final Validation FAILED. Max retries ({MAX_RETRIES}) reached. Routing to END.")
        return "end"
        
    print(f"   ↳ 🔄 Final Validation FAILED. Routing to REGENERATE (Attempt {retries + 1}).")
    return "regenerate"

def regeneration_node(state: GraphState) -> GraphState:
    print("♻️  [REGENERATION NODE] Extracting failed fields...")
    golden = state.get("golden_record", {})
    val_result = run_validation_suite(golden)
    
    errors = val_result["errors"]
    
    # Extract fields from errors if possible
    # E.g. "Rule 1: Company Name is missing" -> extract Company Name
    # For now, we pass the raw errors back to focus the LLM.
    failed_fields = [e for e in errors]
    
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "failed_fields": failed_fields,
        "errors": errors
    }
