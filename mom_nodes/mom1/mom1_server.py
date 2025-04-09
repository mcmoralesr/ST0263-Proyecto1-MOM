from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime
from mom_nodes.mom1.message_broker import broker
from mom_nodes.mom1.grpc_client import replicator

app = FastAPI()

# CORS para permitir conexiones desde cualquier origen (ajustar si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIG ===
SECRET_KEY = "clave-secreta-del-proyecto"
ALGORITHM = "HS256"

# === UTILS ===

def get_username_from_token(auth: Optional[str]) -> str:
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token inválido")
    token = auth[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

# === TOPICOS ===

@app.get("/topicos")
def listar_topicos(authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    return {"topicos": list(broker.topicos.keys())}

@app.post("/topicos")
def crear_topico(data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    nombre = data.get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="Falta nombre")
    broker.create_topic(nombre, description=f"Tópico de {usuario}")
    replicator.replicate_create_topic(nombre, description=f"Replicado de {usuario}")
    return {"mensaje": f"Tópico '{nombre}' creado por {usuario}"}

@app.delete("/topicos/{nombre}")
def eliminar_topico(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    broker.delete_topic(nombre)
    return {"mensaje": f"Tópico '{nombre}' eliminado"}

@app.post("/topicos/{nombre}/publicar")
def publicar_topico(nombre: str, data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    mensaje = data.get("mensaje")
    if not mensaje:
        raise HTTPException(status_code=400, detail="Falta mensaje")
    broker.publish_to_topic(nombre, mensaje, emisor=usuario)
    replicator.replicate_publish_to_topic(nombre, mensaje)
    return {"mensaje": "Mensaje publicado exitosamente"}

@app.get("/topicos/{nombre}/mensajes")
def recibir_topico(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    mensajes = broker.get_messages_from_topic(nombre)
    return {"topico": nombre, "mensajes": mensajes}

# === COLAS ===

@app.get("/colas")
def listar_colas(authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    return {"colas": list(broker.colas.keys())}

@app.post("/colas")
def crear_cola(data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    nombre = data.get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="Falta nombre")
    broker.create_queue(nombre, description=f"Cola de {usuario}")
    replicator.replicate_create_queue(nombre, description=f"Replicado de {usuario}")
    return {"mensaje": f"Cola '{nombre}' creada por {usuario}"}

@app.delete("/colas/{nombre}")
def eliminar_cola(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    broker.delete_queue(nombre)
    return {"mensaje": f"Cola '{nombre}' eliminada"}

@app.post("/colas/{nombre}/enviar")
def enviar_cola(nombre: str, data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    mensaje = data.get("mensaje")
    if not mensaje:
        raise HTTPException(status_code=400, detail="Falta mensaje")
    broker.publish_to_queue(nombre, mensaje, emisor=usuario)
    replicator.replicate_publish_to_queue(nombre, mensaje)
    return {"mensaje": "Mensaje enviado a la cola"}

@app.get("/colas/{nombre}/recibir")
def recibir_cola(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    mensaje = broker.consume_from_queue(nombre)
    if not mensaje:
        return {"mensaje": "Cola vacía"}
    return {"mensaje": mensaje}

# === DATA SIMULADA ===

@app.on_event("startup")
def startup_event():
    from mom_nodes.mom1.data_simulation import simulate_data
    simulate_data()
