# timer-service/schemas.py

from pydantic import BaseModel

class TimerStatus(BaseModel):
    running: bool
    elapsed: float
