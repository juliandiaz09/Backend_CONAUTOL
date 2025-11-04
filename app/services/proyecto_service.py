from app.services.supabase_service import SupabaseService

class ProyectoService:
    def __init__(self):
        self.db = SupabaseService()
        self.table = 'proyectos'
    
    def listar_proyectos(self):
        return self.db.get_all(self.table)
    
    def obtener_proyecto(self, id):
        return self.db.get_by_id(self.table, id)
    
    def crear_proyecto(self, data):
        return self.db.create(self.table, data)
    
    def actualizar_proyecto(self, id, data):
        return self.db.update(self.table, id, data)
    
    def eliminar_proyecto(self, id):
        return self.db.delete(self.table, id) 
