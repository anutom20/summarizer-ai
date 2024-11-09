from pydantic import BaseModel
from typing import Optional


class GeminiPrompt(BaseModel):
    question: str
