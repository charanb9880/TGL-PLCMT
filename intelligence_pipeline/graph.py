from langgraph.graph import StateGraph, END
from state.state import GraphState, InputState

# Import new granular nodes
from nodes.input_node import prepare_research_node
from nodes.generation_nodes import openai_research_node, gemini_research_node, router_research_node
from nodes.validation_nodes import openai_validate_node, gemini_validate_node, router_validate_node
from nodes.consolidation_node import consolidation_node
from nodes.recovery_node import null_recovery_node
from nodes.router import route_after_consolidation, regeneration_node
from nodes.save_node import save_node

def build_graph():
    workflow = StateGraph(GraphState, input=InputState)
    
    # 1. INPUT STAGE
    workflow.add_node("entry", prepare_research_node)
    
    # 2. GENERATION STAGE (Parallel Branches)
    workflow.add_node("groq_generate", openai_research_node)
    workflow.add_node("mixtral_generate", gemini_research_node)
    workflow.add_node("cerebras_generate", router_research_node)
    
    # 3. VALIDATION STAGE (Parallel Branches)
    workflow.add_node("groq_validate", openai_validate_node)
    workflow.add_node("mixtral_validate", gemini_validate_node)
    workflow.add_node("cerebras_validate", router_validate_node)
    
    # 4. CONSOLIDATION & RECOVERY
    workflow.add_node("consolidate", consolidation_node)
    workflow.add_node("recover", null_recovery_node)
    workflow.add_node("regenerate", regeneration_node)
    workflow.add_node("excel", save_node)
    
    # --- DEFINE EDGES ---
    
    # Entry
    workflow.set_entry_point("entry")
    
    # Fan-out to parallel branches
    workflow.add_edge("entry", "groq_generate")
    workflow.add_edge("entry", "mixtral_generate")
    workflow.add_edge("entry", "cerebras_generate")
    
    # Internal branch flow
    workflow.add_edge("groq_generate", "groq_validate")
    workflow.add_edge("mixtral_generate", "mixtral_validate")
    workflow.add_edge("cerebras_generate", "cerebras_validate")
    
    # Fan-in (Merge) to consolidation
    workflow.add_edge("groq_validate", "consolidate")
    workflow.add_edge("mixtral_validate", "consolidate")
    workflow.add_edge("cerebras_validate", "consolidate")
    
    # Post-merge flow
    workflow.add_edge("consolidate", "recover")
    
    # Conditional routing
    workflow.add_conditional_edges(
        "recover",
        route_after_consolidation,
        {
            "save": "excel",
            "regenerate": "regenerate",
            "recover": "recover",
            "end": END
        }
    )
    
    workflow.add_edge("regenerate", "entry")
    workflow.add_edge("excel", END)
    
    return workflow.compile(name="PES-Parallel-Intelligence")
