import operator
from typing import TypedDict, List, Dict, Any, Annotated

class InputState(TypedDict):
    company_name: str

class GraphState(InputState):
    llm_outputs: Annotated[List[Dict[str, Any]], operator.add]
    validated_outputs: Annotated[List[Dict[str, Any]], operator.add]
    golden_record: Dict[str, Any]
    errors: Annotated[List[str], operator.add]
    retry_count: int
    failed_fields: List[str]
    search_context: str
