# app/routes/contacto.py
from flask import Blueprint, request, jsonify
from app.utils.responses import success_response, error_response
from app.utils.validators import validate_email, validate_required_fields
from app.services.email_service import enviar_email_contacto, enviar_email_confirmacion
from app.services.supabase_service import SupabaseService

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
        
        # 1. Guardar en base de datos (opcional pero recomendado)
        try:
            db = SupabaseService()
            mensaje_guardado = db.create('mensajes_contacto', {
                'nombre': data['nombre'],
                'email': data['email'],
                'telefono': data['telefono'],
                'mensaje': data['mensaje'],
                'estado': 'pendiente'
            })
        except Exception as db_error:
            print(f"Error al guardar en BD: {str(db_error)}")
            # Continuar aunque falle el guardado en BD
        
        # 2. Enviar email de notificación a la empresa
        try:
            enviar_email_contacto(data)
        except Exception as email_error:
            print(f"Error al enviar email de notificación: {str(email_error)}")
            # Si falla el email, igual retornamos éxito (ya se guardó en BD)
        
        # 3. Enviar email de confirmación al cliente (opcional)
        try:
            enviar_email_confirmacion(data['email'], data['nombre'])
        except Exception as conf_error:
            print(f"Error al enviar confirmación: {str(conf_error)}")
            # No es crítico si falla
        
        return success_response({
            'mensaje': 'Contacto recibido',
            'datos': {
                'nombre': data['nombre'],
                'email': data['email']
            }
        }, "Mensaje enviado exitosamente. Te responderemos pronto.", 201)
        
    except Exception as e:
        return error_response(f"Error al procesar mensaje: {str(e)}", 500)