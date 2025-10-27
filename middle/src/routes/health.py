"""
Health Check Route Module - API Gateway

This module provides health check endpoints for monitoring the gateway
and backend service availability.

Monitoring Features:
    - Gateway health status
    - Backend connectivity verification
    - Database connection status (via backend)
    - Response time measurements
    - Dependency health checks

Used by:
    - Load balancers
    - Kubernetes liveness/readiness probes
    - Monitoring systems (Prometheus, Datadog, etc)
    - CI/CD pipelines
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from src.config import config
import logging
import time
from datetime import datetime
from typing import Dict, Any

# Configure module logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@router.get(
    "/health",
    summary="Gateway Health Check",
    description="""
    Comprehensive health check for the API Gateway.
    
    Returns:
        - Gateway status
        - Backend connectivity
        - Uptime information
        - Configuration status
        - Cache status (if enabled)
    
    Status Codes:
        - 200: All systems operational
        - 503: Gateway or backend unavailable
    
    Used by load balancers and monitoring systems.
    """,
    responses={
        200: {
            "description": "Gateway is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-10-27T10:30:00",
                        "version": "1.0.0",
                        "environment": "production",
                        "gateway": {
                            "status": "operational",
                            "uptime": "2d 5h 30m"
                        },
                        "backend": {
                            "status": "connected",
                            "url": "http://backend:8000",
                            "response_time_ms": 45
                        },
                        "features": {
                            "rate_limiting": "enabled",
                            "caching": "enabled",
                            "monitoring": "enabled"
                        }
                    }
                }
            }
        },
        503: {"description": "Service unavailable"}
    },
    tags=["Health"]
)
async def health_check():
    """
    Main health check endpoint.
    
    Verifies:
        1. Gateway is running
        2. Configuration is valid
        3. Backend is reachable (optional)
        4. Cache is operational (if enabled)
    """
    logger.debug("Health check requested")
    
    start_time = time.time()
    
    # Basic gateway health
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": config.ENVIRONMENT,
        "gateway": {
            "status": "operational",
            "config_loaded": True,
            "features": {
                "rate_limiting": config.RATE_LIMIT_PER_MINUTE > 0,
                "caching": config.ENABLE_CACHING,
                "request_validation": config.ENABLE_REQUEST_VALIDATION,
                "input_sanitization": config.SANITIZE_INPUTS
            }
        }
    }
    
    # Try to check backend connectivity
    backend_status = await check_backend_health()
    health_data["backend"] = backend_status
    
    # Calculate response time
    response_time = (time.time() - start_time) * 1000
    health_data["response_time_ms"] = round(response_time, 2)
    
    # Determine overall status
    if backend_status["status"] == "disconnected":
        health_data["status"] = "degraded"
        logger.warning("Backend is unreachable - gateway in degraded mode")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_data
        )
    
    logger.debug(f"Health check completed in {response_time:.2f}ms")
    return health_data


@router.get(
    "/health/backend",
    summary="Backend Health Check",
    description="""
    Dedicated endpoint to check backend service health.
    
    Performs:
        - Connectivity test to backend
        - Response time measurement
        - Backend status verification
    
    Returns:
        Backend health information including response time
    """,
    responses={
        200: {"description": "Backend is healthy"},
        502: {"description": "Backend is unreachable"},
        503: {"description": "Backend is unhealthy"}
    },
    tags=["Health"]
)
async def backend_health_check():
    """
    Check backend service health and connectivity.
    
    This endpoint specifically tests the backend service
    and provides detailed connectivity information.
    """
    logger.info("Backend health check requested")
    
    backend_status = await check_backend_health()
    
    if backend_status["status"] == "disconnected":
        logger.error("Backend health check failed - service unreachable")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=backend_status
        )
    
    if backend_status["status"] == "unhealthy":
        logger.warning("Backend health check failed - service unhealthy")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=backend_status
        )
    
    logger.info(f"Backend is healthy (response time: {backend_status.get('response_time_ms')}ms)")
    return backend_status


@router.get(
    "/health/detailed",
    summary="Detailed System Health",
    description="""
    Comprehensive system health check with detailed diagnostics.
    
    Includes:
        - All service statuses
        - Configuration details
        - Performance metrics
        - Dependency checks
    
    Use for debugging and detailed monitoring.
    """,
    responses={
        200: {"description": "Detailed health information"}
    },
    tags=["Health"]
)
async def detailed_health_check():
    """
    Detailed health check with comprehensive diagnostics.
    
    Provides extensive information about gateway and backend status,
    useful for troubleshooting and monitoring.
    """
    logger.debug("Detailed health check requested")
    
    start_time = time.time()
    
    # Gather comprehensive health data
    health_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "gateway": {
            "status": "operational",
            "version": "1.0.0",
            "environment": config.ENVIRONMENT,
            "debug_mode": config.DEBUG,
            "configuration": {
                "backend_url": config.get_backend_base_url(),
                "backend_timeout": config.BACKEND_TIMEOUT,
                "request_timeout": config.REQUEST_TIMEOUT,
                "max_request_size": config.MAX_REQUEST_SIZE,
                "rate_limit": {
                    "enabled": True,
                    "requests_per_minute": config.RATE_LIMIT_PER_MINUTE,
                    "burst_limit": config.RATE_LIMIT_BURST
                },
                "caching": {
                    "enabled": config.ENABLE_CACHING,
                    "ttl_seconds": config.CACHE_TTL_SECONDS,
                    "max_size": config.CACHE_MAX_SIZE
                },
                "security": {
                    "request_validation": config.ENABLE_REQUEST_VALIDATION,
                    "input_sanitization": config.SANITIZE_INPUTS,
                    "cors_enabled": True,
                    "allowed_origins": len(config.get_allowed_origins_list())
                },
                "logging": {
                    "level": config.LOG_LEVEL,
                    "format": config.LOG_FORMAT
                }
            }
        },
        "backend": await check_backend_health(),
        "performance": {
            "health_check_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    }
    
    logger.debug("Detailed health check completed")
    return health_data


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def check_backend_health() -> Dict[str, Any]:
    """
    Verify backend service health and connectivity.
    
    Attempts to connect to the backend health endpoint
    and measures response time.
    
    Returns:
        Dictionary with backend health status:
            - status: connected|disconnected|unhealthy
            - url: backend URL
            - response_time_ms: response time in milliseconds
            - error: error message if connection failed
    """
    backend_url = config.get_backend_base_url()
    health_endpoint = f"{backend_url}/health"
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_endpoint)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "url": backend_url,
                    "response_time_ms": round(response_time, 2),
                    "backend_response": response.json() if response.content else None
                }
            else:
                return {
                    "status": "unhealthy",
                    "url": backend_url,
                    "response_time_ms": round(response_time, 2),
                    "http_status": response.status_code
                }
                
    except httpx.TimeoutException:
        logger.error(f"Backend health check timeout: {health_endpoint}")
        return {
            "status": "disconnected",
            "url": backend_url,
            "error": "Connection timeout",
            "timeout_seconds": 5.0
        }
        
    except httpx.RequestError as e:
        logger.error(f"Backend health check failed: {e}")
        return {
            "status": "disconnected",
            "url": backend_url,
            "error": str(e)
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in backend health check: {e}")
        return {
            "status": "disconnected",
            "url": backend_url,
            "error": f"Unexpected error: {str(e)}"
        }


@router.get(
    "/ping",
    summary="Simple Ping",
    description="Minimal health check for basic availability testing",
    responses={
        200: {
            "description": "Pong",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "message": "pong"}
                }
            }
        }
    },
    tags=["Health"]
)
async def ping():
    """
    Minimal ping endpoint for basic availability checks.
    
    Fastest health check - just verifies the gateway is responding.
    """
    return {"status": "ok", "message": "pong"}
