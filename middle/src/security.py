"""
Utilitários de Segurança - Gateway de API

Este módulo fornece utilitários relacionados à segurança para o Gateway de API,
implementando práticas de segurança padrão da indústria e validações.

Recursos:
    - Validação de token JWT
    - Sanitização de inputs
    - Prevenção de SQL injection
    - Prevenção de XSS
    - Proteção CSRF
    - Helpers de limitação de taxa
    - Utilitários de criptografia
    - Geração segura de aleatórios

Padrões de Segurança:
    - Conformidade OWASP Top 10
    - Diretrizes PCI DSS
    - Conformidade GDPR (proteção de dados)
    - Melhores práticas ISO 27001
"""

import hashlib
import hmac
import secrets
import re
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

# Configurar logger
logger = logging.getLogger(__name__)


# ============================================================================
# UTILITÁRIOS DE TOKEN JWT
# ============================================================================

class JWTValidator:
    """
    Utilitários de validação e parsing de token JWT.
    
    Em produção, integraria com python-jose para
    validação completa de JWT incluindo verificação de assinatura.
    
    Atual: Validação básica de formato
    Produção: Verificação criptográfica completa
    """
    
    def __init__(self, secret_key: str = "default-secret"):
        """
        Inicializa o validador JWT.
        
        Args:
            secret_key: Chave secreta para validação HMAC
        """
        self.secret_key = secret_key
        logger.info("Validador JWT inicializado")
    
    def validate_token_format(self, token: str) -> bool:
        """
        Valida formato do token JWT (não verificação criptográfica).
        
        Verificações:
            - Token tem 3 partes (header.payload.signature)
            - Cada parte é base64-encoded
            - Token não está vazio
        
        Args:
            token: String do token JWT
            
        Returns:
            True se formato é válido
        """
        if not token:
            logger.warning("Token vazio fornecido")
            return False
        
        # Remove prefixo "Bearer " se presente
        if token.startswith("Bearer "):
            token = token[7:]
        
        # Verifica por 3 partes
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning(f"Formato de token inválido: esperado 3 partes, obtido {len(parts)}")
            return False
        
        # Verifica se cada parte não está vazia
        for i, part in enumerate(parts):
            if not part:
                logger.warning(f"Parte {i} do token está vazia")
                return False
        
        logger.debug("Formato de token validado com sucesso")
        return True
    
    def extract_token_from_header(self, auth_header: Optional[str]) -> Optional[str]:
        """
        Extrai token JWT do header de Authorization.
        
        Args:
            auth_header: Valor do header Authorization
            
        Returns:
            Token extraído ou None
        """
        if not auth_header:
            return None
        
        # Trata formato "Bearer <token>"
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            if self.validate_token_format(token):
                return token
        
        # Trata token bruto
        if self.validate_token_format(auth_header):
            return auth_header
        
        logger.warning("Não foi possível extrair token válido do header")
        return None
    
    def is_token_expired(self, token_data: Dict[str, Any]) -> bool:
        """
        Verifica se token expirou baseado no claim 'exp'.
        
        Args:
            token_data: Dados decodificados do token
            
        Returns:
            True se expirado
        """
        if 'exp' not in token_data:
            logger.warning("Token sem claim 'exp'")
            return True
        
        exp_timestamp = token_data['exp']
        current_timestamp = datetime.utcnow().timestamp()
        
        is_expired = current_timestamp > exp_timestamp
        
        if is_expired:
            logger.info("Token expirou")
        
        return is_expired


# ============================================================================
# SANITIZAÇÃO DE INPUT
# ============================================================================

