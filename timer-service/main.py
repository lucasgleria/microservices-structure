# timer-service/main.py

from fastapi.responses import Response
from fastapi import FastAPI
from models import Timer
from schemas import TimerStatus
from prometheus_client import start_http_server, Counter, generate_latest
from cache import get_cache, set_cache, delete_cache
import json

app = FastAPI(title="Timer Service with Cache and Invalidation")

timer = Timer()
CACHE_KEY = "timer_status"

@app.post("/start")
async def start():
    return {"message": timer.start()}

@app.post("/pause")
async def pause():
    msg = timer.pause()
    await delete_cache(CACHE_KEY)
    return {"message": msg}

@app.post("/reset")
async def reset():
    msg = timer.reset()
    await delete_cache(CACHE_KEY)
    return {"message": msg}

@app.get("/status", response_model=TimerStatus)
async def status():
    cache_key = "timer_status"
    
    cached_status = await get_cache(cache_key)
    if cached_status:
        result = json.loads(cached_status)
    else:
        result = timer.status()
        await set_cache(cache_key, json.dumps(result))
    
    return result

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/")
async def root():
    return {"message": "Timer Service Running with Cache and Invalidation"}