import os
import json
from state.state import GraphState
from tools.supabase_tool import save_to_supabase

def save_node(state: GraphState) -> GraphState:
    print("💾  [SAVE NODE] Persisting to DB and Local Storage...")
    golden = state.get("golden_record", {})
    company_name = state.get("company_name", "unknown_company")
    
    # 1. Save to Supabase
    save_to_supabase(golden)
    
    # 2. Save Locally as JSON
    output_dir = "research_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{company_name.replace(' ', '_').lower()}_intelligence.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w") as f:
        json.dump(golden, f, indent=4)
        
    print(f"   ↳ ✅ Local copy saved to: {filepath}")
    
    return state
