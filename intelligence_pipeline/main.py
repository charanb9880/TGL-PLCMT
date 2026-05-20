import sys
import os
import argparse
import asyncio

# Ensure local imports work correctly
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from graph import build_graph

async def run_pipeline(company_name: str, debug: bool = False):
    print(f"\n🚀 STARTING INTELLIGENCE PIPELINE FOR: {company_name}")
    print("=" * 60)
    
    app = build_graph()
    
    initial_state = {
        "company_name": company_name,
        "llm_outputs": [],
        "validated_outputs": [],
        "golden_record": {},
        "errors": [],
        "retry_count": 0,
        "failed_fields": [],
        "search_context": ""
    }
    
    # Execute the graph asynchronously
    async for output in app.astream(initial_state, {"recursion_limit": 15}):
        for key, value in output.items():
            if debug:
                print(f"\n--- STATE UPDATE FROM [{key}] ---")
                if "_gen" in key:
                    print(f"Generation from {key} complete.")
                elif "_val" in key:
                    print(f"Validation for {key} complete.")
                elif key == "consolidate":
                    print(f"Golden Record has {len(value.get('golden_record', {}))} fields.")
                print("-" * 30)
                
    print("=" * 60)
    print("🏁 PIPELINE EXECUTION COMPLETE.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Company Intelligence Pipeline")
    parser.add_argument("company", type=str, help="Name of the company to research")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging stream")
    
    args = parser.parse_args()
    
    # Handle async execution properly
    asyncio.run(run_pipeline(args.company, args.debug))
