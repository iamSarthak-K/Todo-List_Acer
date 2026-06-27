from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

# ---------------------------------------------------------
# Request Models (FastAPI Input)
# ---------------------------------------------------------
class ExtractRequest(BaseModel):
    text: str

class TaskPlanRequest(BaseModel):
    commitment_id: int

class ReminderRequest(BaseModel):
    task_id: int

class RecoveryRequest(BaseModel):
    task_id: int

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

# ---------------------------------------------------------
# Internal State Models (Context & Memory)
# ---------------------------------------------------------
class Context(BaseModel):
    date: date
    user_id: int
    active_commitment: Optional[Dict[str, Any]] = None
    tasks: List[Dict[str, Any]] = []
    calendar_events: List[Dict[str, Any]] = []
    conversation_history: List[Dict[str, str]] = []

class Memory(BaseModel):
    preferences: Dict[str, Any] = {}
    previous_reminders: List[str] = []
    postponement_reasons: List[str] = []
    working_habits: str = ""

# ---------------------------------------------------------
# LLM Output Models (Pydantic Validation for JSON output)
# ---------------------------------------------------------
class CommitmentOutput(BaseModel):
    title: str
    category: str
    due_date: date
    priority: str

class TaskPlanOutput(BaseModel):
    tasks: List[str]

class ReminderOutput(BaseModel):
    reminder: str

class RecoveryPlanOutput(BaseModel):
    plan: List[str]

class ChatOutput(BaseModel):
    reply: str
