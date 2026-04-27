from pydantic import BaseModel
from typing import List

class AnimeItem(BaseModel):
    title: str
    description: str
    genres: List[str]
    rating: float
    score: float
    reason: str

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    interpreted_preferences: List[str]
    recommendations: List[AnimeItem]
    assistant_message: str
