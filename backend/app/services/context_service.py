from datetime import date
from sqlalchemy.orm import Session
from app.models.commitment import Commitment
from app.models.task import Task
from app.schemas.ai import Context

class ContextService:
    @staticmethod
    def build_context(db: Session, user_id: int, commitment_id: int = None) -> Context:
        today = date.today()
        
        active_commitment = None
        if commitment_id:
            c = db.query(Commitment).filter(Commitment.id == commitment_id, Commitment.user_id == user_id).first()
            if c:
                active_commitment = {
                    "id": c.id,
                    "title": c.title,
                    "due_date": str(c.due_date) if c.due_date else None,
                    "priority": c.priority
                }
                
        # Fetch pending tasks
        pending_tasks = db.query(Task).filter(Task.user_id == user_id, Task.is_done == False).all()
        tasks_data = [{"id": t.id, "title": t.title, "due_date": str(t.due_date) if hasattr(t, 'due_date') and t.due_date else None} for t in pending_tasks]
        
        return Context(
            date=today,
            user_id=user_id,
            active_commitment=active_commitment,
            tasks=tasks_data,
            calendar_events=[], # Placeholder for calendar integration
            conversation_history=[] # Placeholder for conversation history
        )
