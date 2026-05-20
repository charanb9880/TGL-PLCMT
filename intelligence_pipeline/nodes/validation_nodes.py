from state.state import GraphState
from tools.validation_tool import run_validation_suite

def validate_branch(record: dict, branch_name: str) -> list:
    print(f"🛡️  [VAL NODE] {branch_name} validating...")
    if not record or "_error" in record:
        return []
    
    val = run_validation_suite(record)
    if not val["errors"]:
        return [record]
    return []

def openai_validate_node(state: GraphState) -> GraphState:
    # Find the OpenAI output in llm_outputs
    outputs = [o for o in state.get("llm_outputs", []) if o.get("_llm_source") == "OpenAI"]
    record = outputs[-1] if outputs else {}
    return {"validated_outputs": validate_branch(record, "OpenAI")}

def gemini_validate_node(state: GraphState) -> GraphState:
    outputs = [o for o in state.get("llm_outputs", []) if o.get("_llm_source") == "Gemini"]
    record = outputs[-1] if outputs else {}
    return {"validated_outputs": validate_branch(record, "Gemini")}

def router_validate_node(state: GraphState) -> GraphState:
    outputs = [o for o in state.get("llm_outputs", []) if o.get("_llm_source") == "OpenRouter"]
    record = outputs[-1] if outputs else {}
    return {"validated_outputs": validate_branch(record, "OpenRouter")}
