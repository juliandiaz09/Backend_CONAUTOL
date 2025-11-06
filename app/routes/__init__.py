from app.routes.proyectos import proyectos_bp
from app.routes.servicios import servicios_bp
from app.routes.admin import admin_bp

def register_routes(app):
    app.register_blueprint(proyectos_bp, url_prefix='/api/proyectos')
    app.register_blueprint(servicios_bp, url_prefix='/api/servicios')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
