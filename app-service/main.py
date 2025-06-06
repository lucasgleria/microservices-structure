# app-service/main.py

from fastapi.responses import Response
from fastapi import FastAPI
from models import App
from schemas import AppOut
from prometheus_client import start_http_server, Counter, generate_latest


app = FastAPI(title="App Service")

available_apps = [
    App(name="Calculator", description="Basic calculator operations."),
    App(name="Timer", description="Simple timer and stopwatch.")
]

@app.get("/apps", response_model=list[AppOut])
async def get_apps():
    return [AppOut(name=app.name, description=app.description) for app in available_apps]

@app.get("/")
async def root():
    return {"message": "App Service Running"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")