from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class GenerateRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company to research")
    webhook_url: Optional[str] = Field(None, description="Optional webhook URL for progress/completion callbacks")

class GenerateResponse(BaseModel):
    run_id: str = Field(..., description="Unique ID for the background execution run")
    status: str = Field(..., description="Initial status of the run (e.g. queued, running)")
    message: str = Field(..., description="Response message")

class RunStatusResponse(BaseModel):
    run_id: str
    status: str
    progress: int = Field(0, description="Percentage completion (0-100)")
    stage: str = Field("queued", description="Current execution stage")
    golden_record: Optional[Dict[str, Any]] = Field(None, description="The final structured output")
    confidence_score: Optional[float] = Field(None, description="Confidence score out of 100 based on data completeness")
    errors: Optional[List[str]] = Field(None, description="Any errors encountered during execution")
    created_at: str
    updated_at: str

class HealthResponse(BaseModel):
    status: str = "ok"
