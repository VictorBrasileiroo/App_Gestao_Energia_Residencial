"""
Módulo de Configuração - Camada Intermediária (Gateway de API)

Este módulo gerencia toda a configuração do Gateway de API,
incluindo variáveis de ambiente, configurações de segurança e descoberta de serviços.

Funcionalidades:
    - Configuração baseada em ambiente
    - Gerenciamento seguro de credenciais
    - Resolução dinâmica de URL do backend
    - Configuração de limitação de taxa
    - Políticas de cache
    - Configurações de monitoramento e logging

Segurança:
    Todas as credenciais sensíveis são carregadas de variáveis de ambiente
    e nunca codificadas diretamente no código fonte.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import logging

# Configurar logging para o módulo de configuração
logger = logging.getLogger(__name__)


class Config(BaseSettings):
    """
    Configurações do Gateway
    
    Esta classe gerencia todos os parâmetros de configuração do Gateway de API,
    garantindo segurança de tipo e validação através do Pydantic.
    
    Atributos:
        BACKEND_URL: URL do serviço backend interno
        API_KEY: Chave de API opcional para autenticação no backend
        ENVIRONMENT: Ambiente de deployment (development/staging/production)
        SECRET_KEY: Chave secreta JWT para validação de token
        RATE_LIMIT_PER_MINUTE: Máximo de requisições por minuto por IP
        ENABLE_CACHING: Habilitar/desabilitar cache de resposta
        CACHE_TTL_SECONDS: Tempo de vida do cache em segundos
        LOG_LEVEL: Nível de verbosidade do logging
        ALLOWED_ORIGINS: Origens permitidas pelo CORS
    """
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Configuração do Serviço Backend
    BACKEND_URL: str
    
    # Configuração de Segurança
    API_KEY: Optional[str] = None
    SECRET_KEY: Optional[str] = "default-secret-key-change-in-production"
    
    # Configuração de Ambiente
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Configuração de Limitação de Taxa
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_BURST: int = 20
    
    # Configuração de Cache
    ENABLE_CACHING: bool = True
    CACHE_TTL_SECONDS: int = 300  # 5 minutos padrão
    CACHE_MAX_SIZE: int = 1000
    
    # Configuração de Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Configuração de CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Configuração de Timeouts
    BACKEND_TIMEOUT: int = 30
    REQUEST_TIMEOUT: int = 60
    
    # Validação de Requisição
    MAX_REQUEST_SIZE: int = 10485760  # 10MB
    ENABLE_REQUEST_VALIDATION: bool = True
    SANITIZE_INPUTS: bool = True
    
    def get_allowed_origins_list(self) -> list[str]:
        """
        Converte string ALLOWED_ORIGINS em lista de origens.
        
        Returns:
            Lista de URLs de origem permitidas para configuração CORS
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    def is_production(self) -> bool:
        """Verifica se está rodando em ambiente de produção."""
        return self.ENVIRONMENT.lower() == "production"
    
    def is_development(self) -> bool:
        """Verifica se está rodando em ambiente de desenvolvimento."""
        return self.ENVIRONMENT.lower() == "development"
    
    def get_backend_base_url(self) -> str:
        """
        Obtém URL do backend normalizada sem barra final.
        
        Returns:
            URL do backend normalizada
        """
        return self.BACKEND_URL.rstrip("/")


# Inicializar instância global de configuração
config = Config()

# Registrar configuração na inicialização (ocultar dados sensíveis)
logger.info(
    f"Configuração do Gateway Carregada: "
    f"Environment={config.ENVIRONMENT}, "
    f"Backend={config.get_backend_base_url()}, "
    f"RateLimit={config.RATE_LIMIT_PER_MINUTE}/min, "
    f"Caching={'Habilitado' if config.ENABLE_CACHING else 'Desabilitado'}"
)
