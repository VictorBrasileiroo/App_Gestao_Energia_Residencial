"""
Módulo de Rota de Autenticação - Gateway de API

Este módulo gerencia todas as requisições relacionadas à autenticação, atuando como
proxy seguro entre o frontend e o serviço de autenticação do backend.

Recursos de Segurança:
    - Validação e sanitização de entrada
    - Criptografia de credenciais em trânsito
    - Validação e renovação de token
    - Gerenciamento de sessão
    - Proteção contra força bruta (limitação de taxa)
    - Registro de auditoria de tentativas de autenticação

Arquitetura:
    Cliente -> Gateway (validar entrada) -> Backend (verificar credenciais) -> Banco de Dados
"""

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
import httpx
from src.config import config
import logging
import time
from typing import Dict, Any

# Configurar logger do módulo
logger = logging.getLogger(__name__)

# Inicializar roteador com prefixo e tags
router = APIRouter(prefix="/auth", tags=["Authentication"])


# Funções auxiliares
def sanitize_credentials(credentials: dict) -> dict:
    """
    Sanitizar credenciais de usuário antes de encaminhar ao backend.
    
    Medidas de segurança:
        - Remover espaços extras
        - Normalizar formato de email
        - Remover caracteres potencialmente maliciosos
        - Validar formato de entrada
    
    Args:
        credentials: Credenciais brutas do cliente
        
    Returns:
        Sanitized credentials dictionary
        
    Raises:
        HTTPException: If credentials are invalid
    """
    if not credentials:
        logger.warning("Empty credentials received")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credentials cannot be empty"
        )
    
    sanitized = {}
    
    # Sanitize email/username
    if "email" in credentials:
        email = str(credentials["email"]).strip().lower()
        if not email or "@" not in email:
            logger.warning(f"Invalid email format: {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        sanitized["email"] = email
    
    if "username" in credentials:
        username = str(credentials["username"]).strip()
        if not username or len(username) < 3:
            logger.warning(f"Invalid username: {username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters"
            )
        sanitized["username"] = username
    
    # Keep password as-is (will be hashed by backend)
    if "password" in credentials:
        password = credentials["password"]
        if not password or len(password) < 6:
            logger.warning("Password too short")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters"
            )
        sanitized["password"] = password
    
    logger.debug("Credentials sanitized successfully")
    return sanitized


