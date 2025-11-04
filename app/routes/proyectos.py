from flask import Blueprint, request, jsonify
from app.services.proyecto_service import ProyectoService

proyectos_bp = Blueprint('proyectos', __name__)
proyecto_service = ProyectoService()

@proyectos_bp.route('/', methods=['GET'])
def listar_proyectos():
    try:
        proyectos = proyecto_service.listar_proyectos()
        return jsonify(proyectos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['GET'])
def obtener_proyecto(id):
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if proyecto:
            return jsonify(proyecto), 200
        return jsonify({'error': 'Proyecto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/', methods=['POST'])
def crear_proyecto():
    try:
        data = request.get_json()
        proyecto = proyecto_service.crear_proyecto(data)
        return jsonify(proyecto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_proyecto(id):
    try:
        data = request.get_json()
        proyecto = proyecto_service.actualizar_proyecto(id, data)
        return jsonify(proyecto), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_proyecto(id):
    try:
        proyecto_service.eliminar_proyecto(id)
        return jsonify({'message': 'Proyecto eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

