from abc import ABC, abstractmethod
from typing import Optional, Any

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_instr: Optional[str] = None, temperature: float = 0.3) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, response_schema: Any, system_instr: Optional[str] = None, temperature: float = 0.3) -> str:
        pass
