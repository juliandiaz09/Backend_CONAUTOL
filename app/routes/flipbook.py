from flask import Blueprint, request, jsonify
from app.services.flipbook_service import FlipbookService
from app.models.flipbook import FlipbookCreate, FlipbookUpdate, PaginaFlipbook

flipbook_bp = Blueprint('flipbook', __name__)
flipbook_service = FlipbookService()

@flipbook_bp.route('/', methods=['GET'])
def listar_flipbooks():
    try:
        activo = request.args.get('activo')
        if activo is not None:
            activo = activo.lower() == 'true'
        flipbooks = flipbook_service.listar_flipbooks(activo)
        return jsonify(flipbooks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flipbook_bp.route('/<int:id>', methods=['GET'])
def obtener_flipbook(id):
    try:
        flipbook = flipbook_service.obtener_flipbook(id)
        if flipbook:
            return jsonify(flipbook), 200
        return jsonify({'error': 'Flipbook no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flipbook_bp.route('/', methods=['POST'])
def crear_flipbook():
    try:
        data = request.get_json()
        flipbook_data = FlipbookCreate(**data)
        flipbook = flipbook_service.crear_flipbook(flipbook_data.model_dump())
        return jsonify(flipbook), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@flipbook_bp.route('/<int:id>', methods=['PUT'])
def actualizar_flipbook(id):
    try:
        data = request.get_json()
        flipbook_data = FlipbookUpdate(**data)
        update_data = {k: v for k, v in flipbook_data.model_dump().items() if v is not None}
        flipbook = flipbook_service.actualizar_flipbook(id, update_data)
        return jsonify(flipbook), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@flipbook_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_flipbook(id):
    try:
        flipbook_service.eliminar_flipbook(id)
        return jsonify({'message': 'Flipbook eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flipbook_bp.route('/<int:flipbook_id>/paginas', methods=['POST'])
def agregar_pagina(flipbook_id):
    try:
        data = request.get_json()
        pagina_data = PaginaFlipbook(**data)
        flipbook = flipbook_service.agregar_pagina(flipbook_id, pagina_data.model_dump())
        return jsonify(flipbook), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@flipbook_bp.route('/<int:flipbook_id>/paginas/<int:numero_pagina>', methods=['DELETE'])
def eliminar_pagina(flipbook_id, numero_pagina):
    try:
        flipbook = flipbook_service.eliminar_pagina(flipbook_id, numero_pagina)
        return jsonify(flipbook), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flipbook_bp.route('/categoria/<string:categoria>', methods=['GET'])
def buscar_por_categoria(categoria):
    try:
        flipbooks = flipbook_service.buscar_por_categoria(categoria)
        return jsonify(flipbooks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