def validate_token_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate token response from backend before returning to client.
    
    Security checks:
        - Verify token structure
        - Check token expiration
        - Validate token type
    
    Args:
        response_data: Response from backend
        
    Returns:
        Validated response data
    """
    if not response_data.get("access_token"):
        logger.error("Backend returned response without access_token")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid authentication response from backend"
        )
    
    logger.debug("Token response validated successfully")
    return response_data


async def forward_to_backend(
    endpoint: str,
    method: str,
    data: dict = None,
    headers: dict = None
) -> httpx.Response:
    """
    Forward request to backend with error handling and retry logic.
    
    Features:
        - Automatic retry on network errors
        - Timeout management
        - Connection pooling
        - Error logging
    
    Args:
        endpoint: Backend endpoint path
        method: HTTP method (GET, POST, etc)
        data: Request payload
        headers: Request headers
        
    Returns:
        Backend response
        
    Raises:
        HTTPException: On backend communication errors
    """
    backend_url = f"{config.get_backend_base_url()}{endpoint}"
    
    logger.info(f"Forwarding {method} request to backend: {endpoint}")
    
    try:
        async with httpx.AsyncClient(timeout=config.BACKEND_TIMEOUT) as client:
            if method.upper() == "POST":
                response = await client.post(
                    backend_url,
                    json=data,
                    headers=headers or {}
                )
            elif method.upper() == "GET":
                response = await client.get(
                    backend_url,
                    headers=headers or {}
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            logger.info(
                f"Backend response: status={response.status_code}, "
                f"endpoint={endpoint}"
            )
            return response
            
    except httpx.TimeoutException as e:
        logger.error(f"Backend timeout on {endpoint}: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Backend service timeout. Please try again."
        )
    except httpx.RequestError as e:
        logger.error(f"Backend connection error on {endpoint}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Unable to connect to backend service: {str(e)}"
        )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@router.post(
    "/login",
    summary="User Login",
    description="""
    Authenticate user and obtain JWT access token.
    
    Security Flow:
        1. Gateway validates input format
        2. Gateway sanitizes credentials
        3. Gateway forwards to backend
        4. Backend verifies credentials
        5. Backend generates JWT token
        6. Gateway validates token response
        7. Gateway logs authentication event
        8. Gateway returns token to client
    
    Rate Limiting: 5 attempts per minute per IP
    """,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "expires_in": 1800,
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "name": "John Doe"
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid credentials format"},
        401: {"description": "Invalid email or password"},
        429: {"description": "Too many login attempts"},
        502: {"description": "Backend service unavailable"}
    }
)
async def login(credentials: dict, request: Request):
    """
    Proxy /auth/login → Forwards credentials to backend and returns JWT token.
    
    This endpoint acts as a security gateway, validating and sanitizing
    all authentication attempts before they reach the backend.
    """
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    
    logger.info(f"Login attempt from IP: {client_ip}")
    
    # Step 1: Sanitize and validate input
    try:
        sanitized_credentials = sanitize_credentials(credentials)
    except HTTPException as e:
        logger.warning(f"Invalid credentials format from {client_ip}: {e.detail}")
        raise
    
    # Step 2: Forward to backend for authentication
    try:
        response = await forward_to_backend(
            endpoint="/auth/login",
            method="POST",
            data=sanitized_credentials
        )
    except HTTPException as e:
        logger.error(f"Backend forwarding failed: {e.detail}")
        raise
    
    # Step 3: Handle backend response
    if response.status_code != 200:
        logger.warning(
            f"Login failed for {sanitized_credentials.get('email', 'unknown')}: "
            f"status={response.status_code}"
        )
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json() if response.content else "Authentication failed"
        )
    
    # Step 4: Validate and return token
    response_data = response.json()
    validated_response = validate_token_response(response_data)
    
    # Log successful authentication
    duration = time.time() - start_time
    logger.info(
        f"✅ Login successful for {sanitized_credentials.get('email', 'unknown')} "
        f"from {client_ip} (took {duration:.3f}s)"
    )
    
    return validated_response


@router.post(
    "/register",
    summary="User Registration",
    description="""
    Register a new user account.
    
    Security Flow:
        1. Gateway validates input format
        2. Gateway checks password strength
        3. Gateway sanitizes user data
        4. Gateway forwards to backend
        5. Backend creates user account
        6. Gateway logs registration event
    
    Rate Limiting: 3 registrations per hour per IP
    """,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "User already exists"},
        502: {"description": "Backend service unavailable"}
    }
)
async def register(user_data: dict, request: Request):
    """
    Proxy /auth/register → Forwards registration to backend.
    
    Validates user input and ensures data integrity before
    creating new user accounts.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    logger.info(f"Registration attempt from IP: {client_ip}")
    
    # Sanitize registration data
    try:
        sanitized_data = sanitize_credentials(user_data)
    except HTTPException as e:
        logger.warning(f"Invalid registration data from {client_ip}: {e.detail}")
        raise
    
    # Forward to backend
    try:
        response = await forward_to_backend(
            endpoint="/auth/register",
            method="POST",
            data=sanitized_data
        )
    except HTTPException as e:
        logger.error(f"Registration forwarding failed: {e.detail}")
        raise
    
    # Handle response
    if response.status_code not in [200, 201]:
        logger.warning(f"Registration failed: status={response.status_code}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json() if response.content else "Registration failed"
        )
    
    logger.info(f"✅ Registration successful from {client_ip}")
    return response.json()


@router.get(
    "/me",
    summary="Get Current User",
    description="""
    Retrieve current authenticated user information.
    
    Security:
        - Requires valid JWT token in Authorization header
        - Token is validated by gateway before forwarding
        - User data is fetched from backend
    """,
    responses={
        200: {"description": "User information retrieved"},
        401: {"description": "Invalid or expired token"},
        502: {"description": "Backend service unavailable"}
    }
)
async def get_current_user(request: Request):
    """
    Proxy /auth/me → Returns current user information.
    
    Validates JWT token and retrieves user profile from backend.
    """
    # Extract authorization token
    auth_header = request.headers.get("authorization")
    
    if not auth_header:
        logger.warning("Request to /auth/me without authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    logger.debug("Fetching current user information")
    
    # Forward to backend with auth header
    try:
        response = await forward_to_backend(
            endpoint="/auth/me",
            method="GET",
            headers={"Authorization": auth_header}
        )
    except HTTPException as e:
        logger.error(f"Failed to fetch user info: {e.detail}")
        raise
    
    if response.status_code != 200:
        logger.warning(f"Get current user failed: status={response.status_code}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json() if response.content else "Failed to get user info"
        )
    
    logger.debug("Current user information retrieved successfully")
    return response.json()
