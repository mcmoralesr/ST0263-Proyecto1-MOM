from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import uuid
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://34.201.237.162"], supports_credentials=True)
app.config['JWT_SECRET_KEY'] = 'clave-secreta-del-proyecto'  # En producción usar variable de entorno
jwt = JWTManager(app)

CORS(app, 
     resources={r"/api/*": {"origins": "http://34.201.237.162"}},
     supports_credentials=True,
     allow_headers="*",
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"]
)

usuarios = {}
topicos = {}
colas = {}
mensajes_topicos = {}
mensajes_colas = {}


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Endpoints de autenticación
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400
    
    if username in usuarios:
        return jsonify({"error": "El usuario ya existe"}), 409
    
    # Hash de la contraseña para almacenamiento seguro
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    usuarios[username] = {'password': hashed_password, 
                          'topicos_creados': [], 
                          'colas_creadas': [],
                          'topicos_suscritos': []
                          }
    
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password or username not in usuarios:
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    stored_password = usuarios[username]['password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        # Generar token JWT
        access_token = create_access_token(identity=username)
        return jsonify({"token": access_token}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint para suscribirse a un tópico
@app.route('/api/topicos/<nombre_topico>/suscribir', methods=['POST'])
@jwt_required()
def suscribir_topico(nombre_topico):
    current_user = get_jwt_identity()

    if nombre_topico not in topicos:
        return jsonify({"error": "Tópico no encontrado"}), 404
    
    if nombre_topico in usuarios[current_user]['topicos_suscritos']:
        return jsonify({"error": "Ya estás suscrito a este tópico"}), 409
    
    usuarios[current_user]['topicos_suscritos'].append(nombre_topico)
    return jsonify({"mensaje": f"Suscrito al tópico '{nombre_topico}' exitosamente"}), 200

@app.route('/api/topicos/<nombre_topico>/desuscribir', methods=['POST'])
@jwt_required()
def desuscribir_topico(nombre_topico):
    current_user = get_jwt_identity()

    if nombre_topico not in topicos:
        return jsonify({"error": "Tópico no encontrado"}), 404
    
    if nombre_topico not in usuarios[current_user]['topicos_suscritos']:
        return jsonify({"error": "No estás suscrito a este tópico"}), 409
    
    usuarios[current_user]['topicos_suscritos'].remove(nombre_topico)
    return jsonify({"mensaje": f"Desuscrito del tópico '{nombre_topico}' exitosamente"}), 200



# Endpoints de gestión de tópicos
@app.route('/api/topicos', methods=['GET'])
@jwt_required()
def listar_topicos():
    return jsonify({"topicos": list(topicos.keys())}), 200

@app.route('/api/topicos', methods=['POST'])
@jwt_required()
def crear_topico():
    data = request.json
    nombre_topico = data.get('nombre')
    current_user = get_jwt_identity()
    
    if not nombre_topico:
        return jsonify({"error": "Nombre del tópico es obligatorio"}), 400
    
    if nombre_topico in topicos:
        return jsonify({"error": "El tópico ya existe"}), 409
    
    topico_id = str(uuid.uuid4())
    topicos[nombre_topico] = {
        'id': topico_id,
        'creador': current_user,
        'fecha_creacion': datetime.now().isoformat()
    }
    usuarios[current_user]['topicos_creados'].append(nombre_topico)
    mensajes_topicos[nombre_topico] = []
    
    return jsonify({
        "mensaje": f"Tópico '{nombre_topico}' creado exitosamente",
        "topico_id": topico_id
    }), 201

@app.route('/api/topicos/<nombre_topico>', methods=['DELETE'])
@jwt_required()
def borrar_topico(nombre_topico):
    current_user = get_jwt_identity()
    
    if nombre_topico not in topicos:
        return jsonify({"error": "Tópico no encontrado"}), 404
    
    if topicos[nombre_topico]['creador'] != current_user:
        return jsonify({"error": "No tienes permiso para borrar este tópico"}), 403
    
    del topicos[nombre_topico]
    if nombre_topico in mensajes_topicos:
        del mensajes_topicos[nombre_topico]
    usuarios[current_user]['topicos_creados'].remove(nombre_topico)
    
    return jsonify({"mensaje": f"Tópico '{nombre_topico}' eliminado exitosamente"}), 200

# Endpoints para las colas
@app.route('/api/colas', methods=['GET'])
@jwt_required()
def listar_colas():
    return jsonify({"colas": list(colas.keys())}), 200

@app.route('/api/colas', methods=['POST'])
@jwt_required()
def crear_cola():
    data = request.json
    nombre_cola = data.get('nombre')
    current_user = get_jwt_identity()
    
    if not nombre_cola:
        return jsonify({"error": "Nombre de la cola es obligatorio"}), 400
    
    if nombre_cola in colas:
        return jsonify({"error": "La cola ya existe"}), 409
    
    cola_id = str(uuid.uuid4())
    colas[nombre_cola] = {
        'id': cola_id,
        'creador': current_user,
        'fecha_creacion': datetime.now().isoformat()
    }
    usuarios[current_user]['colas_creadas'].append(nombre_cola)
    mensajes_colas[nombre_cola] = []
    
    return jsonify({
        "mensaje": f"Cola '{nombre_cola}' creada exitosamente",
        "cola_id": cola_id
    }), 201

@app.route('/api/colas/<nombre_cola>', methods=['DELETE'])
@jwt_required()
def borrar_cola(nombre_cola):
    current_user = get_jwt_identity()
    
    if nombre_cola not in colas:
        return jsonify({"error": "Cola no encontrada"}), 404
    
    if colas[nombre_cola]['creador'] != current_user:
        return jsonify({"error": "No tienes permiso para borrar esta cola"}), 403
    
    del colas[nombre_cola]
    if nombre_cola in mensajes_colas:
        del mensajes_colas[nombre_cola]
    usuarios[current_user]['colas_creadas'].remove(nombre_cola)
    
    return jsonify({"mensaje": f"Cola '{nombre_cola}' eliminada exitosamente"}), 200

# Endpoints para envío y recepción de mensajes
@app.route('/api/topicos/<nombre_topico>/mensajes', methods=['POST'])
@jwt_required()
def enviar_mensaje_topico(nombre_topico):
    current_user = get_jwt_identity()
    data = request.json
    mensaje = data.get('mensaje')
    
    if not mensaje:
        return jsonify({"error": "El mensaje no puede estar vacío"}), 400
    
    if nombre_topico not in topicos:
        return jsonify({"error": "Tópico no encontrado"}), 404
    
    mensaje_id = str(uuid.uuid4())
    mensaje_data = {
        'id': mensaje_id,   
        'emisor': current_user,
        'contenido': mensaje,
        'timestamp': datetime.now().isoformat()
    }
    
    mensajes_topicos[nombre_topico].append(mensaje_data)
    
    
    return jsonify({
        "mensaje": "Mensaje enviado exitosamente al tópico",
        "mensaje_id": mensaje_id
    }), 201

@app.route('/api/topicos/<nombre_topico>/mensajes', methods=['GET'])
@jwt_required()
def recibir_mensajes_topico(nombre_topico):
    if nombre_topico not in topicos:
        return jsonify({"error": "Tópico no encontrado"}), 404
    
    return jsonify({
        "topico": nombre_topico,
        "mensajes": mensajes_topicos.get(nombre_topico, [])
    }), 200

@app.route('/api/colas/<nombre_cola>/mensajes', methods=['POST'])
@jwt_required()
def enviar_mensaje_cola(nombre_cola):
    current_user = get_jwt_identity()
    data = request.json
    mensaje = data.get('mensaje')
    
    if not mensaje:
        return jsonify({"error": "El mensaje no puede estar vacío"}), 400
    
    if nombre_cola not in colas:
        return jsonify({"error": "Cola no encontrada"}), 404
    
    mensaje_id = str(uuid.uuid4())
    mensaje_data = {
        'id': mensaje_id,
        'emisor': current_user,
        'contenido': mensaje,
        'timestamp': datetime.now().isoformat(),
        'entregado': False
    }
    
    mensajes_colas[nombre_cola].append(mensaje_data)
    
    return jsonify({
        "mensaje": "Mensaje enviado exitosamente a la cola",
        "mensaje_id": mensaje_id
    }), 201

@app.route('/api/colas/<nombre_cola>/mensajes', methods=['GET'])
@jwt_required()
def recibir_mensaje_cola(nombre_cola):
    current_user = get_jwt_identity()
    
    if nombre_cola not in colas:
        return jsonify({"error": "Cola no encontrada"}), 404
    
    for mensaje in mensajes_colas[nombre_cola]:
        if not mensaje['entregado']:
            mensaje['entregado'] = True
            mensaje['receptor'] = current_user
            mensaje['fecha_entrega'] = datetime.now().isoformat()
            
            return jsonify({
                "mensaje": mensaje
            }), 200
    
    return jsonify({"mensaje": "No hay mensajes pendientes en la cola"}), 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
