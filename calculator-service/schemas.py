# calculator-service/schemas.py

from pydantic import BaseModel
from typing import Union

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str

class CalculationResponse(BaseModel):
    result: Union[float, str]
