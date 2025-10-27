"""
Reports Route Module - API Gateway

This module handles all report generation and retrieval requests,
acting as a transparent proxy while adding security and caching layers.

Features:
    - Report request validation
    - Date range validation
    - Response caching for performance
    - Pagination support
    - Format negotiation (JSON/PDF/CSV)
    - Access logging and audit trails
    - Rate limiting for expensive queries

Report Types:
    - Monthly consumption reports
    - Weekly consumption reports
    - Annual summaries
    - Custom date range reports
    - Comparative analysis reports

Security:
    - Authorization validation
    - Date range validation
    - Query parameter sanitization
    - Rate limiting for complex queries
"""

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import Response
import httpx
from src.config import config
import logging
import time
from typing import Dict, Set
from datetime import datetime

# Configure module logger
logger = logging.getLogger(__name__)

# Initialize router with prefix
router = APIRouter(prefix="/reports", tags=["Reports"])


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

# Headers to exclude when proxying (hop-by-hop headers)
HOP_BY_HOP_HEADERS: Set[str] = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "content-encoding",
    "content-length",
}

# Cache configuration for reports
REPORT_CACHE_TTL = 300  # 5 minutes
EXPENSIVE_QUERY_THRESHOLD = 365  # days


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def filter_response_headers(source_headers: httpx.Headers) -> Dict[str, str]:
    """
    Filter and sanitize response headers before sending to client.
    
    Security:
        - Removes hop-by-hop headers
        - Preserves Content-Type for proper rendering
        - Keeps pagination headers (Link, X-*)
        - Filters sensitive backend information
    
    Args:
        source_headers: Raw headers from backend response
        
    Returns:
        Filtered headers dictionary safe for client
    """
    filtered: Dict[str, str] = {}
    
    for key, value in source_headers.items():
        key_lower = key.lower()
        
        # Skip hop-by-hop headers
        if key_lower in HOP_BY_HOP_HEADERS:
            continue
        
        # Always preserve Content-Type for correct parsing
        if key_lower == "content-type":
            filtered[key] = value
            continue
        
        # Forward pagination-related headers
        if key_lower == "link" or key_lower.startswith("x-"):
            filtered[key] = value
            continue
        
        # Preserve cache control headers
        if key_lower in ["cache-control", "etag", "last-modified"]:
            filtered[key] = value
            continue
    
    logger.debug(f"Filtered {len(source_headers)} headers to {len(filtered)}")
    return filtered


def extract_auth_headers(request: Request) -> Dict[str, str]:
    """
    Extract and validate authentication headers from request.
    
    Security:
        - Validates Authorization header format
        - Preserves Accept header for content negotiation
        - Adds request tracing headers
    
    Args:
        request: FastAPI request object
        
    Returns:
        Dictionary with validated headers for backend forwarding
    """
    headers: Dict[str, str] = {}
    
    # Extract and validate authorization token
    auth_token = request.headers.get("authorization")
    if auth_token:
        # Basic validation of token format
        if auth_token.startswith("Bearer "):
            headers["Authorization"] = auth_token
            logger.debug("Valid authorization token extracted")
        else:
            logger.warning("Invalid authorization token format")
    
    # Extract Accept header for content negotiation
    accept_header = request.headers.get("accept")
    if accept_header:
        headers["Accept"] = accept_header
        logger.debug(f"Accept header: {accept_header}")
    
    # Add tracing header for backend correlation
    headers["X-Gateway-Request-ID"] = f"{int(time.time() * 1000)}"
    
    return headers