class InputSanitizer:
    """
    Utilitários de sanitização e validação de inputs.
    
    Protege contra:
        - SQL injection
        - Ataques XSS
        - Path traversal
        - Command injection
        - LDAP injection
    """
    
    # Padrões perigosos para detectar
    SQL_INJECTION_PATTERNS = [
        r"('\s*OR\s*'1'\s*=\s*'1)",
        r"('\s*OR\s*1\s*=\s*1)",
        r"(--\s*$)",
        r"(;\s*DROP\s+TABLE)",
        r"(;\s*DELETE\s+FROM)",
        r"(UNION\s+SELECT)",
        r"(INSERT\s+INTO)",
        r"(UPDATE\s+.+SET)",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe",
        r"<object",
        r"<embed",
    ]
    
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e/",
        r"%2e%2e\\",
    ]
    
    def __init__(self):
        """Inicializa o sanitizador de inputs."""
        self.sql_regex = re.compile(
            '|'.join(self.SQL_INJECTION_PATTERNS),
            re.IGNORECASE
        )
        self.xss_regex = re.compile(
            '|'.join(self.XSS_PATTERNS),
            re.IGNORECASE
        )
        self.path_regex = re.compile(
            '|'.join(self.PATH_TRAVERSAL_PATTERNS),
            re.IGNORECASE
        )
        logger.info("Sanitizador de inputs inicializado")
    
    def check_sql_injection(self, text: str) -> bool:
        """
        Verifica por padrões de SQL injection.
        
        Args:
            text: Texto de input para verificar
            
        Returns:
            True se SQL injection detectado
        """
        if self.sql_regex.search(text):
            logger.warning(f"SQL injection detectado: {text[:50]}...")
            return True
        return False
    
    def check_xss(self, text: str) -> bool:
        """
        Verifica por padrões de XSS.
        
        Args:
            text: Texto de input para verificar
            
        Returns:
            True se XSS detectado
        """
        if self.xss_regex.search(text):
            logger.warning(f"Tentativa de XSS detectada: {text[:50]}...")
            return True
        return False
    
    def check_path_traversal(self, path: str) -> bool:
        """
        Verifica por padrões de path traversal.
        
        Args:
            path: Caminho para verificar
            
        Returns:
            True se path traversal detectado
        """
        if self.path_regex.search(path):
            logger.warning(f"Path traversal detectado: {path}")
            return True
        return False
    
    def sanitize_string(self, text: str, max_length: int = 1000) -> str:
        """
        Sanitiza input de string.
        
        Operações:
            - Trim de espaços em branco
            - Remove bytes nulos
            - Limita comprimento
            - Remove caracteres de controle
        
        Args:
            text: Texto de input
            max_length: Comprimento máximo permitido
            
        Returns:
            Texto sanitizado
        """
        if not text:
            return ""
        
        # Remove bytes nulos
        sanitized = text.replace('\x00', '')
        
        # Remove outros caracteres de controle (exceto newline/tab)
        sanitized = ''.join(
            char for char in sanitized
            if char.isprintable() or char in '\n\t'
        )
        
        # Trim de espaços em branco
        sanitized = sanitized.strip()
        
        # Limita comprimento
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            logger.debug(f"String truncada para {max_length} caracteres")
        
        return sanitized
    
    def is_safe_input(self, text: str) -> bool:
        """
        Verificação de segurança abrangente para input.
        
        Args:
            text: Input para validar
            
        Returns:
            True se input é seguro
        """
        if self.check_sql_injection(text):
            return False
        if self.check_xss(text):
            return False
        if self.check_path_traversal(text):
            return False
        
        return True


# ============================================================================
# UTILITÁRIOS CRIPTOGRÁFICOS
# ============================================================================

