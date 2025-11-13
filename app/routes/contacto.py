# app/routes/contacto.py
from flask import Blueprint, request, jsonify
from app.utils.responses import success_response, error_response
from app.utils.validators import validate_email, validate_required_fields

contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/', methods=['POST'])
def enviar_contacto():
    """
    Endpoint para recibir mensajes de contacto
    Body: { "nombre": "...", "email": "...", "telefono": "...", "mensaje": "..." }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        is_valid, error_msg = validate_required_fields(
            data, 
            ['nombre', 'email', 'telefono', 'mensaje']
        )
        if not is_valid:
            return error_response(error_msg, 400)
        
        # Validar formato de email
        if not validate_email(data['email']):
            return error_response("Formato de email inválido", 400)
        
        # Aquí puedes:
        # 1. Guardar en base de datos
        # 2. Enviar email de notificación
        # 3. Integrar con un CRM
        
        # Por ahora solo retornamos éxito
        return success_response({
            'mensaje': 'Contacto recibido',
            'datos': {
                'nombre': data['nombre'],
                'email': data['email']
            }
        }, "Mensaje enviado exitosamente", 201)
        
    except Exception as e:
        return error_response(f"Error al procesar mensaje: {str(e)}", 500)