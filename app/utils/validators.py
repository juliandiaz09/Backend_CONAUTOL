import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Valida formato de teléfono (colombiano)"""
    # Acepta: +57 3001234567, 3001234567, (300) 1234567
    pattern = r'^(\+57)?[\s\-]?(\(?\d{3}\)?[\s\-]?)?\d{7}$'
    return bool(re.match(pattern, phone.replace(' ', '')))

def validate_url(url: str) -> bool:
    """Valida formato de URL"""
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return bool(re.match(pattern, url))

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Valida extensión de archivo"""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions

def validate_file_size(file_size: int, max_size_mb: int = 5) -> bool:
    """Valida tamaño de archivo en MB"""
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes

def validate_password_strength(password: str) -> dict:
    """Valida fortaleza de contraseña"""
    errors = []
    
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    if not re.search(r'[A-Z]', password):
        errors.append("Debe contener al menos una mayúscula")
    if not re.search(r'[a-z]', password):
        errors.append("Debe contener al menos una minúscula")
    if not re.search(r'[0-9]', password):
        errors.append("Debe contener al menos un número")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Debe contener al menos un carácter especial")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, Optional[str]]:
    """
    Valida que todos los campos requeridos estén presentes y no estén vacíos
    Returns:
        tuple: (is_valid, error_message)
    """
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"El campo '{field}' es requerido"
    return True, None

def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, Optional[str]]:
    """Valida que los campos requeridos estén presentes y no estén vacíos."""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"El campo '{field}' es requerido y no puede estar vacío."
    return True, None
