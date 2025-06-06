# api-gateway/main.py

from fastapi.responses import Response
from fastapi import FastAPI, Request, HTTPException, Depends
import httpx
import logging
import json
import time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter, generate_latest
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="API Gateway")

origins = [
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_SERVICE_URL = "http://auth-service:5000"
APP_SERVICE_URL = "http://app-service:5001"
CALCULATOR_SERVICE_URL = "http://calculator-service:5002"
TIMER_SERVICE_URL = "http://timer-service:5003"

TIMEOUT = 5.0  # segundos

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Logger estruturado
logger = logging.getLogger("api-gateway")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_event(event_type: str, detail: dict):
    log_entry = {
        "event": event_type,
        "detail": detail
    }
    logger.info(json.dumps(log_entry))

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        log_event("auth", {"user": payload.get("sub")})
        return payload
    except JWTError:
        log_event("auth_error", {"token": token})
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

async def forward_request(method: str, url: str, request: Request):
    start_time = time.time()
    try:
        log_event("request", {"method": method, "url": url})
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=request.headers.raw,
                params=request.query_params,
                content=await request.body()
            )
            duration = round(time.time() - start_time, 4)
            log_event("response", {
                "status_code": response.status_code,
                "url": url,
                "duration": duration
            })
            return response.json()
    except httpx.ConnectError:
        log_event("error", {"type": "ConnectError", "url": url})
        raise HTTPException(status_code=502, detail=f"Failed to connect to {url}")
    except httpx.TimeoutException:
        log_event("error", {"type": "Timeout", "url": url})
        raise HTTPException(status_code=504, detail=f"Timeout when connecting to {url}")
    except Exception as e:
        log_event("error", {"type": "Exception", "error": str(e), "url": url})
        raise HTTPException(status_code=500, detail=str(e))

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(request: Request):
    url = f"{AUTH_SERVICE_URL}/auth/{request.path_params['path']}"
    return await forward_request(request.method, url, request)

@app.api_route("/apps", methods=["GET"])
async def proxy_apps(request: Request, user=Depends(verify_jwt_token)):
    url = f"{APP_SERVICE_URL}/apps"
    return await forward_request("GET", url, request)

@app.api_route("/calculate", methods=["POST"])
async def proxy_calculate(request: Request, user=Depends(verify_jwt_token)):
    url = f"{CALCULATOR_SERVICE_URL}/calculate"
    return await forward_request("POST", url, request)

@app.api_route("/timer/{action}", methods=["GET", "POST"])
async def proxy_timer(request: Request, action: str, user=Depends(verify_jwt_token)):
    url = f"{TIMER_SERVICE_URL}/{action}"
    return await forward_request(request.method, url, request)

@app.get("/")
async def root():
    log_event("health_check", {"message": "API Gateway Running"})
    return {"message": "API Gateway Running"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")