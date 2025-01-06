# backend/app/models/pitch_deck_model.py
from pydantic import BaseModel, Field

class PitchDeckInput(BaseModel):
    name: str = Field(..., description="Startup Name")
    domain: str = Field(..., description="Startup Domain")
    problem: str = Field(..., description="Problem Statement") 
    solution: str = Field(..., description="Startup Solution")
    founders: str = Field(..., description="Founder Names")
