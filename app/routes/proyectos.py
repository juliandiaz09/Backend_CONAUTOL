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

        # (opcional) valida contra tu schema
        # ProyectoCreate(**data)

        # imagen opcional
        file = request.files.get('imagen')
        if file:
            imagen_url = storage_service.upload_file(file, 'proyectos')
            data['imagen_url'] = imagen_url

        creado = proyecto_service.crear_proyecto(data)
        return jsonify(creado), 201

    except Exception as e:
        # usar 400 para errores de validación/entrada (consistente con servicios)
        return jsonify({'error': str(e)}), 400


@proyectos_bp.route('/<int:id>', methods=['PUT'])
@token_required
def actualizar_proyecto(id):
    try:
        data_str = request.form.get('data')
        if not data_str:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        data = json.loads(data_str)

        existente = proyecto_service.obtener_proyecto(id)
        if not existente:
            return jsonify({'error': 'Proyecto no encontrado'}), 404

        # filtra None para no borrar campos accidentalmente
        update_data = {k: v for k, v in data.items() if v is not None}

        # si hay archivo, sube/actualiza imagen y setea la URL
        file = request.files.get('imagen')
        if file:
            # si tu storage_service requiere distinguir update/upload:
            # if existente.get('imagen_url'):
            #     imagen_url = storage_service.update_file(existente.get('imagen_url'), file, 'proyectos')
            # else:
            #     imagen_url = storage_service.upload_file(file, 'proyectos')
            imagen_url = storage_service.update_file(existente.get('imagen_url'), file, 'proyectos')
            update_data['imagen_url'] = imagen_url

        actualizado = proyecto_service.actualizar_proyecto(id, update_data)
        return jsonify(actualizado), 200

    except Exception as e:
        # 400 por consistencia con servicios al fallar parseo/validación/subida
        return jsonify({'error': str(e)}), 400


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
