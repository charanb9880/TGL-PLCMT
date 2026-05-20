from state.state import GraphState
from agents.consolidation_agent import consolidate_records

def consolidation_node(state: GraphState) -> GraphState:
    print("🤝  [CONSOLIDATION NODE] Merging data into Golden Record...")
    validated = state.get("validated_outputs", [])
    
    golden = consolidate_records(validated)
    print(f"   ↳ Merged {len(golden.keys())} fields into Golden Record.")
    
    # Prune state: Clear raw outputs to save memory/token context in state
    return {
        "golden_record": golden,
        "llm_outputs": [],
        "validated_outputs": []
    }
