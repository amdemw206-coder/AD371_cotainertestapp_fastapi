Containerized FastAPI Microservice
1. Project Title & Architecture Overview

This project containerizes and orchestrates a lightweight Python FastAPI microservice with a landing page (/), a health check endpoint (/healthz), and a runtime metadata endpoint (/metadata) showing hostname and uptime.

    Base Image: Multi-stage build using python:3.11-alpine to keep the final image small, avoid bloated base images, copy requirements.txt before main.py for layer caching, and run as a non-root user (appuser).

    Orchestration Strategy: Managed locally with Docker Compose (docker-compose.yml), configured with CPU/memory limits and reservations, a restart: unless-stopped policy, a health check on /healthz, .env configuration, and multi-replica scaling.

2. Prerequisites & Run Guide

    Prerequisites: Docker Desktop installed and running with virtualization enabled (WSL 2 on Windows) and the project files (main.py, requirements.txt, Dockerfile, docker-compose.yml, .env) in your working directory.

    Build the Docker image:
    PowerShell

    docker build -t fastapi-production-app:latest .

    Start the orchestration stack:
    PowerShell

    docker compose up --build -d

    Access the application and verify health:
    PowerShell

    docker compose ps
    curl.exe -i http://localhost:8000/
    curl.exe http://localhost:8000/healthz
    curl.exe http://localhost:8000/metadata

    (If replicas use dynamic host ports when scaled, open the mapped http://localhost:<port>/ address shown in docker compose ps.)

    Tear down the environment:
    PowerShell

    docker compose down

3. AI Disclosure & Prompt Appendix

    AI Tool Used: Gemini.

    Prompts Submitted:

        Initial prompt asking to act as a senior DevOps and cloud infrastructure architect to generate a production Dockerfile, an orchestration manifest (Option A: Docker Compose), minimal FastAPI app code, and build/run/scale commands.

        Follow-up prompts covering the Step 2 container reality check, VS Code setup, Step 3 QA checklist steps, troubleshooting Windows/Docker/Compose/PowerShell issues, and summarizing containerization trade-offs.

    What Worked vs. What Was Patched:

        Produced correctly: A lightweight FastAPI app with /, /healthz, and /metadata; a multi-stage python:3.11-alpine Dockerfile copying requirements.txt before main.py with a non-root appuser; and a Compose manifest with resource limits and health checks.

        Issues & fixes encountered:

            Removed container_name from docker-compose.yml so multi-replica scaling wouldn't fail on duplicate container names, and used dynamic host port mapping ("8000") when scaling multiple replicas on one host so port 8000 wouldn't conflict.

            Fixed Uvicorn's module target from main.py:app to main:app and ensured /home/appuser and /app ownership so the container didn't crash-loop as appuser.

            Updated the health check to target 127.0.0.1 instead of localhost so containers reported healthy cleanly.

            Used curl.exe / Invoke-WebRequest in PowerShell instead of Linux-style curl -i.

4. QA Checklist Summary

    [x] Container Image & Build Verification: Built fastapi-production-app:latest cleanly, verified image size/tags with docker images, and confirmed processes ran as non-root appuser via docker compose top.

    [x] Functional & Endpoint Testing: Verified / returned HTTP 200 OK, /healthz returned {"status": "healthy"}, and /metadata returned dynamic container hostname and uptime.

    [~] Orchestration & Resilience Testing:

        Scaling: Scaled to 3 replicas (docker compose up --build --scale web=3 -d) and verified all 3 replicas ran in a (healthy) state.

        Self-Healing / Auto-Restart: Tested with docker kill fastapi-devops-app-web-2 (restart: unless-stopped was set), but web-2 remained Exited (137) rather than auto-recreating on its own; reconciled desired scale via docker compose up -d --scale web=3 and noted the self-healing check as not passing automatically.

    [x] Browser Console & Health Check Status: Checked the app in browser DevTools—/ returned HTTP 200 with headers and timing, the console had no uncaught frontend errors, and the browser's automatic /favicon.ico request was noted as non-blocking.