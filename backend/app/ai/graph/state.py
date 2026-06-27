from typing import TypedDict, Optional, Dict, Any

class AIState(TypedDict):
    user_id: int
    action: str
    context: Optional[Dict[str, Any]]
    memory: Optional[Dict[str, Any]]
    input: Optional[Any]
    response: Optional[Any]
