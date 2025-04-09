# mom-nodes/mom1/mom1_server.py

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from jose import jwt, JWTError
from datetime import datetime
from message_broker import broker
from data_simulation import simulate_data

SECRET_KEY = "clave-secreta-del-proyecto"
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    simulate_data()

def decode_jwt_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_user_from_auth(authorization: str) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Formato de token inválido")
    token = authorization[7:]
    user = decode_jwt_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    return user

# === TOPICOS ===

@app.get("/topicos")
def listar_topicos(authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    return {"usuario": user, "topicos": list(broker.topics.keys())}

@app.post("/topicos")
def crear_topico(data: dict, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    nombre = data.get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre del tópico requerido")
    if nombre in broker.topics:
        raise HTTPException(status_code=409, detail="Tópico ya existe")
    broker.create_topic(nombre, owner=user)
    return {"mensaje": f"Tópico '{nombre}' creado por {user}"}

@app.delete("/topicos/{nombre}")
def eliminar_topico(nombre: str, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    if not broker.topic_exists(nombre):
        raise HTTPException(status_code=404, detail="Tópico no encontrado")
    if not broker.can_user_modify_topic(nombre, user):
        raise HTTPException(status_code=403, detail="No autorizado")
    broker.delete_topic(nombre)
    return {"mensaje": f"Tópico '{nombre}' eliminado por {user}"}

@app.post("/topicos/{nombre}/publicar")
def publicar_en_topico(nombre: str, data: dict, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    mensaje = data.get("mensaje")
    if not mensaje:
        raise HTTPException(status_code=400, detail="Mensaje vacío")
    if not broker.topic_exists(nombre):
        raise HTTPException(status_code=404, detail="Tópico no encontrado")
    broker.publish_to_topic(nombre, mensaje, user)
    return {"mensaje": "Mensaje publicado exitosamente"}

@app.get("/topicos/{nombre}/mensajes")
def recibir_mensajes(nombre: str, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    if not broker.topic_exists(nombre):
        raise HTTPException(status_code=404, detail="Tópico no encontrado")
    mensajes = broker.get_messages_from_topic(nombre)
    return {"topico": nombre, "mensajes": mensajes}

# === COLAS ===

@app.get("/colas")
def listar_colas(authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    return {"usuario": user, "colas": list(broker.queues.keys())}

@app.post("/colas")
def crear_cola(data: dict, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    nombre = data.get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre de cola requerido")
    if nombre in broker.queues:
        raise HTTPException(status_code=409, detail="Cola ya existe")
    broker.create_queue(nombre, owner=user)
    return {"mensaje": f"Cola '{nombre}' creada por {user}"}

@app.delete("/colas/{nombre}")
def eliminar_cola(nombre: str, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    if not broker.queue_exists(nombre):
        raise HTTPException(status_code=404, detail="Cola no encontrada")
    if not broker.can_user_modify_queue(nombre, user):
        raise HTTPException(status_code=403, detail="No autorizado")
    broker.delete_queue(nombre)
    return {"mensaje": f"Cola '{nombre}' eliminada por {user}"}

@app.post("/colas/{nombre}/enviar")
def enviar_a_cola(nombre: str, data: dict, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    mensaje = data.get("mensaje")
    if not mensaje:
        raise HTTPException(status_code=400, detail="Mensaje vacío")
    if not broker.queue_exists(nombre):
        raise HTTPException(status_code=404, detail="Cola no encontrada")
    broker.send_to_queue(nombre, mensaje, user)
    return {"mensaje": "Mensaje enviado a la cola"}

@app.get("/colas/{nombre}/recibir")
def recibir_de_cola(nombre: str, authorization: str = Header(...)):
    user = get_user_from_auth(authorization)
    if not broker.queue_exists(nombre):
        raise HTTPException(status_code=404, detail="Cola no encontrada")
    mensaje = broker.consume_from_queue(nombre)
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"mensaje": "Cola vacía"}, 204
