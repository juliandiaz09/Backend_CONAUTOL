from flask import Blueprint, request, jsonify
from app.services.chatbot_service import ChatbotService
from app.models.chatbot import MensajeCreate, ChatbotConfigUpdate
import uuid

chatbot_bp = Blueprint('chatbot', __name__)
chatbot_service = ChatbotService()

@chatbot_bp.route('/mensaje', methods=['POST'])
def enviar_mensaje():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje')
        session_id = data.get('session_id')
        
        if not mensaje:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        # Generar session_id si no existe
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Procesar mensaje
        respuesta = chatbot_service.procesar_mensaje(mensaje, session_id)
        
        return jsonify({
            'respuesta': respuesta,
            'session_id': session_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/historial/<string:session_id>', methods=['GET'])
def obtener_historial(session_id):
    try:
        limit = request.args.get('limit', 50, type=int)
        historial = chatbot_service.obtener_historial(session_id, limit)
        return jsonify(historial), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/configuracion', methods=['GET'])
def obtener_configuracion():
    try:
        config = chatbot_service.obtener_configuracion()
        if config:
            return jsonify(config), 200
        return jsonify({'error': 'Configuración no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/configuracion/<int:id>', methods=['PUT'])
def actualizar_configuracion(id):
    try:
        data = request.get_json()
        config_data = ChatbotConfigUpdate(**data)
        update_data = {k: v for k, v in config_data.model_dump().items() if v is not None}
        config = chatbot_service.actualizar_configuracion(id, update_data)
        return jsonify(config), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 
