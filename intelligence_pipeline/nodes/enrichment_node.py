from state.state import GraphState
from models.llm_clients import get_openai_client
from langchain_core.prompts import ChatPromptTemplate
import json
import asyncio

def enrichment_node(state: GraphState) -> GraphState:
    return asyncio.run(_enrichment_logic(state))

async def _enrichment_logic(state: GraphState) -> GraphState:
    print("💎  [ENRICHMENT NODE] Enhancing research data...")
    llm_outputs = state.get("llm_outputs", [])
    company_name = state["company_name"]
    
    if not llm_outputs:
        return {}

    client = get_openai_client()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Enrichment Agent. Given partial company data, fill in missing logical fields like social handles, common email patterns, and tech stack based on industry trends."),
        ("user", "Company: {company_name}\nData: {data}\n\nReturn enriched JSON.")
    ])
    
    enriched_outputs = []
    for output in llm_outputs:
        try:
            chain = prompt | client
            res = await chain.ainvoke({"company_name": company_name, "data": json.dumps(output)})
            content = res.content if hasattr(res, 'content') else str(res)
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            enriched_data = json.loads(content)
            output.update(enriched_data)
            enriched_outputs.append(output)
        except:
            enriched_outputs.append(output)
            
    return {"llm_outputs": enriched_outputs}
