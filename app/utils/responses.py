from flask import jsonify
from typing import Any, Dict, Optional

def success_response(data: Any = None, message: str = "Operación exitosa", status_code: int = 200):
    """Respuesta exitosa estándar"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message: str, status_code: int = 400, errors: Optional[Dict] = None):
    """Respuesta de error estándar"""
    response = {
        'success': False,
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code

def unauthorized_response(message: str = "No autorizado"):
    """Respuesta de no autorizado"""
    return error_response(message, 401)

def forbidden_response(message: str = "Acceso prohibido"):
    """Respuesta de acceso prohibido"""
    return error_response(message, 403)

def not_found_response(message: str = "Recurso no encontrado"):
    """Respuesta de recurso no encontrado"""
    return error_response(message, 404)

def server_error_response(message: str = "Error interno del servidor"):
    """Respuesta de error del servidor"""
    return error_response(message, 500) 
