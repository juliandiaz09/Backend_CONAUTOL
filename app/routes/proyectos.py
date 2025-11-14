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

        # ✅ MODIFICACIÓN: Manejar múltiples imágenes
        files = request.files.getlist('imagenes')  # Cambia de 'imagen' a 'imagenes'
        
        imagen_urls = []
        if files and files[0].filename:  # Verificar que hay archivos válidos
            # Subir todas las imágenes
            for file in files:
                if file.filename:  # Asegurar que el archivo tiene nombre
                    imagen_url = storage_service.upload_file(file, 'proyectos')
                    imagen_urls.append(imagen_url)
        
        # ✅ MODIFICACIÓN: Guardar array de URLs en lugar de una sola
        if imagen_urls:
            data['imagen_urls'] = imagen_urls  # Cambia a plural
            # Mantener compatibilidad con código existente - primera imagen como principal
            data['imagen_url'] = imagen_urls[0] if imagen_urls else None

        creado = proyecto_service.crear_proyecto(data)
        return jsonify(creado), 201

    except Exception as e:
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

        # ✅ MODIFICACIÓN: Manejar múltiples imágenes en actualización
        new_files = request.files.getlist('imagenes')  # Cambia a 'imagenes'
        
        if new_files and new_files[0].filename:
            # Obtener URLs existentes o inicializar array vacío
            existing_urls = existente.get('imagen_urls', [])
            new_urls = []
            
            # Subir nuevas imágenes
            for file in new_files:
                if file.filename:
                    imagen_url = storage_service.upload_file(file, 'proyectos')
                    new_urls.append(imagen_url)
            
            # Combinar URLs existentes con nuevas (o reemplazar según tu lógica)
            # Opción 1: Reemplazar todas las imágenes
            all_urls = new_urls
            
            # Opción 2: Mantener existentes y agregar nuevas
            # all_urls = existing_urls + new_urls
            
            update_data['imagen_urls'] = all_urls
            # Mantener compatibilidad
            update_data['imagen_url'] = all_urls[0] if all_urls else None

        actualizado = proyecto_service.actualizar_proyecto(id, update_data)
        return jsonify(actualizado), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@proyectos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def eliminar_proyecto(id):
    try:
        proyecto_existente = proyecto_service.obtener_proyecto(id)
        if not proyecto_existente:
            return jsonify({'error': 'Proyecto no encontrado'}), 404

        # ✅ MODIFICACIÓN: Eliminar todas las imágenes
        # Eliminar imagen principal (compatibilidad)
        if proyecto_existente.get('imagen_url'):
            storage_service.delete_file(proyecto_existente['imagen_url'])
        
        # Eliminar todas las imágenes del array
        if proyecto_existente.get('imagen_urls'):
            for imagen_url in proyecto_existente['imagen_urls']:
                try:
                    storage_service.delete_file(imagen_url)
                except Exception as e:
                    print(f"Error eliminando imagen {imagen_url}: {e}")
                    # Continuar con las demás

        proyecto_service.eliminar_proyecto(id)
        return jsonify({'message': 'Proyecto eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500