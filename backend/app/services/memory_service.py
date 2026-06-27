from sqlalchemy.orm import Session
from app.schemas.ai import Memory

class MemoryService:
    @staticmethod
    def build_memory(db: Session, user_id: int) -> Memory:
        # In a real implementation, this would query a user preferences table,
        # past reminders, habit data, etc.
        # For now, it returns an empty structured memory object.
        return Memory(
            preferences={},
            previous_reminders=[],
            postponement_reasons=[],
            working_habits=""
        )
