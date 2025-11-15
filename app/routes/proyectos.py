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
        
        # Parsear imagen_urls para cada proyecto
        for proyecto in proyectos:
            if proyecto.get('imagen_urls'):
                if isinstance(proyecto['imagen_urls'], str):
                    try:
                        proyecto['imagen_urls'] = json.loads(proyecto['imagen_urls'])
                    except:
                        proyecto['imagen_urls'] = []
            else:
                proyecto['imagen_urls'] = []
        
        return jsonify(proyectos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/<int:id>', methods=['GET'])
def obtener_proyecto(id):
    try:
        proyecto = proyecto_service.obtener_proyecto(id)
        if proyecto:
            # Parsear imagen_urls si es string JSON
            if proyecto.get('imagen_urls'):
                if isinstance(proyecto['imagen_urls'], str):
                    try:
                        proyecto['imagen_urls'] = json.loads(proyecto['imagen_urls'])
                        print(f"✅ imagen_urls parseado: {proyecto['imagen_urls']}")
                    except:
                        proyecto['imagen_urls'] = []
                        print(f"⚠️ No se pudo parsear imagen_urls")
            else:
                proyecto['imagen_urls'] = []
            
            print(f"\n🔍 GET Proyecto {id}:")
            print(f"  - imagen_urls: {proyecto.get('imagen_urls')}")
            print(f"  - tipo imagen_urls: {type(proyecto.get('imagen_urls'))}")
            
            return jsonify(proyecto), 200
        return jsonify({'error': 'Proyecto no encontrado'}), 404
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@proyectos_bp.route('/', methods=['POST'])
@token_required
def crear_proyecto():
    try:
        data_str = request.form.get('data')
        if not data_str:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        data = json.loads(data_str)

        # Obtener múltiples archivos
        files = request.files.getlist('imagenes')
        
        print(f"📥 Archivos recibidos: {len(files)}")
        for idx, file in enumerate(files):
            print(f"  {idx + 1}. {file.filename}")
        
        imagen_urls = []
        if files and files[0].filename:
            # Subir todas las imágenes
            imagen_urls = storage_service.upload_multiple_files(files, 'proyectos')
            print(f"✅ URLs generadas: {imagen_urls}")
        
        # 🔥 Solo guardamos imagen_urls (la primera es la principal)
        data['imagen_urls'] = json.dumps(imagen_urls)
        
        print(f"📋 Datos a guardar:")
        print(f"  - imagen_urls (JSON string): {data['imagen_urls']}")

        creado = proyecto_service.crear_proyecto(data)
        
        # 🔥 Parsear de vuelta para la respuesta
        if creado.get('imagen_urls') and isinstance(creado['imagen_urls'], str):
            creado['imagen_urls'] = json.loads(creado['imagen_urls'])
        
        print(f"✅ Proyecto creado:")
        print(f"  - id: {creado.get('id')}")
        print(f"  - imagen_urls en respuesta: {creado.get('imagen_urls')}")
        
        return jsonify(creado), 201

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
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

        print(f"\n📋 Datos recibidos:")
        print(f"  - data: {data}")
        
        # 🔥 PASO 1: Extraer imagenes_a_eliminar y índice de imagen principal
        imagenes_a_eliminar = data.pop('imagenes_a_eliminar', [])
        indice_principal = data.pop('indice_imagen_principal', 0)
        
        print(f"  - Imágenes a eliminar: {imagenes_a_eliminar}")
        print(f"  - Índice imagen principal: {indice_principal}")
        
        # 🔥 PASO 2: Eliminar archivos del bucket
        if imagenes_a_eliminar:
            for url in imagenes_a_eliminar:
                try:
                    storage_service.delete_file(url)
                    print(f"✓ Imagen eliminada del bucket: {url}")
                except Exception as e:
                    print(f"⚠ Error eliminando imagen {url}: {e}")
        
        # 🔥 PASO 3: Obtener URLs existentes
        urls_existentes_raw = existente.get('imagen_urls', '[]')
        
        if isinstance(urls_existentes_raw, str):
            try:
                urls_existentes = json.loads(urls_existentes_raw)
            except:
                urls_existentes = []
        else:
            urls_existentes = urls_existentes_raw if isinstance(urls_existentes_raw, list) else []
        
        print(f"📸 URLs existentes: {urls_existentes}")
        
        # Filtrar las que NO están marcadas para eliminar
        urls_a_mantener = [
            url for url in urls_existentes 
            if url not in imagenes_a_eliminar
        ]
        
        print(f"📸 URLs a mantener: {urls_a_mantener}")
        
        # 🔥 PASO 4: Agregar nuevas imágenes si vienen archivos
        new_files = request.files.getlist('imagenes')
        if new_files and new_files[0].filename:
            nuevas_urls = storage_service.upload_multiple_files(new_files, 'proyectos')
            urls_a_mantener.extend(nuevas_urls)
            print(f"✓ {len(nuevas_urls)} imagen(es) nueva(s) subida(s)")
        
        # 🔥 PASO 5: Reordenar array para que la principal esté primera
        if urls_a_mantener and 0 <= indice_principal < len(urls_a_mantener):
            # Mover la imagen principal al inicio
            imagen_principal = urls_a_mantener.pop(indice_principal)
            urls_a_mantener.insert(0, imagen_principal)
            print(f"📸 Imagen principal movida al inicio: {imagen_principal}")
        
        # 🔥 PASO 6: Preparar datos para actualizar
        update_data = {k: v for k, v in data.items() if v is not None}
        
        # Convertir array a JSON string
        update_data['imagen_urls'] = json.dumps(urls_a_mantener)
        
        print(f"📊 Resumen: {len(urls_a_mantener)} imagen(es) total(es)")
        print(f"📝 Datos a actualizar: {list(update_data.keys())}")
        print(f"📸 imagen_urls (JSON): {update_data['imagen_urls']}")

        actualizado = proyecto_service.actualizar_proyecto(id, update_data)
        
        # 🔥 Parsear de vuelta para la respuesta
        if actualizado.get('imagen_urls') and isinstance(actualizado['imagen_urls'], str):
            actualizado['imagen_urls'] = json.loads(actualizado['imagen_urls'])
        
        return jsonify(actualizado), 200

    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@proyectos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def eliminar_proyecto(id):
    try:
        proyecto_existente = proyecto_service.obtener_proyecto(id)
        if not proyecto_existente:
            return jsonify({'error': 'Proyecto no encontrado'}), 404

        # 🔥 Solo necesitamos imagen_urls
        urls_a_eliminar = []
        
        if proyecto_existente.get('imagen_urls'):
            if isinstance(proyecto_existente['imagen_urls'], str):
                try:
                    urls_a_eliminar = json.loads(proyecto_existente['imagen_urls'])
                except:
                    pass
            elif isinstance(proyecto_existente['imagen_urls'], list):
                urls_a_eliminar = proyecto_existente['imagen_urls']
        
        # Eliminar archivos del bucket
        if urls_a_eliminar:
            try:
                storage_service.delete_multiple_files(urls_a_eliminar)
                print(f"✓ {len(urls_a_eliminar)} imagen(es) eliminada(s) del bucket")
            except Exception as e:
                print(f"⚠ Error eliminando imágenes: {e}")

        # Eliminar el proyecto de la base de datos
        proyecto_service.eliminar_proyecto(id)
        return jsonify({'message': 'Proyecto eliminado'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500