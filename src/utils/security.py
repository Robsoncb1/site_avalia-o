"""
Módulo de segurança para o site Coco Bambu Alphaville
Implementa funções de segurança para proteção contra ataques comuns
"""

import re
import hashlib
import bleach
from functools import wraps
from flask import request, abort, session, redirect, url_for

# Lista de caracteres especiais permitidos em entradas de texto
ALLOWED_SPECIAL_CHARS = r'@._\-\s\'\",!?()[]{}:;/+=#*&%$'

def sanitize_input(text):
    """
    Sanitiza entrada de texto para prevenir XSS
    
    Args:
        text (str): Texto a ser sanitizado
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ""
        
    # Usar bleach para sanitizar HTML
    allowed_tags = []  # Não permitir nenhuma tag HTML
    allowed_attrs = {}
    
    sanitized = bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    
    return sanitized

def validate_email(email):
    """
    Valida formato de e-mail
    
    Args:
        email (str): E-mail a ser validado
        
    Returns:
        bool: True se o e-mail for válido, False caso contrário
    """
    if not email:
        return False
        
    # Padrão de validação de e-mail
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))

def validate_rating(rating):
    """
    Valida avaliação (1-5)
    
    Args:
        rating (int): Avaliação a ser validada
        
    Returns:
        bool: True se a avaliação for válida, False caso contrário
    """
    try:
        rating_int = int(rating)
        return 1 <= rating_int <= 5
    except (ValueError, TypeError):
        return False

def validate_text_length(text, min_length=0, max_length=None):
    """
    Valida comprimento de texto
    
    Args:
        text (str): Texto a ser validado
        min_length (int): Comprimento mínimo
        max_length (int): Comprimento máximo
        
    Returns:
        bool: True se o texto tiver comprimento válido, False caso contrário
    """
    if text is None:
        text = ""
        
    text_length = len(text)
    
    if min_length > 0 and text_length < min_length:
        return False
        
    if max_length and text_length > max_length:
        return False
        
    return True

def validate_phone(phone):
    """
    Valida formato de telefone brasileiro
    
    Args:
        phone (str): Telefone a ser validado
        
    Returns:
        bool: True se o telefone for válido, False caso contrário
    """
    if not phone:
        return True  # Telefone é opcional
        
    # Remove caracteres não numéricos
    phone_digits = re.sub(r'\D', '', phone)
    
    # Verifica se tem entre 10 e 11 dígitos (com ou sem DDD)
    if len(phone_digits) < 10 or len(phone_digits) > 11:
        return False
        
    return True

def check_csrf_token(token):
    """
    Verifica token CSRF
    
    Args:
        token (str): Token CSRF a ser verificado
        
    Returns:
        bool: True se o token for válido, False caso contrário
    """
    if not token or not session.get('csrf_token'):
        return False
        
    return token == session.get('csrf_token')

def generate_csrf_token():
    """
    Gera token CSRF
    
    Returns:
        str: Token CSRF gerado
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha256(os.urandom(64)).hexdigest()
        
    return session['csrf_token']

def require_csrf_token(f):
    """
    Decorador para exigir token CSRF em rotas POST
    
    Args:
        f (function): Função a ser decorada
        
    Returns:
        function: Função decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = request.form.get('csrf_token')
            if not check_csrf_token(token):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def is_spam(text):
    """
    Verifica se o texto parece ser spam
    
    Args:
        text (str): Texto a ser verificado
        
    Returns:
        bool: True se o texto parecer spam, False caso contrário
    """
    if not text:
        return False
        
    # Lista de palavras-chave comuns em spam
    spam_keywords = [
        'viagra', 'cialis', 'casino', 'lottery', 'winner', 'prize', 
        'free money', 'earn money', 'make money', 'bitcoin', 'investment',
        'http://', 'https://', 'www.', '.com', '.net', '.org', '.info',
        'click here', 'buy now', 'limited time', 'act now', 'hurry'
    ]
    
    # Converter para minúsculas para comparação
    text_lower = text.lower()
    
    # Verificar presença de palavras-chave de spam
    for keyword in spam_keywords:
        if keyword in text_lower:
            return True
            
    # Verificar excesso de URLs
    url_count = len(re.findall(r'https?://\S+', text))
    if url_count > 2:
        return True
        
    # Verificar excesso de caracteres maiúsculos (gritar)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    if uppercase_ratio > 0.5 and len(text) > 20:
        return True
        
    return False

def rate_limit_check(ip_address, action_type, limit=10, period=60):
    """
    Verifica limite de taxa para prevenir ataques de força bruta
    
    Args:
        ip_address (str): Endereço IP do cliente
        action_type (str): Tipo de ação (ex: 'login', 'avaliacao', 'contato')
        limit (int): Número máximo de ações permitidas no período
        period (int): Período em segundos
        
    Returns:
        bool: True se o limite não foi excedido, False caso contrário
    """
    # Implementação simplificada - em produção, usar Redis ou similar
    # para armazenar contadores de taxa por IP
    
    # Nesta implementação de exemplo, sempre retorna True
    # Em um ambiente real, implementar controle de taxa adequado
    return True

def validate_form_data(form_data, required_fields, field_validators=None):
    """
    Valida dados de formulário
    
    Args:
        form_data (dict): Dados do formulário
        required_fields (list): Lista de campos obrigatórios
        field_validators (dict): Dicionário de validadores específicos por campo
        
    Returns:
        tuple: (is_valid, errors) onde is_valid é um booleano e errors é um dicionário de erros
    """
    errors = {}
    
    # Verificar campos obrigatórios
    for field in required_fields:
        if field not in form_data or not form_data[field]:
            errors[field] = f"O campo {field} é obrigatório."
    
    # Aplicar validadores específicos
    if field_validators:
        for field, validator in field_validators.items():
            if field in form_data and form_data[field]:
                is_valid, error_msg = validator(form_data[field])
                if not is_valid:
                    errors[field] = error_msg
    
    return len(errors) == 0, errors
