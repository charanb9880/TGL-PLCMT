from state.state import GraphState
from agents.research_agent import generate_company_data
import asyncio

def research_node(state: GraphState) -> GraphState:
    print(f"🕵️  [RESEARCH NODE] Fetching data for: {state['company_name']} (Retry: {state.get('retry_count', 0)})")
    company_name = state["company_name"]
    failed_fields = state.get("failed_fields", [])
    
    outputs = asyncio.run(generate_company_data(company_name, failed_fields))
    print(f"   ↳ Gathered {len(outputs)} LLM outputs.")
    return {"llm_outputs": outputs}
