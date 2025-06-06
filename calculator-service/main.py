# calculator-service/main.py

from fastapi.responses import Response
from fastapi import FastAPI
from models import Calculator
from schemas import CalculationRequest, CalculationResponse
from prometheus_client import start_http_server, Counter, generate_latest
from cache import get_cache, set_cache

import json

app = FastAPI(title="Calculator Service")

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(req: CalculationRequest):
    cache_key = f"{req.a}:{req.b}:{req.operation}"
    
    # Check cache
    cached_result = await get_cache(cache_key)
    if cached_result:
        result = json.loads(cached_result)
    else:
        result = Calculator.calculate(req.a, req.b, req.operation)
        await set_cache(cache_key, json.dumps(result))
    
    return {"result": result}

@app.get("/")
async def root():
    return {"message": "Calculator Service Running with Cache"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")