from supabase import create_client
import os

_supabase_client = None

def get_supabase_client(service_role: bool = False):
    """
    Retorna una instancia del cliente de Supabase.
    Usa la service_role key si se solicita (para operaciones seguras del backend).
    """
    global _supabase_client
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = (
            os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
            if service_role
            else os.environ.get("SUPABASE_ANON_KEY")
        )
        _supabase_client = create_client(url, key)
    return _supabase_client
