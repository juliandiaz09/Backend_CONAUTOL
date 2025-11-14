# app/services/email_service.py
from flask import render_template_string
from flask_mail import Mail, Message
import os

mail = Mail()

def init_mail(app):
    """Inicializar Flask-Mail con la configuración del app"""
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail.init_app(app)
    return mail

def enviar_email_contacto(datos):
    """
    Envía email de notificación cuando alguien llena el formulario de contacto
    
    Args:
        datos (dict): Diccionario con nombre, email, telefono, mensaje
    """
    try:
        destinatario = os.getenv('MAIL_RECIPIENT', 'ing.conautol@gmail.com')
        
        # Crear mensaje
        msg = Message(
            subject=f'Nuevo mensaje de contacto - {datos["nombre"]}',
            recipients=[destinatario],
            reply_to=datos['email']
        )
        
        # Cuerpo del email en HTML
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .field {{
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #eee;
                }}
                .field-label {{
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 5px;
                }}
                .field-value {{
                    color: #555;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #999;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Nuevo Mensaje de Contacto</h2>
                    <p>CONAUTOL - Sitio Web</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="field-label">👤 Nombre:</div>
                        <div class="field-value">{datos['nombre']}</div>
                    </div>
                    
                    <div class="field">
                        <div class="field-label">📧 Email:</div>
                        <div class="field-value">{datos['email']}</div>
                    </div>
                    
                    <div class="field">
                        <div class="field-label">📱 Teléfono:</div>
                        <div class="field-value">{datos['telefono']}</div>
                    </div>
                    
                    <div class="field">
                        <div class="field-label">💬 Mensaje:</div>
                        <div class="field-value" style="white-space: pre-wrap;">{datos['mensaje']}</div>
                    </div>
                    
                    <p style="margin-top: 30px; padding: 15px; background-color: #f0f0f0; border-radius: 5px;">
                        <strong>💡 Tip:</strong> Puedes responder directamente a este email para contactar al cliente.
                    </p>
                </div>
                <div class="footer">
                    Este mensaje fue enviado desde el formulario de contacto de www.conautol.com.co
                </div>
            </div>
        </body>
        </html>
        """
        
        # Versión texto plano (fallback)
        msg.body = f"""
        Nuevo mensaje de contacto - CONAUTOL
        
        Nombre: {datos['nombre']}
        Email: {datos['email']}
        Teléfono: {datos['telefono']}
        
        Mensaje:
        {datos['mensaje']}
        
        ---
        Este mensaje fue enviado desde www.conautol.com.co
        """
        
        # Enviar
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        raise Exception(f"Error al enviar email: {str(e)}")


def enviar_email_confirmacion(email_destino, nombre):
    """
    Envía email de confirmación al cliente que llenó el formulario
    
    Args:
        email_destino (str): Email del cliente
        nombre (str): Nombre del cliente
    """
    try:
        msg = Message(
            subject='Hemos recibido tu mensaje - CONAUTOL',
            recipients=[email_destino]
        )
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border: 1px solid #ddd;
                    border-top: none;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Gracias por contactarnos!</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{nombre}</strong>,</p>
                    
                    <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo lo antes posible.</p>
                    
                    <p>Nuestro equipo revisará tu solicitud y te responderá en un plazo máximo de 24-48 horas hábiles.</p>
                    
                    <p>Mientras tanto, si tienes alguna pregunta urgente, no dudes en llamarnos al:</p>
                    <p style="text-align: center; font-size: 18px; color: #667eea;">
                        <strong>📱 +57 3227150837</strong>
                    </p>
                    
                    <p style="margin-top: 30px;">
                        <strong>Saludos cordiales,</strong><br>
                        Equipo CONAUTOL<br>
                        Ingeniería Electromecánica
                    </p>
                    
                    <div style="text-align: center;">
                        <a href="https://www.conautol.com.co" class="button">Visitar nuestro sitio web</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.body = f"""
        Hola {nombre},
        
        Hemos recibido tu mensaje y nos pondremos en contacto contigo lo antes posible.
        
        Nuestro equipo revisará tu solicitud y te responderá en un plazo máximo de 24-48 horas hábiles.
        
        Si tienes alguna pregunta urgente, llámanos al +57 3227150837
        
        Saludos cordiales,
        Equipo CONAUTOL
        Ingeniería Electromecánica
        
        www.conautol.com.co
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error al enviar email de confirmación: {str(e)}")
        # No lanzamos excepción aquí porque el email de confirmación es secundario
        return False