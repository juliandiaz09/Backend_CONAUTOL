from functools import wraps
from flask import request
from app.services.supabase_service import SupabaseAuthService
from app.utils.responses import unauthorized_response

auth_service = SupabaseAuthService()

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return unauthorized_response("Token no proporcionado o en formato incorrecto")
        
        token = auth_header.split(' ')[1]
        
        try:
            is_valid = auth_service.verify_token(token)
            if not is_valid:
                return unauthorized_response("Token inválido o expirado")
        except Exception as e:
            return unauthorized_response(f"Error al verificar el token: {str(e)}")
            
        return f(*args, **kwargs)
    return decorated_function
