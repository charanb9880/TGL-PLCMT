import asyncio
from state.state import GraphState
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

async def prepare_research_node(state: GraphState) -> GraphState:
    company_name = state["company_name"]
    print(f"🕵️  [INPUT NODE] Gathering deep intelligence for: {company_name}")
    
    search_tool = DuckDuckGoSearchRun()
    queries = [
        f"{company_name} official website, headquarters, and mission",
        f"{company_name} latest annual report revenue profit EBITDA financials",
        f"{company_name} total employee count, leadership, board of directors",
        f"{company_name} tech stack, engineering blog, AI ML adoption",
        f"{company_name} employee benefits, leave policy, work culture, Glassdoor reviews",
        f"{company_name} recent news, acquisitions, and market position"
    ]
    
    try:
        # Run more searches in parallel
        search_results = await asyncio.gather(*(asyncio.to_thread(search_tool.invoke, q) for q in queries))
        # Sweet spot: 8,000 chars for high efficiency and low token cost
        context = "\n\n".join(search_results)[:8000]
    except Exception as e:
        print(f"   ⚠️ Search Warning: {str(e)[:50]}")
        context = f"Company: {company_name}"
        
    return {"search_context": context}
