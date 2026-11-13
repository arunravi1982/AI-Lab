import os
import time
import uuid
import asyncio
import logging

from datetime import datetime, timezone
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")

CACHE_TTL_SECONDS = int(
    os.getenv("CACHE_TTL_SECONDS", "30")
)

MAX_CONCURRENT_REQUESTS = int(
    os.getenv("MAX_CONCURRENT_REQUESTS", "3")
)


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="IT Operations AI Assistant",
    description="AI-powered IT service investigation API",
    version="1.0.0"
)


# --------------------------------------------------
# 4. SIMULATED IT SERVICES
# --------------------------------------------------

IT_SERVICES = {

    "payment": {
        "status": "DOWN",
        "cpu": 95,
        "memory": 88,
        "response_time": 15000,
        "description": "Payment processing service"
    },

    "authentication": {
        "status": "UP",
        "cpu": 35,
        "memory": 45,
        "response_time": 120,
        "description": "User authentication service"
    },

    "notification": {
        "status": "UP",
        "cpu": 25,
        "memory": 40,
        "response_time": 90,
        "description": "Notification delivery service"
    },
    "database": {
       "status": "UP",
       "cpu": 55,
       "memory": 65,
       "response_time": 250,
       "description": "Enterprise database service"
   }

}


# --------------------------------------------------
# 5. CACHE STORAGE
# --------------------------------------------------

service_cache = {}

cache_lock = asyncio.Lock()

metrics_lock = asyncio.Lock()

request_semaphore = asyncio.Semaphore(
    MAX_CONCURRENT_REQUESTS
)


# --------------------------------------------------
# 6. PERFORMANCE METRICS
# --------------------------------------------------

metrics = {

    "total_requests": 0,

    "successful_requests": 0,

    "failed_requests": 0,

    "cache_hits": 0,

    "cache_misses": 0,

    "total_processing_time": 0.0
}


# --------------------------------------------------
# 7. REQUEST MODEL
# --------------------------------------------------

class InvestigationRequest(BaseModel):

    services: List[str] = Field(
        default=["payment"],
        min_length=1,
        max_length=3
    )

    question: str = Field(
        default="Investigate the service health",
        min_length=5,
        max_length=500
    )


# --------------------------------------------------
# 8. CACHE IMPLEMENTATION
# --------------------------------------------------

async def get_cached_result(service_name):

    async with cache_lock:

        cached = service_cache.get(service_name)

        if cached:

            result, created_at = cached

            age = time.monotonic() - created_at

            if age < CACHE_TTL_SECONDS:

                metrics["cache_hits"] += 1

                logger.info(
                    f"Cache HIT for {service_name}"
                )

                return result

            else:

                del service_cache[service_name]

        metrics["cache_misses"] += 1

        logger.info(
            f"Cache MISS for {service_name}"
        )

        return None


async def store_cached_result(service_name, result):

    async with cache_lock:

        service_cache[service_name] = (
            result,
            time.monotonic()
        )


# --------------------------------------------------
# 9. SIMULATED SERVICE HEALTH CHECK
# --------------------------------------------------

async def check_service(service_name):

    cached_result = await get_cached_result(
        service_name
    )

    if cached_result is not None:

        return cached_result

    logger.info(
        f"Checking service: {service_name}"
    )

    # Simulate a slow monitoring API call.
    await asyncio.sleep(2)

    service_data = IT_SERVICES[service_name]

    result = {

        "service": service_name,

        "status": service_data["status"],

        "cpu": service_data["cpu"],

        "memory": service_data["memory"],

        "response_time": service_data["response_time"],

        "description": service_data["description"]

    }

    await store_cached_result(
        service_name,
        result
    )

    return result


# --------------------------------------------------
# 10. PARALLEL SERVICE INVESTIGATION
# --------------------------------------------------

async def investigate_services(service_names):

    logger.info(
        f"Starting parallel checks: {service_names}"
    )

    start_time = time.perf_counter()

    tasks = [

        check_service(service)

        for service in service_names

    ]

    results = await asyncio.gather(*tasks)

    elapsed_time = time.perf_counter() - start_time

    logger.info(
        f"Service checks completed in {elapsed_time:.2f}s"
    )

    return results


