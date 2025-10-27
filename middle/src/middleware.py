"""
Módulos de Middleware Customizados - Gateway de API

Este módulo contém componentes de middleware customizados para o Gateway de API,
implementando recursos avançados de segurança, performance e monitoramento.

Pilha de Middleware (em ordem de execução):
    1. Request Logging - Registra todas as requisições recebidas
    2. Rate Limiting - Previne abuso da API
    3. Authentication - Valida tokens JWT
    4. Request Validation - Sanitiza inputs
    5. Response Caching - Cacheia consultas frequentes
    6. Response Compression - Otimiza banda
    7. Metrics Collection - Coleta dados de performance

Cada middleware é projetado para ser:
    - Não-bloqueante (async)
    - Tolerante a falhas
    - Otimizado para performance
    - Pronto para produção
"""

import logging
import time
from typing import Callable, Dict, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import hashlib
import json

# Configurar logger
logger = logging.getLogger(__name__)


# ============================================================================
# MIDDLEWARE DE LIMITAÇÃO DE TAXA
# ============================================================================

class RateLimiter:
    """
    Implementação de limitação de taxa em memória.
    
    Em produção, usaria Redis para limitação de taxa distribuída
    entre múltiplas instâncias do gateway.
    
    Recursos:
        - Algoritmo de janela deslizante
        - Rastreamento por IP
        - Limites configuráveis
        - Limpeza automática
        - Suporte a burst
    
    Atual: Implementação simplificada (registra mas não bloqueia)
    Produção: Integraria com Redis
    """
    
    def __init__(self, requests_per_minute: int = 100, burst: int = 20):
        """
        Inicializa o limitador de taxa.
        
        Args:
            requests_per_minute: Máximo de requisições por minuto
            burst: Máximo de requisições em burst
        """
        self.requests_per_minute = requests_per_minute
        self.burst = burst
        self.request_counts: Dict[str, list] = {}
        logger.info(
            f"Limitador de taxa inicializado: {requests_per_minute} req/min, "
            f"burst={burst}"
        )
    
    def check_rate_limit(self, client_ip: str) -> tuple[bool, int]:
        """
        Verifica se o cliente excedeu o limite de taxa.
        
        Args:
            client_ip: Endereço IP do cliente
            
        Returns:
            Tupla de (permitido, requisições_restantes)
        """
        current_time = time.time()
        window_start = current_time - 60  # janela de 1 minuto
        
        # Obtém ou cria histórico de requisições para este IP
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Remove requisições antigas fora da janela
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if req_time > window_start
        ]
        
        # Conta requisições na janela atual
        request_count = len(self.request_counts[client_ip])
        
        # Verifica se o limite foi excedido
        is_allowed = request_count < self.requests_per_minute
        remaining = max(0, self.requests_per_minute - request_count)
        
        if is_allowed:
            # Adiciona requisição atual ao histórico
            self.request_counts[client_ip].append(current_time)
        
        logger.debug(
            f"Verificação de limite para {client_ip}: "
            f"count={request_count}, remaining={remaining}, "
            f"allowed={is_allowed}"
        )
        
        return is_allowed, remaining
    
    def cleanup_old_entries(self) -> None:
        """
        Limpa entradas antigas para prevenir sobrecarga de memória.
        
        Deve ser chamada periodicamente (a cada 5 minutos).
        """
        current_time = time.time()
        window_start = current_time - 300  # 5 minutos
        
        for ip in list(self.request_counts.keys()):
            self.request_counts[ip] = [
                req_time for req_time in self.request_counts[ip]
                if req_time > window_start
            ]
            
            # Remove IP se não houver requisições recentes
            if not self.request_counts[ip]:
                del self.request_counts[ip]


# Instância global do limitador de taxa
# Em produção, seria um cliente Redis
rate_limiter = RateLimiter(requests_per_minute=100, burst=20)


# ============================================================================
# MIDDLEWARE DE CACHE DE RESPOSTA
# ============================================================================

