from app.services.supabase_service import SupabaseService

class ServicioService:
    def __init__(self):
        self.db = SupabaseService()
        self.table = 'servicios'
    
    def listar_servicios(self, activo=None):
        if activo is not None:
            return self.db.client.table(self.table).select("*").eq('activo', activo).execute().data
        return self.db.get_all(self.table)
    
    def obtener_servicio(self, id):
        return self.db.get_by_id(self.table, id)
    
    def crear_servicio(self, data):
        return self.db.create(self.table, data)
    
    def actualizar_servicio(self, id, data):
        return self.db.update(self.table, id, data)
    
    def eliminar_servicio(self, id):
        return self.db.delete(self.table, id)
    
    def buscar_por_categoria(self, categoria):
        try:
            response = self.db.client.table(self.table).select("*").eq('categoria', categoria).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al buscar por categoría: {str(e)}") 
