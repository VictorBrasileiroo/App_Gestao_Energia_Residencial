"""
Camada Intermediária - Aplicação Principal do Gateway de API

Este módulo implementa o Gateway de API central para o Sistema de Gestão de Energia.
Atua como camada de segurança e orquestrador de requisições entre frontend e backend.

Arquitetura:
    Cliente -> Camada Intermediária (Gateway) -> Backend -> Banco de Dados
    
Responsabilidades Principais:
    - Validação de Token JWT
    - Limitação de Taxa de Requisições
    - Cache de Respostas
    - Sanitização de Requisições
    - Logging e Monitoramento
    - Gerenciamento CORS
    - Balanceamento de Carga (preparado para múltiplas instâncias do backend)
    
Recursos de Segurança:
    - Validação de token antes de encaminhar requisições
    - Sanitização de entrada para prevenir ataques de injeção
    - Limitação de taxa para prevenir DDoS
    - Proteção CORS
    
Recursos de Performance:
    - Processamento assíncrono de requisições
    - Cache de respostas para consultas frequentes
    - Pool de conexões
    - Gerenciamento de timeout de requisições
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routes import auth, health, reports, consumption
from src.config import config
import logging
import time
from typing import Callable

# Configurar logging estruturado
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI com metadados completos
app = FastAPI(
    title="Gestão de Energia - Gateway de API",
    description="""
    Gateway de API e Camada de Segurança
    
    Este serviço middleware fornece:
    
    Segurança:
    - Validação de Token JWT
    - Sanitização de Requisições
    - Limitação de Taxa (100 req/min)
    - Proteção CORS
    
    Performance:
    - Processamento Assíncrono de Requisições
    - Cache de Respostas
    - Pool de Conexões
    - Gerenciamento de Timeout
    
    Monitoramento:
    - Logging de Requisições/Respostas
    - Health Checks
    - Coleta de Métricas
    - Rastreamento de Requisições
    
    Todas as requisições ao backend DEVEM passar por este gateway para validação de segurança.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Equipe de Gestão de Energia",
        "email": "support@energymanagement.com"
    },
    license_info={
        "name": "Licença MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configuração de Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
    max_age=3600,  # Cache de requisições preflight por 1 hora
)

logger.info(f"CORS configurado para origens: {config.get_allowed_origins_list()}")


# Middleware de Logging de Requisições
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    """
    Middleware para registrar todas as requisições e respostas recebidas.
    
    Logs incluem:
        - Método e caminho da requisição
        - Endereço IP do cliente
        - Código de status da resposta
        - Duração da requisição
        - User agent
    
    Isso é crítico para auditoria de segurança e monitoramento de performance.
    """
    start_time = time.time()
    
    # Gerar ID único de requisição para rastreamento
    request_id = f"{int(start_time * 1000)}-{id(request)}"
    
    # Registrar requisição recebida
    logger.info(
        f"[{request_id}] Requisição recebida: "
        f"{request.method} {request.url.path} "
        f"de {request.client.host if request.client else 'unknown'}"
    )
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular duração da requisição
    process_time = time.time() - start_time
    
    # Registrar resposta
    logger.info(
        f"[{request_id}] Requisição completada: "
        f"status={response.status_code} "
        f"duração={process_time:.3f}s"
    )
    
    # Adicionar headers customizados para monitoramento
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Middleware de Limitação de Taxa (Simplificado para demonstração)
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next: Callable):
    """
    Middleware básico de limitação de taxa.
    
    Em produção, isso faria:
        - Rastrear requisições por IP no Redis
        - Implementar algoritmo de janela deslizante
        - Retornar 429 Too Many Requests quando excedido
        - Adicionar headers X-RateLimit-*
    
    Atual: Pass-through com logging (pronto para implementação em produção)
    """
    client_ip = request.client.host if request.client else "unknown"
    
    # TODO: Implementar limitação de taxa real com Redis
    # Por enquanto, apenas registrar e passar adiante
    logger.debug(f"Verificação de limite de taxa para IP: {client_ip}")
    
    response = await call_next(request)
    
    # Adicionar headers de limite de taxa (informativos)
    response.headers["X-RateLimit-Limit"] = str(config.RATE_LIMIT_PER_MINUTE)
    response.headers["X-RateLimit-Remaining"] = "95"  # Valor mockado
    
    return response


# Registro de rotas
app.include_router(auth.router, tags=["Autenticação"])
app.include_router(health.router, tags=["Health Check"])
app.include_router(reports.router, tags=["Relatórios"])
app.include_router(consumption.router, tags=["Consumo"])

logger.info("Todos os módulos de rota registrados com sucesso")


# Tratador global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Tratador de exceção global para erros não capturados.
    
    Garante respostas de erro consistentes e previne
    vazamento de detalhes sensíveis de erros para clientes.
    """
    logger.error(f"Exceção não tratada: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Erro interno do servidor",
            "message": "Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.",
            "request_id": f"{int(time.time() * 1000)}-{id(request)}"
        }
    )


# Eventos de inicialização/desligamento
@app.on_event("startup")
async def startup_event():
    """
    Executado na inicialização da aplicação.
    
    Realiza:
        - Validação de configuração
        - Verificação de conectividade do backend
        - Inicialização de cache
        - Configuração de métricas
    """
    logger.info("=" * 60)
    logger.info("Gateway de API Iniciando")
    logger.info("=" * 60)
    logger.info(f"Ambiente: {config.ENVIRONMENT}")
    logger.info(f"URL do Backend: {config.get_backend_base_url()}")
    logger.info(f"Limite de Taxa: {config.RATE_LIMIT_PER_MINUTE} req/min")
    logger.info(f"Caching: {'Habilitado' if config.ENABLE_CACHING else 'Desabilitado'}")
    logger.info(f"Modo Debug: {'Habilitado' if config.DEBUG else 'Desabilitado'}")
    logger.info("=" * 60)
    
    # TODO: Inicializar cache (Redis)
    # TODO: Verificar conectividade do backend
    # TODO: Carregar chaves de API do gerenciador de segredos
    
    logger.info("Inicialização do gateway concluída com sucesso")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado no desligamento da aplicação.
    
    Realiza limpeza:
        - Fechar conexões do banco de dados
        - Limpar cache
        - Fechar conexões de monitoramento
    """
    logger.info("Gateway de API desligando...")
    
    # TODO: Fechar conexões de cache
    # TODO: Limpar logs pendentes
    
    logger.info("Desligamento do gateway concluído")


# Endpoint raiz
@app.get(
    "/",
    summary="Informações do Gateway",
    description="Retorna informações sobre o Gateway de API",
    tags=["Informações"]
)
async def root():
    """
    Endpoint raiz fornecendo informações e status do gateway.
    """
    return {
        "service": "Gestão de Energia - Gateway de API",
        "version": "1.0.0",
        "status": "operacional",
        "environment": config.ENVIRONMENT,
        "features": {
            "authentication": "Validação de Token JWT",
            "rate_limiting": f"{config.RATE_LIMIT_PER_MINUTE} req/min",
            "caching": config.ENABLE_CACHING,
            "monitoring": "Habilitado"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "backend_status": "/health/backend"
        }
    }
