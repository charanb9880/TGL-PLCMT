import sys
import os
import pandas as pd
import json
import asyncio

# Ensure local imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import build_graph
from state.state import GraphState

def load_from_excel(company_name):
    xl_path = "/Users/charanb/Desktop/TGL_Customised/TGl.xlsx"
    if not os.path.exists(xl_path):
        return None
    
    xl = pd.ExcelFile(xl_path)
    # Find sheet
    sheet_name = next((s for s in xl.sheet_names if company_name.lower() in s.lower() and 'Consolidated' in s), None)
    if not sheet_name:
        return None
        
    df = xl.parse(sheet_name)
    param_col = next((c for c in df.columns if 'Parameter' in str(c)), None)
    data_col = next((c for c in df.columns if 'Research Output' in str(c) or 'Data' in str(c)), None)
    
    if param_col and data_col:
        df = df.dropna(subset=[param_col])
        record = dict(zip(df[param_col].astype(str).str.strip(), df[data_col]))
        return record
    return None

async def run_verification(company_name: str):
    print(f"\n🔍 VERIFYING ACTUAL DATA FOR: {company_name}")
    print("=" * 60)
    
    record = load_from_excel(company_name)
    if not record:
        print(f"❌ Could not find data for {company_name} in Excel.")
        return

    app = build_graph()
    
    # We start with the actual data as if it was the LLM output
    initial_state = {
        "company_name": company_name,
        "llm_outputs": [record], # Inject actual data here
        "validated_outputs": [],
        "golden_record": {},
        "errors": [],
        "retry_count": 0,
        "failed_fields": []
    }
    
    # We want to skip 'research' and go to 'validate'
    # In LangGraph, we can't easily skip the entry point unless we modify the graph
    # or just let it run (it will do research, but we can ignore it)
    
    from nodes.validation_node import per_llm_validation_node
    from nodes.consolidation_node import consolidation_node
    from tools.validation_tool import run_validation_suite
    
    print("🛡️ Running Validation Engine on Actual Data...")
    val_results = run_validation_suite(record)
    
    if val_results["errors"]:
        print(f"\n❌ Found {len(val_results['errors'])} validation errors in Excel data:")
        for err in val_results["errors"]:
            print(f"  - {err}")
    else:
        print("\n✅ Excel data passed all validation rules!")

    if val_results["warnings"]:
        print(f"\n⚠️ Found {len(val_results['warnings'])} warnings:")
        for warn in val_results["warnings"]:
            print(f"  - {warn}")

    # Now run the rest of the flow
    val_state = per_llm_validation_node(initial_state)
    
    # Merge results into state
    current_state = initial_state.copy()
    current_state.update(val_state)
    
    final_state = consolidation_node(current_state)
    
    print("=" * 60)
    print("🏁 VERIFICATION COMPLETE.")
    
    golden = final_state.get("golden_record", {})
    print(f"\n✅ Validated Record for {company_name} has {len(golden)} fields.")
    
    if final_state.get("errors"):
        print("\n❌ Errors found:")
        for err in final_state["errors"]:
            print(f"  - {err}")
    else:
        print("\n✨ No major errors found in critical fields.")

if __name__ == "__main__":
    company = sys.argv[1] if len(sys.argv) > 1 else "Twitter"
    asyncio.run(run_verification(company))
