# auth-service/main.py

from fastapi.responses import Response
from fastapi import FastAPI, Depends
from auth import router as auth_router
from auth_utils import get_current_user
from prometheus_client import start_http_server, Counter, generate_latest


app = FastAPI(title="Auth Service")

app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Auth Service Running"}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['email']}! This is a protected route."}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
