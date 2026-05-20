import asyncio
import logging
from app.storage.run_store import run_store
from graph import build_graph

logger = logging.getLogger(__name__)

# Map node names to execution stages and overall completion percentages
NODE_STAGE_MAPPING = {
    "entry": {"stage": "initializing", "progress": 10},
    "groq_generate": {"stage": "researching", "progress": 30},
    "mixtral_generate": {"stage": "researching", "progress": 30},
    "cerebras_generate": {"stage": "researching", "progress": 30},
    "groq_validate": {"stage": "validating", "progress": 60},
    "mixtral_validate": {"stage": "validating", "progress": 60},
    "cerebras_validate": {"stage": "validating", "progress": 60},
    "consolidate": {"stage": "consolidation", "progress": 80},
    "recover": {"stage": "recovery", "progress": 85},
    "regenerate": {"stage": "regenerating", "progress": 40},
    "excel": {"stage": "formatting", "progress": 95}
}

class WorkflowService:
    def __init__(self):
        # We compile the graph once per worker to avoid recompilation overhead
        self.app = build_graph()

    async def execute_run(self, run_id: str, company_name: str):
        logger.info(f"Starting execution for run_id={run_id}, company={company_name}")
        run_store.update_run(run_id, status="running", stage="starting", progress=5)
        
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
        
        try:
            # We use astream to capture events node-by-node and update progress
            async for output in self.app.astream(initial_state, {"recursion_limit": 15}):
                for key, value in output.items():
                    if key in NODE_STAGE_MAPPING:
                        stage_info = NODE_STAGE_MAPPING[key]
                        run_store.update_run(
                            run_id,
                            stage=stage_info["stage"],
                            progress=stage_info["progress"]
                        )
                    
                    # Capture any graph errors
                    if value.get("errors"):
                        run_store.update_run(run_id, errors=value["errors"])

                    # On final successful stage
                    if key == "excel" or key == "consolidate":
                        # Attempt to capture the golden record if it exists
                        golden_record = value.get("golden_record")
                        if golden_record:
                            # Force a valid Logo URL using Clearbit based on Website URL
                            website_url = golden_record.get("Website URL", "")
                            if website_url and str(website_url).lower() not in ["null", "none", "n/a", "unknown", ""]:
                                import urllib.parse
                                try:
                                    if not website_url.startswith('http'):
                                        website_url = 'http://' + website_url
                                    domain = urllib.parse.urlparse(website_url).netloc
                                    if domain:
                                        golden_record["Logo"] = f"https://logo.clearbit.com/{domain}"
                                except Exception:
                                    pass

                            # Calculate simple extraction confidence score based on completeness
                            exclusions = [
                                "null", "none", "n/a", "unknown", "", "not available", 
                                "not explicitly reported", "not found", "confidential / market estimated", 
                                "optimized / standard industry data", "modern cloud-native stack (saas, aws/azure, ai-ready)",
                                "industry standard compliance (soc2/iso)"
                            ]
                            filled_fields = sum(1 for v in golden_record.values() if v and str(v).lower() not in exclusions)
                            total_fields = max(len(golden_record), 163)
                            confidence_score = round((filled_fields / total_fields) * 100, 2)
                            
                            run_store.update_run(
                                run_id, 
                                golden_record=golden_record,
                                confidence_score=confidence_score
                            )

            run_store.update_run(run_id, status="completed", stage="completed", progress=100)
            logger.info(f"Successfully completed run_id={run_id}")

        except Exception as e:
            logger.error(f"Execution failed for run_id={run_id}: {str(e)}", exc_info=True)
            run_store.update_run(
                run_id, 
                status="failed", 
                stage="failed", 
                errors=[str(e)]
            )

workflow_service = WorkflowService()
