from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
import logging

T = TypeVar('T', bound=BaseModel)

class Parser:
    @staticmethod
    def parse_json(json_str: str, schema: Type[T]) -> T:
        """Parses a JSON string into a Pydantic model. Raises ValidationError if it fails."""
        try:
            return schema.model_validate_json(json_str)
        except ValidationError as e:
            logging.error(f"Failed to parse LLM output against {schema.__name__}: {e}\nRaw output: {json_str}")
            raise
