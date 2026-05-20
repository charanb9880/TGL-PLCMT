from state.state import GraphState
from tools.validation_tool import run_validation_suite

def per_llm_validation_node(state: GraphState) -> GraphState:
    print("🛡️  [VALIDATION NODE] Validating individual LLM outputs...")
    outputs = state.get("llm_outputs", [])
    
    validated = []
    for out in outputs:
        if "_error" in out:
            continue
        val = run_validation_suite(out)
        if not val["errors"]:
            validated.append(out)
            
    if not validated:
        print("   ↳ ⚠️ All LLMs failed strict validation. Passing best effort to consolidation.")
        validated = [out for out in outputs if "_error" not in out]
    else:
        print(f"   ↳ {len(validated)} outputs passed validation.")
        
    return {"validated_outputs": validated}
