# LangGraph to FastAPI Architecture Conversion

## Overview

I have successfully analyzed the existing LangGraph pipeline and adapted it into a scalable FastAPI backend service while strictly preserving the integrity of the graph orchestration.

By leaving `graph.py` completely framework-independent, we've successfully decoupled the execution logic from the HTTP layer. I created an entirely new `app/` directory alongside the LangGraph definitions that acts as the API boundary and execution manager.

## Refactored Architecture

```text
intelligence_pipeline/
├── app/
│   ├── main.py                  # FastAPI application entry point, exception handlers
│   ├── service.py               # Workflow wrapper, maps LangGraph streams to progress tracking
│   ├── routes/
│   │   └── agent.py             # API Endpoint declarations (generate, status)
│   ├── models/
│   │   └── api_models.py        # Pydantic schemas for requests, responses, and validation
│   └── storage/
│       └── run_store.py         # In-memory execution storage and state management
├── graph.py                     # Unmodified LangGraph orchestration
├── state/                       # Unmodified LangGraph state
├── nodes/                       # Unmodified LangGraph nodes
├── models/                      # Unmodified LLM configs
└── config/                      # Unmodified environment configurations
```

## How It Works

### 1. Execution Service (`app/service.py`)
Instead of directly exposing the graph, the service layer wraps `build_graph()` and manages the workflow execution lifecycle inside an asynchronous background task.

### 2. Progress Tracking
To track progress without modifying any of your `nodes/` code, the service intercepts `app.astream()` yields. Since LangGraph yields the names of the nodes that just executed (like `entry`, `groq_generate`, `consolidate`), the service maps these node names to discrete semantic stages (e.g., `initializing`, `researching`, `consolidation`) and specific progress percentages. 

### 3. Asynchronous APIs (`app/routes/agent.py`)
The endpoints are built for scale. Calling `POST /v1/agent/generate` simply generates a `run_id`, seeds the in-memory `RunStore`, and delegates the heavy execution to a FastAPI `BackgroundTask`. The client gets an immediate `202 Accepted` response. The client can then long-poll `GET /v1/agent/status/{run_id}` to retrieve live progress updates and the final Golden Record.

### 4. Exception Handling
Exceptions happening inside the LangGraph agent are caught by `service.py`, marking the run as `failed` with the error trace stored inside the run state (preventing the server from crashing). The `main.py` entrypoint also registers a global exception handler to guarantee raw stack traces never leak to HTTP clients.

## API Usage Examples

**1. Start a Run**
```bash
curl -X POST "http://localhost:8000/v1/agent/generate" \
     -H "Content-Type: application/json" \
     -d '{"company_name": "OpenAI"}'
```
*Response:*
```json
{
  "run_id": "64b18c72-4e44-42f2-8c10-eb529cc559d2",
  "status": "queued",
  "message": "Workflow successfully queued for execution."
}
```

**2. Check Run Status**
```bash
curl -X GET "http://localhost:8000/v1/agent/status/64b18c72-4e44-42f2-8c10-eb529cc559d2"
```
*Response:*
```json
{
  "run_id": "64b18c72-4e44-42f2-8c10-eb529cc559d2",
  "status": "running",
  "progress": 60,
  "stage": "validating",
  "golden_record": null,
  "errors": [],
  "created_at": "2026-05-16T01:40:00Z",
  "updated_at": "2026-05-16T01:40:15Z"
}
```

## Running the Server

You can run the new architecture directly using Uvicorn from the `intelligence_pipeline` directory:

```bash
cd intelligence_pipeline
uvicorn app.main:app --reload --port 8000
```

*(Note: We used `app.main:app` so Python resolves the local imports properly).*

## Next Steps

1. **Persistence:** The `app/storage/run_store.py` currently uses an in-memory dictionary. For production, you should swap this to store results directly into Postgres/Supabase.
2. **Webhooks:** The Pydantic request model includes an optional `webhook_url`. You can update `service.py` to trigger a `POST` request to this URL when execution hits 100%.
