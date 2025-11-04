from app.extensions import get_supabase_client
from typing import Optional, Dict, Any
from gotrue.errors import AuthApiError

class SupabaseAuthService:
    """Servicio para autenticación con Supabase"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Inicia sesión con email y contraseña
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            return {
                'user': response.user,
                'session': response.session,
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token
            }
        except AuthApiError as e:
            raise Exception(f"Error de autenticación: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al iniciar sesión: {str(e)}")
    
    def sign_out(self, access_token: str) -> bool:
        """
        Cierra la sesión del usuario
        """
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            raise Exception(f"Error al cerrar sesión: {str(e)}")
    
    def get_user(self, access_token: str) -> Optional[Dict]:
        """
        Obtiene el usuario actual usando el token de acceso
        """
        try:
            response = self.client.auth.get_user(access_token)
            return response.user
        except Exception as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")
    
    def refresh_session(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresca la sesión usando el refresh token
        """
        try:
            response = self.client.auth.refresh_session(refresh_token)
            return {
                'session': response.session,
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token
            }
        except Exception as e:
            raise Exception(f"Error al refrescar sesión: {str(e)}")
    
    def verify_token(self, access_token: str) -> bool:
        """
        Verifica si un token es válido
        """
        try:
            user = self.get_user(access_token)
            return user is not None
        except:
            return False


class SupabaseService:
    """Servicio genérico para operaciones CRUD con Supabase"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    def get_all(self, table: str, filters: Optional[Dict] = None, order_by: Optional[str] = None):
        """Obtiene todos los registros de una tabla"""
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            if order_by:
                query = query.order(order_by)
            
            response = query.execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener datos de {table}: {str(e)}")
    
    def get_by_id(self, table: str, id: int):
        """Obtiene un registro por ID"""
        try:
            response = self.client.table(table).select("*").eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al obtener registro de {table}: {str(e)}")
    
    def create(self, table: str, data: Dict):
        """Crea un nuevo registro"""
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear registro en {table}: {str(e)}")
    
    def update(self, table: str, id: int, data: Dict):
        """Actualiza un registro existente"""
        try:
            response = self.client.table(table).update(data).eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar registro en {table}: {str(e)}")
    
    def delete(self, table: str, id: int):
        """Elimina un registro"""
        try:
            self.client.table(table).delete().eq('id', id).execute()
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar registro de {table}: {str(e)}")