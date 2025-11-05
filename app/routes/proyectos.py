from flask import Blueprint, request, jsonify
from app.services.proyecto_service import ProyectoService
from app.services.supabase_service import SupabaseStorageService
from app.utils.decorators import token_required
import json

proyectos_bp = Blueprint('proyectos', __name__)
proyecto_service = ProyectoService()
storage_service = SupabaseStorageService()

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
@token_required
def crear_proyecto():
    try:
        data_str = request.form.get('data')
        if not data_str:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        data = json.loads(data_str)
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            imagen_url = storage_service.upload_file(file, 'proyectos')
            data['imagen_url'] = imagen_url

        proyecto = proyecto_service.crear_proyecto(data)
        return jsonify(proyecto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['PUT'])
@token_required
def actualizar_proyecto(id):
    try:
        data_str = request.form.get('data')
        if not data_str:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
            
        data = json.loads(data_str)
        
        proyecto_existente = proyecto_service.obtener_proyecto(id)
        if not proyecto_existente:
            return jsonify({'error': 'Proyecto no encontrado'}), 404

        if 'imagen' in request.files:
            file = request.files['imagen']
            imagen_url = storage_service.update_file(proyecto_existente.get('imagen_url'), file, 'proyectos')
            data['imagen_url'] = imagen_url

        proyecto = proyecto_service.actualizar_proyecto(id, data)
        return jsonify(proyecto), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def eliminar_proyecto(id):
    try:
        proyecto_existente = proyecto_service.obtener_proyecto(id)
        if not proyecto_existente:
            return jsonify({'error': 'Proyecto no encontrado'}), 404

        # Eliminar la imagen si existe
        if proyecto_existente.get('imagen_url'):
            storage_service.delete_file(proyecto_existente['imagen_url'])

        proyecto_service.eliminar_proyecto(id)
        return jsonify({'message': 'Proyecto eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