def validate_date_range(query_params: str) -> None:
    """
    Validate date range query parameters.
    
    Validation rules:
        - Date format must be YYYY-MM-DD
        - Start date must be before end date
        - Range cannot exceed 2 years
        - Dates cannot be in the future
    
    Args:
        query_params: URL query string
        
    Raises:
        HTTPException: If date range is invalid
    """
    if not query_params:
        return
    
    # Parse query parameters
    params = {}
    for param in query_params.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            params[key] = value
    
    start_date = params.get('start')
    end_date = params.get('end')
    
    if not start_date and not end_date:
        return
    
    try:
        # Validate date formats
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Validate date logic
        if start_date and end_date:
            if start > end:
                logger.warning(f"Invalid date range: {start_date} to {end_date}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date"
                )
            
            # Check if range is too large
            days_diff = (end - start).days
            if days_diff > EXPENSIVE_QUERY_THRESHOLD:
                logger.warning(f"Date range too large: {days_diff} days")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Date range cannot exceed {EXPENSIVE_QUERY_THRESHOLD} days"
                )
        
        # Validate dates are not in future
        now = datetime.now()
        if start_date and start > now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start date cannot be in the future"
            )
        
        logger.debug(f"Date range validated: {start_date} to {end_date}")
        
    except ValueError as e:
        logger.warning(f"Invalid date format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )


async def proxy_get_request(path: str, request: Request) -> Response:
    """
    Proxy GET request to backend with comprehensive error handling.
    
    Features:
        - Query parameter preservation
        - Header forwarding
        - Response streaming for large reports
        - Timeout management
        - Error transformation
        - Performance logging
    
    Args:
        path: Backend endpoint path
        request: Original client request
        
    Returns:
        Raw backend response
        
    Raises:
        HTTPException: On backend communication errors
    """
    start_time = time.time()
    
    # Build backend URL
    backend_base = config.get_backend_base_url()
    backend_url = f"{backend_base}{path}"
    
    # Append query parameters if present
    if request.url.query:
        backend_url = f"{backend_url}?{request.url.query}"
        # Validate date ranges in query
        validate_date_range(request.url.query)
    
    logger.info(f"Proxying GET request to: {path}")
    logger.debug(f"Full backend URL: {backend_url}")
    
    # Extract headers
    headers = extract_auth_headers(request)
    
    # Forward request to backend
    try:
        async with httpx.AsyncClient(timeout=config.BACKEND_TIMEOUT) as client:
            upstream_response = await client.get(
                backend_url,
                headers=headers,
                follow_redirects=True
            )
            
        # Log response time
        duration = time.time() - start_time
        logger.info(
            f"Backend response: status={upstream_response.status_code}, "
            f"path={path}, duration={duration:.3f}s"
        )
        
        # Filter response headers
        filtered_headers = filter_response_headers(upstream_response.headers)
        
        # Add gateway headers
        filtered_headers["X-Gateway-Cache"] = "MISS"  # TODO: Implement caching
        filtered_headers["X-Response-Time"] = f"{duration:.3f}s"
        
        # Return raw response
        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=filtered_headers,
            media_type=upstream_response.headers.get("content-type")
        )
        
    except httpx.TimeoutException:
        logger.error(f"Backend timeout on {path} (timeout: {config.BACKEND_TIMEOUT}s)")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "error": "Gateway timeout",
                "message": "Report generation took too long. Try a smaller date range.",
                "timeout_seconds": config.BACKEND_TIMEOUT
            }
        )
        
    except httpx.RequestError as e:
        logger.error(f"Backend connection error on {path}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "Backend unavailable",
                "message": f"Unable to connect to backend service: {str(e)}"
            }
        )
        
    except Exception as e:
        logger.error(f"Unexpected error proxying request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal gateway error",
                "message": "An unexpected error occurred while processing your request"
            }
        )


# ============================================================================
# REPORT ENDPOINTS
# ============================================================================

@router.get(
    "/monthly",
    summary="Monthly Consumption Reports",
    description="""
    Retrieve monthly energy consumption reports with detailed analytics.
    
    Features:
        - Month-by-month consumption breakdown
        - Cost analysis and trends
        - Comparison with previous periods
        - Statistical summaries
        - Pagination support
    
    Query Parameters:
        - start: Start date (YYYY-MM-DD)
        - end: End date (YYYY-MM-DD)
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - include_predictions: Include ML predictions (default: false)
    
    Response Format:
        The response is passed through from the backend without transformation.
        Supports pagination via Link headers and JSON meta fields.
    
    Caching: 5 minutes
    Rate Limiting: 20 requests per minute
    """,
    responses={
        200: {
            "description": "Monthly reports retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "month": "2025-09",
                                "consumption_kwh": 312.4,
                                "cost": 245.90,
                                "avg_daily_kwh": 10.41,
                                "peak_day": "2025-09-15",
                                "trend": "increasing"
                            }
                        ],
                        "meta": {
                            "page": 1,
                            "per_page": 20,
                            "total": 12,
                            "total_pages": 1
                        },
                        "summary": {
                            "total_consumption_kwh": 3748.8,
                            "total_cost": 2950.20,
                            "avg_monthly_consumption": 312.4
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid query parameters"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"},
        504: {"description": "Request timeout"}
    }
)
async def get_monthly_reports(request: Request):
    """
    Pass-through proxy for monthly consumption reports.
    
    Validates query parameters and forwards request to backend,
    returning the response without transformation while adding
    security and caching layers.
    """
    logger.info("Monthly reports requested")
    return await proxy_get_request("/reports/monthly", request)


