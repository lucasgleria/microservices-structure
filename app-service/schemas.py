# app-service/schemas.py

from pydantic import BaseModel

class AppOut(BaseModel):
    name: str
    description: str
