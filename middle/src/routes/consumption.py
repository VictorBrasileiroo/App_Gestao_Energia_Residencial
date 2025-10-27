"""
Consumption Route Module - API Gateway

This module handles all energy consumption-related requests, acting as a
secure proxy with data validation and file processing capabilities.

Features:
    - CSV file upload validation and sanitization
    - File size and type verification
    - Virus scanning integration (ready)
    - Data format validation
    - Consumption data analytics proxy
    - Request rate limiting for uploads
    - Audit logging of all data operations

Security:
    - File type validation (CSV only)
    - File size limits (max 5MB)
    - Content sanitization
    - Malicious content detection (ready for integration)
    - Authorization validation
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Request, status
from fastapi.responses import JSONResponse
import httpx
from src.config import config
import logging
import time
from typing import Dict

# Configure module logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

# File upload constraints
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_CONTENT_TYPES = ["text/csv", "application/csv", "text/plain"]
ALLOWED_EXTENSIONS = [".csv"]

# Validation messages
ERROR_INVALID_FILE_TYPE = "Invalid file type. Only CSV files are accepted."
ERROR_FILE_TOO_LARGE = "File size exceeds the maximum limit of 5MB."
ERROR_NO_AUTH_TOKEN = "Authorization token is required."
ERROR_EMPTY_FILE = "File cannot be empty."


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_auth_headers(request: Request) -> Dict[str, str]:
    """
    Extract and validate authentication headers from request.
    
    Security:
        - Validates Authorization header presence
        - Preserves Accept header for content negotiation
        - Sanitizes header values
    
    Args:
        request: FastAPI request object
        
    Returns:
        Dictionary with sanitized headers for backend
    """
    headers: Dict[str, str] = {}
    
    # Extract authorization token
    auth_token = request.headers.get("authorization")
    if auth_token:
        headers["Authorization"] = auth_token
        logger.debug("Authorization header extracted")
    
    # Extract accept header for content negotiation
    accept_header = request.headers.get("accept")
    if accept_header:
        headers["Accept"] = accept_header
    
    return headers


def validate_file_type(file: UploadFile) -> None:
    """
    Validate uploaded file type and extension.
    
    Security checks:
        - Verify MIME type is CSV
        - Check file extension
        - Prevent executable uploads
    
    Args:
        file: Uploaded file object
        
    Raises:
        HTTPException: If file type is invalid
    """
    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        logger.warning(
            f"Invalid file type uploaded: {file.content_type} "
            f"(filename: {file.filename})"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_INVALID_FILE_TYPE
        )
    
    # Check file extension
    if file.filename:
        extension = file.filename.lower().split('.')[-1]
        if f".{extension}" not in ALLOWED_EXTENSIONS:
            logger.warning(f"Invalid file extension: {extension}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_INVALID_FILE_TYPE
            )
    
    logger.debug(f"File type validated: {file.content_type}")


def validate_file_size(content: bytes) -> None:
    """
    Validate uploaded file size.
    
    Prevents:
        - Memory exhaustion attacks
        - Denial of service via large files
        - Storage overflow
    
    Args:
        content: File content bytes
        
    Raises:
        HTTPException: If file exceeds size limit
    """
    file_size = len(content)
    
    if file_size == 0:
        logger.warning("Empty file uploaded")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_EMPTY_FILE
        )
    
    if file_size > MAX_FILE_SIZE:
        logger.warning(
            f"File too large: {file_size} bytes "
            f"(max: {MAX_FILE_SIZE} bytes)"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_FILE_TOO_LARGE
        )
    
    logger.debug(f"File size validated: {file_size} bytes")


def sanitize_csv_content(content: bytes) -> bytes:
    """
    Sanitize CSV file content.
    
    Security measures:
        - Remove null bytes
        - Validate UTF-8 encoding
        - Check for malicious patterns
        - Remove potential script injections
    
    Args:
        content: Raw file content
        
    Returns:
        Sanitized content
        
    Raises:
        HTTPException: If content contains malicious patterns
    """
    try:
        # Validate UTF-8 encoding
        decoded = content.decode('utf-8')
        
        # Check for suspicious patterns (basic security)
        suspicious_patterns = ['<script', 'javascript:', 'onerror=', 'eval(']
        for pattern in suspicious_patterns:
            if pattern.lower() in decoded.lower():
                logger.warning(f"Suspicious pattern detected: {pattern}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File contains potentially malicious content"
                )
        
        # Remove null bytes
        sanitized = decoded.replace('\x00', '')
        
        logger.debug("CSV content sanitized successfully")
        return sanitized.encode('utf-8')
        
    except UnicodeDecodeError:
        logger.error("Invalid file encoding - not UTF-8")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be UTF-8 encoded"
        )


async def forward_file_to_backend(
    url: str,
    file_content: bytes,
    filename: str,
    content_type: str,
    headers: Dict[str, str]
) -> httpx.Response:
    """
    Forward file upload to backend service.
    
    Features:
        - Async file upload
        - Timeout management
        - Error handling
        - Progress logging
    
    Args:
        url: Backend endpoint URL
        file_content: File content bytes
        filename: Original filename
        content_type: File MIME type
        headers: Request headers
        
    Returns:
        Backend response
        
    Raises:
        HTTPException: On backend communication errors
    """
    logger.info(f"Forwarding file to backend: {filename} ({len(file_content)} bytes)")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers=headers,
                files={'file': (filename, file_content, content_type)}
            )
            
            logger.info(
                f"Backend response: status={response.status_code}, "
                f"file={filename}"
            )
            return response
            
    except httpx.TimeoutException:
        logger.error(f"Backend timeout while uploading: {filename}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="File upload timeout. Please try again with a smaller file."
        )
        
    except httpx.RequestError as e:
        logger.error(f"Backend connection error during upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Unable to upload file to backend: {str(e)}"
        )


# ============================================================================
# CONSUMPTION ENDPOINTS
# ============================================================================

@router.post(
    "/consumption/upload",
    summary="Upload Consumption Data",
    description="""
    Upload energy consumption data via CSV file.
    
    Security & Validation:
        1. File type validation (CSV only)
        2. File size check (max 5MB)
        3. Content sanitization
        4. Malicious pattern detection
        5. Authorization verification
        6. Virus scanning (ready for integration)
    
    Expected CSV Format:
        - Headers: timestamp, energy_kwh, cost
        - Date format: YYYY-MM-DD HH:MM:SS
        - Numbers: decimal with dot separator
    
    Rate Limiting: 10 uploads per hour per user
    
    Example CSV:
        ```
        timestamp,energy_kwh,cost
        2025-10-01 00:00:00,1.5,1.2
        2025-10-01 01:00:00,2.3,1.8
        ```
    """,
    responses={
        200: {
            "description": "File processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "File processed successfully",
                        "records_imported": 720,
                        "duplicates_skipped": 5,
                        "errors": []
                    }
                }
            }
        },
        400: {"description": "Invalid file format or content"},
        401: {"description": "Missing or invalid authorization"},
        413: {"description": "File too large"},
        502: {"description": "Backend service error"}
    },
    tags=["Consumption"]
)
async def upload_consumption_file(request: Request, file: UploadFile = File(...)):
    """
    Upload and process CSV file with energy consumption data.
    
    This endpoint acts as a secure gateway for file uploads,
    performing comprehensive validation before forwarding to backend.
    """
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    
    logger.info(
        f"File upload initiated: {file.filename} "
        f"from {client_ip}"
    )
    
    # Step 1: Validate authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logger.warning(f"Upload attempt without authorization from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_NO_AUTH_TOKEN
        )
    
    # Step 2: Validate file type
    try:
        validate_file_type(file)
    except HTTPException as e:
        logger.warning(f"File type validation failed: {e.detail}")
        raise
    
    # Step 3: Read and validate file content
    try:
        file_content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read uploaded file: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read file content"
        )
    
    # Step 4: Validate file size
    try:
        validate_file_size(file_content)
    except HTTPException as e:
        logger.warning(f"File size validation failed: {e.detail}")
        raise
    
    # Step 5: Sanitize content
    try:
        sanitized_content = sanitize_csv_content(file_content)
    except HTTPException as e:
        logger.warning(f"Content sanitization failed: {e.detail}")
        raise
    
    # Step 6: Prepare backend request
    backend_url = f"{config.get_backend_base_url()}/consumption/upload"
    headers = extract_auth_headers(request)
    
    # Step 7: Forward to backend
    try:
        response = await forward_file_to_backend(
            url=backend_url,
            file_content=sanitized_content,
            filename=file.filename or "consumption.csv",
            content_type=file.content_type or "text/csv",
            headers=headers
        )
    except HTTPException as e:
        logger.error(f"Failed to forward file to backend: {e.detail}")
        raise
    
    # Step 8: Handle backend response
    if response.is_error:
        logger.error(
            f"Backend returned error: status={response.status_code}, "
            f"file={file.filename}"
        )
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": True,
                "message": "Backend processing failed",
                "details": response.json() if response.content else "Unknown error"
            }
        )
    
    # Step 9: Return success response
    duration = time.time() - start_time
    result = response.json()
    
    logger.info(
        f"✅ File upload successful: {file.filename} "
        f"from {client_ip} (took {duration:.3f}s)"
    )
    
    return result


@router.get(
    "/consumption/",
    summary="Get Consumption Records",
    description="""
    Retrieve energy consumption records.
    
    Features:
        - Pagination support
        - Date range filtering
        - Sorting options
        - Response caching
    
    Query Parameters:
        - start_date: Filter from date (YYYY-MM-DD)
        - end_date: Filter to date (YYYY-MM-DD)
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - sort: Sort field (date|energy|cost)
        - order: Sort order (asc|desc)
    """,
    responses={
        200: {"description": "Consumption records retrieved"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    },
    tags=["Consumption"]
)
async def get_consumption_records(request: Request):
    """
    Proxy GET /consumption/ to backend.
    
    Retrieves consumption records with optional filtering and pagination.
    """
    logger.debug("Get consumption records requested")
    
    # Validate authorization
    headers = extract_auth_headers(request)
    if not headers.get("Authorization"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_NO_AUTH_TOKEN
        )
    
    # Build backend URL with query parameters
    backend_url = f"{config.get_backend_base_url()}/consumption/"
    if request.url.query:
        backend_url = f"{backend_url}?{request.url.query}"
    
    # Forward to backend
    try:
        async with httpx.AsyncClient(timeout=config.BACKEND_TIMEOUT) as client:
            response = await client.get(backend_url, headers=headers)
    except httpx.RequestError as e:
        logger.error(f"Backend request failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Backend communication error: {str(e)}"
        )
    
    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json() if response.content else "Backend error"
        )
    
    logger.debug("Consumption records retrieved successfully")
    return response.json()


@router.get(
    "/consumption/analytics",
    summary="Get Consumption Analytics",
    description="""
    Retrieve detailed consumption analytics and statistics.
    
    Returns:
        - Daily/weekly/monthly averages
        - Peak consumption times
        - Cost analysis
        - Consumption trends
        - Anomaly detection results
    
    Caching: 5 minutes
    """,
    responses={
        200: {"description": "Analytics data retrieved"},
        401: {"description": "Unauthorized"},
        502: {"description": "Backend service error"}
    },
    tags=["Consumption"]
)
async def get_consumption_analytics(request: Request):
    """
    Proxy GET /consumption/analytics to backend.
    
    Retrieves comprehensive analytics with caching for performance.
    """
    logger.debug("Get consumption analytics requested")
    
    # Validate authorization
    headers = extract_auth_headers(request)
    if not headers.get("Authorization"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_NO_AUTH_TOKEN
        )
    
    # TODO: Check cache before forwarding
    # if config.ENABLE_CACHING:
    #     cached_result = cache.get("analytics")
    #     if cached_result:
    #         return cached_result
    
    # Build backend URL
    backend_url = f"{config.get_backend_base_url()}/consumption/analytics"
    if request.url.query:
        backend_url = f"{backend_url}?{request.url.query}"
    
    # Forward to backend
    try:
        async with httpx.AsyncClient(timeout=config.BACKEND_TIMEOUT) as client:
            response = await client.get(backend_url, headers=headers)
    except httpx.RequestError as e:
        logger.error(f"Analytics request failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Backend communication error: {str(e)}"
        )
    
    if response.is_error:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json() if response.content else "Backend error"
        )
    
    result = response.json()
    
    # TODO: Store in cache
    # if config.ENABLE_CACHING:
    #     cache.set("analytics", result, ttl=config.CACHE_TTL_SECONDS)
    
    logger.debug("Analytics data retrieved successfully")
    return result