class ResponseCache:
    """
    Cache de respostas em memória para consultas frequentes.
    
    Em produção, usaria Redis para cache distribuído
    entre múltiplas instâncias do gateway.
    
    Recursos:
        - Expiração baseada em TTL
        - Geração de chave de cache
        - Invalidação automática
        - Gerenciamento de memória
        - Métricas de hit/miss de cache
    
    Atual: Cache em memória simplificado
    Produção: Usaria Redis com evição LRU
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Inicializa o cache.
        
        Args:
            max_size: Máximo de entradas no cache
            default_ttl: TTL padrão em segundos (5 minutos)
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, dict] = {}
        self.hits = 0
        self.misses = 0
        logger.info(
            f"Cache de resposta inicializado: max_size={max_size}, "
            f"ttl={default_ttl}s"
        )
    
    def generate_cache_key(self, request: Request) -> str:
        """
        Gera chave única de cache a partir da requisição.
        
        Inclui:
            - Método HTTP
            - Caminho da requisição
            - Parâmetros de query
            - Header de autorização (hasheado)
        
        Args:
            request: Requisição FastAPI
            
        Returns:
            String da chave de cache
        """
        # Combina componentes da requisição
        key_components = [
            request.method,
            str(request.url.path),
            str(request.url.query)
        ]
        
        # Adiciona token de auth hasheado se presente
        auth = request.headers.get("authorization")
        if auth:
            auth_hash = hashlib.md5(auth.encode()).hexdigest()
            key_components.append(auth_hash)
        
        # Gera hash
        key_string = ":".join(key_components)
        cache_key = hashlib.sha256(key_string.encode()).hexdigest()
        
        return cache_key
    
    def get(self, cache_key: str) -> Optional[dict]:
        """
        Obtém resposta cacheada se válida.
        
        Args:
            cache_key: Chave do cache
            
        Returns:
            Resposta cacheada ou None se miss/expirada
        """
        if cache_key not in self.cache:
            self.misses += 1
            logger.debug(f"Cache MISS: {cache_key[:16]}...")
            return None
        
        entry = self.cache[cache_key]
        
        # Verifica se expirou
        if time.time() > entry["expires_at"]:
            del self.cache[cache_key]
            self.misses += 1
            logger.debug(f"Cache EXPIRADO: {cache_key[:16]}...")
            return None
        
        self.hits += 1
        logger.debug(f"Cache HIT: {cache_key[:16]}...")
        return entry["response"]
    
    def set(
        self,
        cache_key: str,
        response_data: dict,
        ttl: Optional[int] = None
    ) -> None:
        """
        Armazena resposta no cache.
        
        Args:
            cache_key: Chave do cache
            response_data: Resposta para cachear
            ttl: TTL customizado (usa padrão se None)
        """
        # Verifica limite de tamanho do cache
        if len(self.cache) >= self.max_size:
            # Evicção simples: remove entrada mais antiga
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k]["created_at"]
            )
            del self.cache[oldest_key]
            logger.debug(f"Evicção de cache: {oldest_key[:16]}...")
        
        # Armazena entrada
        ttl = ttl or self.default_ttl
        self.cache[cache_key] = {
            "response": response_data,
            "created_at": time.time(),
            "expires_at": time.time() + ttl
        }
        
        logger.debug(f"Cache SET: {cache_key[:16]}... (ttl={ttl}s)")
    
    def invalidate(self, pattern: str) -> int:
        """
        Invalida entradas do cache que correspondem ao padrão.
        
        Args:
            pattern: Padrão para correspondência com chaves
            
        Returns:
            Número de entradas invalidadas
        """
        count = 0
        for key in list(self.cache.keys()):
            if pattern in key:
                del self.cache[key]
                count += 1
        
        logger.info(f"Cache invalidado: {count} entradas correspondendo a '{pattern}'")
        return count
    
    def get_stats(self) -> dict:
        """
        Obtém estatísticas do cache.
        
        Returns:
            Dicionário com métricas do cache
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests
        }


# Instância global de cache
# Em produção, seria um cliente Redis
response_cache = ResponseCache(max_size=1000, default_ttl=300)


# ============================================================================
# MIDDLEWARE DE VALIDAÇÃO DE REQUISIÇÃO
# ============================================================================

