from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user

from app.schemas.ai import (
    ExtractRequest, CommitmentOutput,
    TaskPlanRequest, TaskPlanOutput,
    ReminderRequest, ReminderOutput,
    RecoveryRequest, RecoveryPlanOutput,
    ChatRequest, ChatOutput
)

from app.services.context_service import ContextService
from app.services.memory_service import MemoryService
from app.ai.graph.graph import ai_graph

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/extract", response_model=CommitmentOutput)
async def extract_commitment(request: ExtractRequest, current_user: User = Depends(get_current_user)):
    state = {
        "user_id": current_user.id,
        "action": "extract",
        "input": request.text,
        "context": None,
        "memory": None
    }
    result_state = ai_graph.invoke(state)
    return result_state["response"]

@router.post("/plan", response_model=TaskPlanOutput)
async def plan_tasks(request: TaskPlanRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    context = ContextService.build_context(db, current_user.id, request.commitment_id)
    
    state = {
        "user_id": current_user.id,
        "action": "plan",
        "input": None,
        "context": context.model_dump(),
        "memory": None
    }
    result_state = ai_graph.invoke(state)
    return result_state["response"]

@router.post("/reminder", response_model=ReminderOutput)
async def generate_reminder(request: ReminderRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    memory = MemoryService.build_memory(db, current_user.id)
    
    state = {
        "user_id": current_user.id,
        "action": "reminder",
        "input": {"task_id": request.task_id, "days_left": 2}, # Mocked days left for now
        "context": None,
        "memory": memory.model_dump()
    }
    result_state = ai_graph.invoke(state)
    return result_state["response"]

@router.post("/recover", response_model=RecoveryPlanOutput)
async def generate_recovery(request: RecoveryRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    context = ContextService.build_context(db, current_user.id)
    
    state = {
        "user_id": current_user.id,
        "action": "recover",
        "input": {"task_id": request.task_id, "days_left": 1},
        "context": context.model_dump(),
        "memory": None
    }
    result_state = ai_graph.invoke(state)
    return result_state["response"]

@router.post("/chat", response_model=ChatOutput)
async def chat_assistant(request: ChatRequest, current_user: User = Depends(get_current_user)):
    state = {
        "user_id": current_user.id,
        "action": "chat",
        "input": {"message": request.message, "history": request.history},
        "context": None,
        "memory": None
    }
    result_state = ai_graph.invoke(state)
    return result_state["response"]
