import uuid
from datetime import datetime, timezone
from typing import Dict, Any

class RunStore:
    def __init__(self):
        self._runs: Dict[str, Dict[str, Any]] = {}

    def create_run(self, company_name: str) -> str:
        run_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        self._runs[run_id] = {
            "run_id": run_id,
            "company_name": company_name,
            "status": "queued",
            "progress": 0,
            "stage": "queued",
            "golden_record": None,
            "confidence_score": None,
            "errors": [],
            "created_at": now,
            "updated_at": now
        }
        return run_id

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self._runs.get(run_id)

    def update_run(self, run_id: str, **kwargs):
        if run_id in self._runs:
            self._runs[run_id].update(kwargs)
            self._runs[run_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    def list_runs(self) -> list:
        return list(self._runs.values())

run_store = RunStore()
