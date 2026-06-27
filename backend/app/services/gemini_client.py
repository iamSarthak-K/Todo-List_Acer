import os
import logging
from typing import Optional, Any
from google import genai
from google.genai import types
from app.services.llm_client import LLMClient
from app.config import settings

class GeminiClient(LLMClient):
    def __init__(self):
        # The key must be in the environment variables
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logging.warning("GEMINI_API_KEY is not set in the environment.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3.5-flash"

    def _build_config(self, system_instr: Optional[str], temperature: float, response_schema: Any = None) -> types.GenerateContentConfig:
        config_args = {
            "temperature": temperature,
            "max_output_tokens": 1000
        }
        if system_instr:
            config_args["system_instruction"] = system_instr
        if response_schema:
            config_args["response_mime_type"] = "application/json"
            config_args["response_schema"] = response_schema
            
        return types.GenerateContentConfig(**config_args)

    def generate(self, prompt: str, system_instr: Optional[str] = None, temperature: float = 0.3) -> str:
        if not self.client:
            raise ValueError("Gemini API key not configured")
        
        contents = [types.UserContent(parts=[types.Part.from_text(text=prompt)])]
        config = self._build_config(system_instr, temperature)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=config
            )
            return response.text
        except Exception as e:
            logging.error(f"Gemini generation failed: {e}")
            raise

    def generate_json(self, prompt: str, response_schema: Any, system_instr: Optional[str] = None, temperature: float = 0.3) -> str:
        if not self.client:
            raise ValueError("Gemini API key not configured")
            
        contents = [types.UserContent(parts=[types.Part.from_text(text=prompt)])]
        config = self._build_config(system_instr, temperature, response_schema)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=config
            )
            return response.text
        except Exception as e:
            logging.error(f"Gemini JSON generation failed: {e}")
            raise
