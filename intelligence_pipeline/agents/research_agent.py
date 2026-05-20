from models.llm_clients import get_openai_client, get_gemini_client, get_openrouter_client
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
import asyncio

async def generate_company_data(company_name: str, failed_fields: list = None) -> list:
    """Runs parallel chunked research to fill all 163 parameters."""
    
    # Define the 4 chunks of the schema
    # (Grouping fields logically to help the LLM focus)
    chunks = [
        {"name": "General & Business", "start": 1, "end": 40},
        {"name": "Culture & HR", "start": 41, "end": 80},
        {"name": "Financials & Market", "start": 81, "end": 120},
        {"name": "Tech & Operations", "start": 121, "end": 167}
    ]
    
    search_tool = DuckDuckGoSearchRun()
    
    # 1. EXPANDED SEARCH CONTEXT
    search_queries = [
        f"{company_name} financials, revenue, and business overview",
        f"{company_name} employee benefits, leave policy, and culture",
        f"{company_name} tech stack, AI adoption, and product roadmap"
    ]
    
    print(f"   🔍 Gathering deep context for {company_name}...")
    try:
        search_results = await asyncio.gather(*(asyncio.to_thread(search_tool.invoke, q) for q in search_queries))
        combined_context = "\n\n".join(search_results)[:3000] # Truncate to fit limits
    except Exception as e:
        print(f"   ⚠️ Search Warning: {str(e)[:100]}. Proceeding with limited context.")
        combined_context = f"Company Name: {company_name}"

    clients = [
        get_openai_client(),
        get_gemini_client(),
        get_openrouter_client()
    ]

    # 2. RUN PARALLEL CHUNKED RESEARCH
    from schema import CompanyIntelligenceSchema
    all_fields = [field.alias for field in CompanyIntelligenceSchema.model_fields.values()]
    
    # Semaphore to prevent hitting rate/credit limits too hard
    sem = asyncio.Semaphore(2) 
    
    async def research_chunk(chunk, client_index):
        async with sem:
            client = clients[client_index % len(clients)]
            chunk_fields = all_fields[chunk['start']-1 : chunk['end']]
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "JSON researcher. Return ONLY JSON for requested fields."),
                ("user", "Context: {context}\n\nCompany: {company_name}\nFields: {fields}")
            ])
            
            try:
                chain = prompt | client
                res = await chain.ainvoke({
                    "context": combined_context,
                    "company_name": company_name,
                    "fields": ", ".join(chunk_fields)
                })
                content = res.content if hasattr(res, 'content') else str(res)
                
                # Extract JSON block
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)
                
                import json
                data = json.loads(content)
                print(f"     ✅ {chunk['name']} ok.")
                return data
            except Exception as e:
                print(f"   ❌ {chunk['name']} err: {str(e)[:50]}")
                return {"_error": str(e)}

    print(f"   🚀 Parallel Missions (4)...")
    tasks = [research_chunk(chunks[i], i) for i in range(len(chunks))]
    chunk_results = await asyncio.gather(*tasks)
    
    # Merge into Golden Record
    final_record = {field: "Data Not Found" for field in all_fields}
    for res in chunk_results:
        if res and "_error" not in res:
            for k, v in res.items():
                if k in final_record and v and v != "Data Not Found":
                    final_record[k] = v
            
    print(f"   ✅ Merged: {len([v for v in final_record.values() if v != 'Data Not Found'])} fields.")
    
    # Return as a list to satisfy the graph's expectation of multi-LLM outputs
    final_record["_llm_source"] = "Chunked_Engine"
    return [final_record]
