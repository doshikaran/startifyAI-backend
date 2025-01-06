from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class HistoryEntry(BaseModel):
    user_id: str
    type: Literal["query", "health_check", "pitch_deck"]
    input: dict
    output: str
    timestamp: datetime
