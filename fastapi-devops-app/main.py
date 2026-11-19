import os
import time
from fastapi import FastAPI, Response, status

app = FastAPI(title="DevOps Lightweight Microservice", version="1.0.0")
START_TIME = time.time()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the containerized microservice!",
        "status": "online",
        "service": "fastapi-production-app"
    }

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    # Perform quick internal dependency or state checks here if needed
    return {"status": "healthy"}

@app.get("/metadata")
def runtime_metadata():
    return {
        "hostname": os.uname().nodename,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "environment": os.getenv("ENVIRONMENT", "production"),
    }