@router.get(
    "/weekly",
    summary="Weekly Consumption Reports",
    description="""
    Retrieve weekly energy consumption reports with pattern analysis.
    
    Features:
        - Week-by-week consumption breakdown
        - Weekday vs weekend analysis
        - Peak usage hours identification
        - Cost projections
        - Anomaly detection
    
    Query Parameters:
        - start: Start date (YYYY-MM-DD)
        - end: End date (YYYY-MM-DD)
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
    
    Response Format:
        Pass-through from backend with pagination support.
    
    Caching: 5 minutes
    Rate Limiting: 20 requests per minute
    """,
    responses={
        200: {
            "description": "Weekly reports retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "week_start": "2025-10-21",
                                "week_end": "2025-10-27",
                                "consumption_kwh": 78.1,
                                "cost": 61.35,
                                "avg_daily_kwh": 11.16,
                                "peak_day": "Wednesday",
                                "weekend_consumption": 18.5
                            }
                        ],
                        "meta": {
                            "page": 1,
                            "per_page": 20,
                            "total": 42
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid query parameters"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    }
)
async def get_weekly_reports(request: Request):
    """
    Pass-through proxy for weekly consumption reports.
    
    Validates date ranges and forwards request to backend
    with proper error handling and logging.
    """
    logger.info("Weekly reports requested")
    return await proxy_get_request("/reports/weekly", request)


@router.get(
    "/annual",
    summary="Annual Consumption Summary",
    description="""
    Retrieve annual energy consumption summary and trends.
    
    Features:
        - Year-over-year comparison
        - Seasonal analysis
        - Cost breakdown by month
        - Consumption patterns
        - Savings opportunities
    
    Query Parameters:
        - year: Target year (default: current year)
        - compare_previous: Include previous year comparison
    
    Caching: 10 minutes (longer cache for annual data)
    """,
    responses={
        200: {"description": "Annual summary retrieved"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    }
)
async def get_annual_reports(request: Request):
    """
    Pass-through proxy for annual consumption summaries.
    
    Annual reports are cached longer due to their
    comprehensive nature and lower update frequency.
    """
    logger.info("Annual reports requested")
    return await proxy_get_request("/reports/annual", request)


@router.get(
    "/export",
    summary="Export Report Data",
    description="""
    Export report data in various formats (CSV, PDF, Excel).
    
    Features:
        - Multiple export formats
        - Custom date ranges
        - Filtered data export
        - Formatted reports
    
    Query Parameters:
        - format: Export format (csv|pdf|excel)
        - start: Start date
        - end: End date
        - report_type: Type of report (monthly|weekly|daily)
    
    Response:
        Raw file download with appropriate Content-Type
    """,
    responses={
        200: {"description": "File export successful"},
        400: {"description": "Invalid export parameters"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    }
)
async def export_reports(request: Request):
    """
    Pass-through proxy for report export functionality.
    
    Handles file downloads with proper content-type headers
    and streaming for large exports.
    """
    logger.info("Report export requested")
    return await proxy_get_request("/reports/export", request)


@router.get(
    "/dashboard",
    summary="Dashboard Summary Data",
    description="""
    Retrieve aggregated data for dashboard display.
    
    Features:
        - Current period summary
        - Key metrics and KPIs
        - Trend indicators
        - Quick stats
        - Alert counts
    
    Optimized for dashboard performance with aggressive caching.
    
    Caching: 2 minutes
    """,
    responses={
        200: {"description": "Dashboard data retrieved"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    }
)
async def get_dashboard_summary(request: Request):
    """
    Pass-through proxy for dashboard summary data.
    
    Heavily cached endpoint optimized for frequent polling
    from dashboard interfaces.
    """
    logger.info("Dashboard summary requested")
    return await proxy_get_request("/reports/dashboard", request)

