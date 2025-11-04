from app.services.supabase_service import SupabaseService
from datetime import datetime

class ChatbotService:
    def __init__(self):
        self.db = SupabaseService()
        self.table_mensajes = 'chatbot_mensajes'
        self.table_config = 'chatbot_config'
    
    def guardar_mensaje(self, data):
        return self.db.create(self.table_mensajes, data)
    
    def obtener_historial(self, session_id, limit=50):
        try:
            response = (self.db.client.table(self.table_mensajes)
                       .select("*")
                       .eq('session_id', session_id)
                       .order('created_at', desc=True)
                       .limit(limit)
                       .execute())
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener historial: {str(e)}")
    
    def obtener_configuracion(self):
        try:
            response = (self.db.client.table(self.table_config)
                       .select("*")
                       .eq('activo', True)
                       .limit(1)
                       .execute())
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al obtener configuración: {str(e)}")
    
    def actualizar_configuracion(self, id, data):
        return self.db.update(self.table_config, id, data)
    
    def procesar_mensaje(self, mensaje, session_id):
        # Guardar mensaje del usuario
        self.guardar_mensaje({
            'contenido': mensaje,
            'tipo': 'usuario',
            'session_id': session_id,
            'created_at': datetime.now().isoformat()
        })
        
        # Obtener configuración
        config = self.obtener_configuracion()
        
        # Buscar respuesta predefinida
        respuesta = "Lo siento, no entiendo tu pregunta."
        if config and config.get('respuestas_predefinidas'):
            respuestas = config['respuestas_predefinidas']
            mensaje_lower = mensaje.lower()
            
            for key, value in respuestas.items():
                if key.lower() in mensaje_lower:
                    respuesta = value
                    break
        
        # Guardar respuesta del bot
        bot_mensaje = self.guardar_mensaje({
            'contenido': respuesta,
            'tipo': 'bot',
            'session_id': session_id,
            'created_at': datetime.now().isoformat()
        })
        
        return bot_mensaje 