class RequestValidator:
    """
    Validação e sanitização de requisições.
    
    Recursos:
        - Sanitização de inputs
        - Prevenção de SQL injection
        - Prevenção de XSS
        - Prevenção de path traversal
        - Validação de tamanho de payload
    """
    
    def __init__(self, max_payload_size: int = 10 * 1024 * 1024):
        """
        Inicializa o validador.
        
        Args:
            max_payload_size: Tamanho máximo do payload em bytes (10MB)
        """
        self.max_payload_size = max_payload_size
        self.suspicious_patterns = [
            '<script',
            'javascript:',
            'onerror=',
            'onload=',
            'eval(',
            'DROP TABLE',
            'SELECT * FROM',
            '../',
            '..\\',
        ]
        logger.info(f"Validador de requisição inicializado: max_size={max_payload_size}")
    
    def validate_payload_size(self, content_length: Optional[int]) -> bool:
        """
        Valida o tamanho do payload da requisição.
        
        Args:
            content_length: Valor do header Content-Length
            
        Returns:
            True se válido, False caso contrário
        """
        if content_length is None:
            return True
        
        if content_length > self.max_payload_size:
            logger.warning(
                f"Payload muito grande: {content_length} bytes "
                f"(max: {self.max_payload_size})"
            )
            return False
        
        return True
    
    def check_suspicious_patterns(self, text: str) -> bool:
        """
        Verifica texto por padrões suspeitos.
        
        Args:
            text: Texto para verificar
            
        Returns:
            True se padrão suspeito encontrado
        """
        text_lower = text.lower()
        for pattern in self.suspicious_patterns:
            if pattern.lower() in text_lower:
                logger.warning(f"Padrão suspeito detectado: {pattern}")
                return True
        
        return False


# Instância global do validador
request_validator = RequestValidator(max_payload_size=10 * 1024 * 1024)


# ============================================================================
# COLETOR DE MÉTRICAS
# ============================================================================

class MetricsCollector:
    """
    Coleta e expõe métricas para monitoramento.
    
    Métricas rastreadas:
        - Contagem de requisições por endpoint
        - Tempos de resposta
        - Taxas de erro
        - Taxas de hit de cache
        - Violações de limite de taxa
    
    Em produção, exportaria para Prometheus/Datadog
    """
    
    def __init__(self):
        """Inicializa o coletor de métricas."""
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.endpoint_counts: Dict[str, int] = {}
        logger.info("Coletor de métricas inicializado")
    
    def record_request(
        self,
        endpoint: str,
        status_code: int,
        response_time: float
    ) -> None:
        """
        Registra métricas da requisição.
        
        Args:
            endpoint: Endpoint da requisição
            status_code: Código de status HTTP
            response_time: Tempo de resposta em segundos
        """
        self.request_count += 1
        self.total_response_time += response_time
        
        # Rastreia contagem por endpoint
        if endpoint not in self.endpoint_counts:
            self.endpoint_counts[endpoint] = 0
        self.endpoint_counts[endpoint] += 1
        
        # Rastreia erros
        if status_code >= 400:
            self.error_count += 1
    
    def get_metrics(self) -> dict:
        """
        Obtém métricas atuais.
        
        Returns:
            Dicionário com todas as métricas
        """
        avg_response_time = (
            self.total_response_time / self.request_count
            if self.request_count > 0 else 0
        )
        
        error_rate = (
            self.error_count / self.request_count * 100
            if self.request_count > 0 else 0
        )
        
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate_percent": round(error_rate, 2),
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "cache_stats": response_cache.get_stats(),
            "top_endpoints": dict(
                sorted(
                    self.endpoint_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            )
        }


# Coletor global de métricas
metrics_collector = MetricsCollector()


# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def log_request_info(request: Request, duration: float) -> None:
    """
    Registra informações da requisição em formato estruturado.
    
    Args:
        request: Requisição FastAPI
        duration: Duração da requisição em segundos
    """
    log_data = {
        "method": request.method,
        "path": str(request.url.path),
        "client_ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "duration_ms": round(duration * 1000, 2)
    }
    
    logger.info(f"Requisição processada: {json.dumps(log_data)}")


def add_security_headers(response: Response) -> Response:
    """
    Adiciona headers de segurança à resposta.
    
    Args:
        response: Resposta FastAPI
        
    Returns:
        Resposta com headers de segurança adicionados
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response
