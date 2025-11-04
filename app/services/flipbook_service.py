from app.services.supabase_service import SupabaseService

class FlipbookService:
    def __init__(self):
        self.db = SupabaseService()
        self.table = 'flipbooks'
    
    def listar_flipbooks(self, activo=None):
        if activo is not None:
            return self.db.client.table(self.table).select("*").eq('activo', activo).execute().data
        return self.db.get_all(self.table)
    
    def obtener_flipbook(self, id):
        return self.db.get_by_id(self.table, id)
    
    def crear_flipbook(self, data):
        # Calcular total de páginas
        if 'paginas' in data:
            data['total_paginas'] = len(data['paginas'])
        return self.db.create(self.table, data)
    
    def actualizar_flipbook(self, id, data):
        # Actualizar total de páginas si se modifican
        if 'paginas' in data:
            data['total_paginas'] = len(data['paginas'])
        return self.db.update(self.table, id, data)
    
    def eliminar_flipbook(self, id):
        return self.db.delete(self.table, id)
    
    def agregar_pagina(self, flipbook_id, pagina_data):
        try:
            # Obtener flipbook actual
            flipbook = self.obtener_flipbook(flipbook_id)
            if not flipbook:
                raise Exception("Flipbook no encontrado")
            
            # Agregar nueva página
            paginas = flipbook.get('paginas', [])
            paginas.append(pagina_data)
            
            # Actualizar flipbook
            return self.actualizar_flipbook(flipbook_id, {
                'paginas': paginas,
                'total_paginas': len(paginas)
            })
        except Exception as e:
            raise Exception(f"Error al agregar página: {str(e)}")
    
    def eliminar_pagina(self, flipbook_id, numero_pagina):
        try:
            # Obtener flipbook actual
            flipbook = self.obtener_flipbook(flipbook_id)
            if not flipbook:
                raise Exception("Flipbook no encontrado")
            
            # Filtrar páginas
            paginas = flipbook.get('paginas', [])
            paginas = [p for p in paginas if p.get('numero') != numero_pagina]
            
            # Reordenar números de página
            for i, pagina in enumerate(paginas, 1):
                pagina['numero'] = i
            
            # Actualizar flipbook
            return self.actualizar_flipbook(flipbook_id, {
                'paginas': paginas,
                'total_paginas': len(paginas)
            })
        except Exception as e:
            raise Exception(f"Error al eliminar página: {str(e)}")
    
    def buscar_por_categoria(self, categoria):
        try:
            response = self.db.client.table(self.table).select("*").eq('categoria', categoria).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al buscar por categoría: {str(e)}") 