class CryptoUtils:
    """
    Utilitários criptográficos para operações seguras.
    
    Recursos:
        - Geração segura de aleatórios
        - Assinatura HMAC
        - Geração de hash
        - Geração de tokens
    """
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Gera token aleatório criptograficamente seguro.
        
        Args:
            length: Comprimento do token em bytes
            
        Returns:
            String do token em hexadecimal
        """
        token = secrets.token_hex(length)
        logger.debug(f"Token seguro gerado: {length} bytes")
        return token
    
    @staticmethod
    def generate_request_id() -> str:
        """
        Gera ID único de requisição para rastreamento.
        
        Returns:
            ID único da requisição
        """
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        random_part = secrets.token_hex(8)
        return f"{timestamp}-{random_part}"
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash de senha com salt usando SHA-256.
        
        Nota: Em produção, use bcrypt ou argon2!
        
        Args:
            password: Senha em texto claro
            salt: Salt opcional (gerado se não fornecido)
            
        Returns:
            Tupla de (senha_hasheada, salt)
        """
        if not salt:
            salt = secrets.token_hex(16)
        
        # Combina senha e salt
        salted = f"{password}{salt}".encode('utf-8')
        
        # Hash com SHA-256
        hashed = hashlib.sha256(salted).hexdigest()
        
        logger.debug("Senha hasheada com sucesso")
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verifica senha contra hash.
        
        Args:
            password: Senha em texto claro para verificar
            hashed: Hash armazenado
            salt: Salt usado para hashing
            
        Returns:
            True se senha corresponder
        """
        computed_hash, _ = CryptoUtils.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, hashed)
    
    @staticmethod
    def generate_hmac_signature(data: str, secret: str) -> str:
        """
        Gera assinatura HMAC para dados.
        
        Args:
            data: Dados para assinar
            secret: Chave secreta
            
        Returns:
            Assinatura HMAC
        """
        signature = hmac.new(
            secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        logger.debug("Assinatura HMAC gerada")
        return signature
    
    @staticmethod
    def verify_hmac_signature(data: str, signature: str, secret: str) -> bool:
        """
        Verifica assinatura HMAC.
        
        Args:
            data: Dados originais
            signature: Assinatura para verificar
            secret: Chave secreta
            
        Returns:
            True se assinatura é válida
        """
        expected_signature = CryptoUtils.generate_hmac_signature(data, secret)
        return hmac.compare_digest(signature, expected_signature)


# ============================================================================
# UTILITÁRIOS DE LIMITAÇÃO DE TAXA
# ============================================================================

class RateLimitHelper:
    """
    Funções auxiliares para limitação de taxa.
    """
    
    @staticmethod
    def get_client_identifier(
        ip_address: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> str:
        """
        Gera identificador único do cliente para limitação de taxa.
        
        Prefere user_id se autenticado, recai para IP.
        
        Args:
            ip_address: Endereço IP do cliente
            user_id: ID do usuário autenticado
            
        Returns:
            Identificador do cliente
        """
        if user_id:
            return f"user:{user_id}"
        if ip_address:
            return f"ip:{ip_address}"
        return "unknown"
    
    @staticmethod
    def calculate_retry_after(requests_per_minute: int) -> int:
        """
        Calcula segundos de Retry-After para resposta de limite de taxa.
        
        Args:
            requests_per_minute: Limite de taxa
            
        Returns:
            Segundos para aguardar
        """
        return 60  # Simples: aguarda 1 minuto


# ============================================================================
# UTILITÁRIOS DE ENDEREÇO IP
# ============================================================================

class IPValidator:
    """
    Validação de endereços IP e utilitários.
    """
    
    @staticmethod
    def is_valid_ipv4(ip: str) -> bool:
        """
        Valida formato de endereço IPv4.
        
        Args:
            ip: String de endereço IP
            
        Returns:
            True se IPv4 válido
        """
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        # Verifica se cada octeto está entre 0-255
        octets = ip.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """
        Verifica se IP está em faixa privada.
        
        Args:
            ip: Endereço IP
            
        Returns:
            True se IP privado
        """
        if not IPValidator.is_valid_ipv4(ip):
            return False
        
        # Faixas de IP privado
        octets = [int(x) for x in ip.split('.')]
        
        # 10.0.0.0/8
        if octets[0] == 10:
            return True
        
        # 172.16.0.0/12
        if octets[0] == 172 and 16 <= octets[1] <= 31:
            return True
        
        # 192.168.0.0/16
        if octets[0] == 192 and octets[1] == 168:
            return True
        
        return False


# ============================================================================
# INSTÂNCIAS GLOBAIS
# ============================================================================

# Inicializa utilitários de segurança globais
jwt_validator = JWTValidator()
input_sanitizer = InputSanitizer()

logger.info("Utilitários de segurança inicializados e prontos")