# --------------------------------------------------
# 11. OPENAI LLM INITIALIZATION
# --------------------------------------------------

def get_llm():

    if not OPENAI_API_KEY:

        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is not configured."
        )

    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0,
        api_key=OPENAI_API_KEY
    )


# --------------------------------------------------
# 12. AI INVESTIGATION
# --------------------------------------------------

async def generate_ai_analysis(question, service_results):

    llm = get_llm()

    prompt = f"""
You are an experienced IT Operations Engineer.

Analyze the following IT service health information.

User question:
{question}

Service information:
{service_results}

Provide the following:

1. Overall system health.
2. Services experiencing problems.
3. Possible causes based on the supplied metrics.
4. Business impact.
5. Recommended troubleshooting steps.

Important:
- Use only the supplied service information.
- Do not invent metrics.
- Clearly identify assumptions.
- Do not claim that you performed any remediation.
"""

    response = await llm.ainvoke(prompt)

    return str(response.content)


# --------------------------------------------------
# 13. HEALTH CHECK ENDPOINT
# --------------------------------------------------

@app.get("/health")
async def health_check():

    return {

        "status": "healthy",

        "application": "IT Operations AI Assistant",

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()

    }


# --------------------------------------------------
# 14. SERVICE LIST ENDPOINT
# --------------------------------------------------

@app.get("/services")
async def list_services():

    return {

        "available_services": list(
            IT_SERVICES.keys()
        )

    }


# --------------------------------------------------
# 15. MAIN AGENT ENDPOINT
# --------------------------------------------------

@app.post("/agent/investigate")
async def investigate(request: InvestigationRequest):

    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    logger.info(
        f"Request started | ID={request_id}"
    )

    async with metrics_lock:

        metrics["total_requests"] += 1

    try:

        # Validate requested services.

        requested_services = [
            service.strip().lower()
            for service in request.services
        ]

        invalid_services = [

            service

            for service in requested_services

            if service not in IT_SERVICES

        ]

        if invalid_services:

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Unknown service",
                    "invalid_services": invalid_services
                }
            )

        # Apply concurrency control.

        async with request_semaphore:

            # Execute service checks in parallel.

            service_results = await investigate_services(
                requested_services
            )

            # Generate AI analysis.

            analysis = await generate_ai_analysis(
                request.question,
                service_results
            )

        processing_time = (
            time.perf_counter() - start_time
        )

        async with metrics_lock:

            metrics["successful_requests"] += 1

            metrics["total_processing_time"] += (
                processing_time
            )

        logger.info(
            f"Request completed | ID={request_id} "
            f"| Time={processing_time:.2f}s"
        )

        return {

            "request_id": request_id,

            "status": "success",

            "service_results": service_results,

            "ai_analysis": analysis,

            "processing_time_seconds": round(
                processing_time, 2
            )

        }

    except HTTPException:

        async with metrics_lock:

            metrics["failed_requests"] += 1

        raise

    except Exception as error:

        async with metrics_lock:

            metrics["failed_requests"] += 1

        logger.exception(
            f"Request failed | ID={request_id}"
        )

        raise HTTPException(
            status_code=500,
            detail="The investigation could not be completed."
        )


# --------------------------------------------------
# 16. PERFORMANCE METRICS ENDPOINT
# --------------------------------------------------

@app.get("/metrics")
async def get_metrics():

    async with metrics_lock:

        current_metrics = metrics.copy()

    async with cache_lock:

        current_cache_size = len(service_cache)

    total = current_metrics["total_requests"]

    average_time = (

        current_metrics["total_processing_time"] / total

        if total > 0

        else 0

    )

    return {

        "total_requests": total,

        "successful_requests":
            current_metrics["successful_requests"],

        "failed_requests":
            current_metrics["failed_requests"],

        "cache_hits":
            current_metrics["cache_hits"],

        "cache_misses":
            current_metrics["cache_misses"],

        "cache_entries": current_cache_size,

        "average_processing_time_seconds": round(
            average_time, 2
        )

    }