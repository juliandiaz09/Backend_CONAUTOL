from flask import Blueprint, request, jsonify
from app.services.servicio_service import ServicioService
from app.services.supabase_service import SupabaseStorageService
from app.models.servicio import ServicioCreate, ServicioUpdate
from app.utils.decorators import token_required
import json

servicios_bp = Blueprint('servicios', __name__)
servicio_service = ServicioService()
storage_service = SupabaseStorageService()

@servicios_bp.route('/', methods=['GET'])
def listar_servicios():
    try:
        activo = request.args.get('activo')
        if activo is not None:
            activo = activo.lower() == 'true'
        servicios = servicio_service.listar_servicios(activo)
        return jsonify(servicios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/<int:id>', methods=['GET'])
def obtener_servicio(id):
    try:
        servicio = servicio_service.obtener_servicio(id)
        if servicio:
            return jsonify(servicio), 200
        return jsonify({'error': 'Servicio no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/', methods=['POST'])
@token_required
def crear_servicio():
    try:
      print(request.form.get('data'))
      # 1) tomar data (JSON) y archivo (imagen) desde multipart/form-data
      data_str = request.form.get('data')
      if not data_str:
          return jsonify({'error': 'No se proporcionaron datos'}), 400
      data = json.loads(data_str)

      # 2) valida campos mínimos (ajusta tu modelo)
      ServicioCreate(**data)

      # 3) si viene imagen, súbela y agrega la URL resultante
      file = request.files.get('imagen')
      if file:
          imagen_url = storage_service.upload_file(file, 'servicios')
          data['imagen_url'] = imagen_url

      # 4) crea en base de datos
      creado = servicio_service.crear_servicio(data)
      return jsonify(creado), 201

    except Exception as e:
      return jsonify({'error': str(e)}), 400

@servicios_bp.route('/<int:id>', methods=['PUT'])
@token_required
def actualizar_servicio(id):
    try:
        data_str = request.form.get('data')
        if not data_str:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
            
        data = json.loads(data_str)
        
        servicio_existente = servicio_service.obtener_servicio(id)
        if not servicio_existente:
            return jsonify({'error': 'Servicio no encontrado'}), 404

        update_data = {k: v for k, v in data.items() if v is not None}

        if 'imagen' in request.files:
            file = request.files['imagen']
            imagen_url = storage_service.update_file(servicio_existente.get('imagen_url'), file, 'servicios')
            update_data['imagen_url'] = imagen_url

        servicio = servicio_service.actualizar_servicio(id, update_data)
        return jsonify(servicio), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@servicios_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def eliminar_servicio(id):
    try:
        servicio_existente = servicio_service.obtener_servicio(id)
        if not servicio_existente:
            return jsonify({'error': 'Servicio no encontrado'}), 404

        # Eliminar la imagen si existe
        if servicio_existente.get('imagen_url'):
            storage_service.delete_file(servicio_existente['imagen_url'])

        servicio_service.eliminar_servicio(id)
        return jsonify({'message': 'Servicio eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/categoria/<string:categoria>', methods=['GET'])
def buscar_por_categoria(categoria):
    try:
        servicios = servicio_service.buscar_por_categoria(categoria)
        return jsonify(servicios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
