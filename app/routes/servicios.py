from flask import Blueprint, request, jsonify
from app.services.servicio_service import ServicioService
from app.models.servicio import ServicioCreate, ServicioUpdate

servicios_bp = Blueprint('servicios', __name__)
servicio_service = ServicioService()

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
def crear_servicio():
    try:
        data = request.get_json()
        # Validar con Pydantic
        servicio_data = ServicioCreate(**data)
        servicio = servicio_service.crear_servicio(servicio_data.model_dump())
        return jsonify(servicio), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@servicios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_servicio(id):
    try:
        data = request.get_json()
        # Validar con Pydantic
        servicio_data = ServicioUpdate(**data)
        # Solo enviar campos no nulos
        update_data = {k: v for k, v in servicio_data.model_dump().items() if v is not None}
        servicio = servicio_service.actualizar_servicio(id, update_data)
        return jsonify(servicio), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@servicios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_servicio(id):
    try:
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
