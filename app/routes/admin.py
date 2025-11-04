from flask import Blueprint, request
from app.services.supabase_service import SupabaseAuthService
from app.utils.responses import (
    success_response, 
    error_response, 
    unauthorized_response
)
from app.utils.validators import validate_email, validate_required_fields

admin_bp = Blueprint('admin', __name__)
auth_service = SupabaseAuthService()

@admin_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión del administrador
    Body: { "email": "admin@example.com", "password": "password123" }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        is_valid, error_msg = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            return error_response(error_msg, 400)
        
        email = data.get('email')
        password = data.get('password')
        
        # Validar formato de email
        if not validate_email(email):
            return error_response("Formato de email inválido", 400)
        
        # Intentar autenticar
        result = auth_service.sign_in(email, password)
        
        return success_response({
            'user': {
                'id': result['user'].id,
                'email': result['user'].email,
                'created_at': str(result['user'].created_at)
            },
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }, "Inicio de sesión exitoso", 200)
        
    except Exception as e:
        error_message = str(e)
        if "Invalid login credentials" in error_message or "autenticación" in error_message.lower():
            return unauthorized_response("Credenciales inválidas")
        return error_response(f"Error al iniciar sesión: {error_message}", 500)


@admin_bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint para cerrar sesión
    Headers: Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return unauthorized_response("Token no proporcionado")
        
        token = auth_header.split(' ')[1]
        auth_service.sign_out(token)
        
        return success_response(None, "Sesión cerrada exitosamente", 200)
        
    except Exception as e:
        return error_response(f"Error al cerrar sesión: {str(e)}", 500)


@admin_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Endpoint para obtener información del usuario actual
    Headers: Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return unauthorized_response("Token no proporcionado")
        
        token = auth_header.split(' ')[1]
        user = auth_service.get_user(token)
        
        if not user:
            return unauthorized_response("Token inválido o expirado")
        
        return success_response({
            'id': user.id,
            'email': user.email,
            'created_at': str(user.created_at)
        }, "Usuario obtenido exitosamente", 200)
        
    except Exception as e:
        return error_response(f"Error al obtener usuario: {str(e)}", 500)


@admin_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Endpoint para refrescar el token de acceso
    Body: { "refresh_token": "..." }
    """
    try:
        data = request.get_json()
        
        if not data or 'refresh_token' not in data:
            return error_response("Refresh token no proporcionado", 400)
        
        result = auth_service.refresh_session(data['refresh_token'])
        
        return success_response({
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }, "Token refrescado exitosamente", 200)
        
    except Exception as e:
        return error_response(f"Error al refrescar token: {str(e)}", 500)


@admin_bp.route('/verify', methods=['POST'])
def verify_token():
    """
    Endpoint para verificar si un token es válido
    Headers: Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response("Token no proporcionado", 400)
        
        token = auth_header.split(' ')[1]
        is_valid = auth_service.verify_token(token)
        
        if is_valid:
            return success_response({'valid': True}, "Token válido", 200)
        else:
            return unauthorized_response("Token inválido o expirado")
        
    except Exception as e:
        return error_response(f"Error al verificar token: {str(e)}", 500) 
