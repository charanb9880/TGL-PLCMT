import asyncio
import json
import re
from state.state import GraphState
from models.llm_clients import get_openai_client, get_gemini_client, get_openrouter_client
from langchain_core.prompts import ChatPromptTemplate
from schema import CompanyIntelligenceSchema

ALL_FIELDS = [field.alias for field in CompanyIntelligenceSchema.model_fields.values()]

# Ultra-granular chunking (8 chunks) to fit low token limits
CHUNKS = [
    {"name": "Core Info", "start": 1, "end": 20},
    {"name": "Business Ops", "start": 21, "end": 40},
    {"name": "HR & Culture", "start": 41, "end": 60},
    {"name": "Leadership", "start": 61, "end": 80},
    {"name": "Financials A", "start": 81, "end": 100},
    {"name": "Financials B", "start": 101, "end": 120},
    {"name": "Tech Stack", "start": 121, "end": 140},
    {"name": "Future & AI", "start": 141, "end": 163}
]

async def run_model_research(state: GraphState, client, model_name: str, chunk_slice: list) -> dict:
    context = state.get("search_context", "")
    company = state["company_name"]
    
    print(f"🤖 [GEN NODE] {model_name} processing {len(chunk_slice)} chunks...")
    
    final_record = {field: "Data Not Found" for field in ALL_FIELDS}
    
    async def process_chunk(chunk):
        chunk_fields = ALL_FIELDS[chunk['start']-1 : chunk['end']]
        prompt = ChatPromptTemplate.from_messages([
            ("system", """JSON Specialist for {company}.
Rules:
1. Primary: Use SEARCH CONTEXT.
2. Secondary: Use internal knowledge if context is sparse.
3. Tertiary: Infer logically (e.g. industry-based estimates).
4. Output: ONLY valid JSON. No prose. No 'Data Not Found' unless unknowable."""),
            ("user", "CONTEXT:\n{context}\n\nFIELDS: {fields}")
        ])
        try:
            chain = prompt | client
            res = await chain.ainvoke({"context": context, "company": company, "fields": ", ".join(chunk_fields)})
            content = res.content if hasattr(res, 'content') else str(res)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                return data
        except:
            return {}
        return {}

    # Run ONLY the assigned chunks for this model
    results = await asyncio.gather(*(process_chunk(c) for c in chunk_slice))
    
    for res in results:
        for k, v in res.items():
            if k in final_record and v and v != "Data Not Found":
                final_record[k] = v
                
    final_record["_llm_source"] = model_name
    return {"llm_outputs": [final_record]}

async def openai_research_node(state: GraphState) -> GraphState:
    # Groq handles Chunks 1-3
    return await run_model_research(state, get_openai_client(), "Groq", CHUNKS[0:3])

async def gemini_research_node(state: GraphState) -> GraphState:
    # Gemini handles Chunks 4-6
    return await run_model_research(state, get_gemini_client(), "Gemini", CHUNKS[3:6])

async def router_research_node(state: GraphState) -> GraphState:
    # Cerebras handles Chunks 7-8
    return await run_model_research(state, get_openrouter_client(), "Cerebras", CHUNKS[6:8])
