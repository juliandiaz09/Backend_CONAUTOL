from flask import Flask, request, make_response
from flask_cors import CORS
from app.config import Config
from app.routes import register_routes
from app.services.email_service import init_mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_mail(app)

    # --- Normaliza origins permitidos ---
    # FRONTEND_URL puede venir con barra final; Origin NO trae path.
    # Además, en dev aceptamos tanto localhost como 127.0.0.1 (mismo puerto).
    frontend_cfg = (app.config.get('FRONTEND_URL') or 'http://localhost:4200').rstrip('/')
    allowed_origins = {
        frontend_cfg,
        'http://localhost:4200',
        'http://127.0.0.1:4200',
        'https://juliandiaz09.github.io',
    }

    # --- CORS para /api/* ---
    # - allow_headers incluye Authorization y Content-Type (preflight)
    # - max_age cachea la preflight
    # - NO usamos credentials a menos que realmente uses cookies de sesión
    CORS(
        app,
        resources={r"/api/*": {
            "origins": list(allowed_origins),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
            "expose_headers": ["Content-Disposition"],
            "supports_credentials": False,
            "max_age": 86400,
        }},
    )

    # --- Garantiza respuesta 204 a preflight en /api/* (por si algún proxy interfiere) ---
    @app.before_request
    def _cors_preflight():
        if request.method == "OPTIONS" and request.path.startswith("/api/"):
            # Flask-CORS suele manejarlo, pero respondemos explícitamente 204 por robustez
            return make_response(("", 204))

    # (Opcional) refuerza Vary/Origin en todas las respuestas /api/*
    @app.after_request
    def _add_vary_origin(resp):
        if request.path.startswith("/api/"):
            # Útil cuando hay varios origins permitidos
            resp.headers.add("Vary", "Origin")
        return resp

    # Registrar rutas después de configurar CORS
    register_routes(app)
    return app
