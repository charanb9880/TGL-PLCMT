from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from dotenv import load_dotenv

# Ensure the root of the intelligence_pipeline is in the python path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# Load the .env file from the final_ui root directory for LangSmith tracing
load_dotenv(os.path.join(os.path.dirname(root_path), '.env'))

from app.routes.agent import router as agent_router
from app.models.api_models import HealthResponse

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Intelligence API",
    description="Scalable FastAPI backend for LangGraph workflow execution",
    version="1.0.0"
)

# CORS middleware for local development/UI integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers to ensure no raw stack traces leak to the client
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal execution error occurred.", "error": str(exc)}
    )

# Include routers
app.include_router(agent_router)

# Healthcheck
@app.get("/health", tags=["System"], response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")
