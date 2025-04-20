# mom_nodes/mom1/mom1_server.py
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime
from mom_nodes.mom1.message_broker import broker
from mom_nodes.mom1 import grpc_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "clave-secreta-del-proyecto"
ALGORITHM = "HS256"

def get_username_from_token(auth: Optional[str]) -> str:
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token inválido")
    token = auth[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

@app.on_event("startup")
def crear_recursos_por_defecto():
    # Recursos propios de MOM1
    if "q1" not in broker.colas:
        broker.create_queue("q1", description="Cola propia de MOM1")
    if "t1" not in broker.topicos:
        broker.create_topic("t1", description="Tópico propio de MOM1")
    
    # Réplicas que este nodo mantiene según topología
    if "q2" not in broker.colas:
        broker.create_queue("q2", description="Replica de cola MOM2")
    if "t3" not in broker.topicos:
        broker.create_topic("t3", description="Replica de tópico MOM3")

@app.get("/topicos")
def listar_topicos(authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    return {"topicos": list(broker.topicos.keys())}

@app.post("/topicos")
def crear_topico(data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    nombre = data.get("nombre")
    broker.create_topic(nombre, description=f"Tópico creado por {usuario}")
    grpc_client.replicar_crear_topico(nombre, f"Tópico creado por {usuario}")
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
        raise HTTPException(status_code=400, detail="El mensaje es obligatorio")
    broker.publish_to_topic(nombre, mensaje, emisor=usuario)
    grpc_client.replicar_publicar_en_topico(nombre, mensaje)
    return {"mensaje": "Mensaje publicado exitosamente"}

@app.get("/topicos/{nombre}/mensajes")
def recibir_topico(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    mensajes = broker.get_messages_from_topic(nombre)
    return {"topico": nombre, "mensajes": mensajes}

@app.get("/colas")
def listar_colas(authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    return {"colas": list(broker.colas.keys())}

@app.post("/colas")
def crear_cola(data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    nombre = data.get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre de cola requerido")
    broker.create_queue(nombre, description=f"Cola creada por {usuario}")
    grpc_client.replicar_crear_cola(nombre, f"Cola creada por {usuario}")
    return {"mensaje": f"Cola '{nombre}' creada por {usuario}"}

@app.delete("/colas/{nombre}")
def eliminar_cola(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    broker.delete_queue(nombre)
    return {"mensaje": f"Cola '{nombre}' eliminada"}

@app.post("/colas/{nombre}/publicar")
def publicar_cola(nombre: str, data: dict, authorization: Optional[str] = Header(None)):
    usuario = get_username_from_token(authorization)
    mensaje = data.get("mensaje")
    if not mensaje:
        raise HTTPException(status_code=400, detail="El mensaje es obligatorio")
    broker.publish_to_queue(nombre, mensaje, user=usuario)
    grpc_client.replicar_publicar_en_cola(nombre, mensaje)
    return {"mensaje": "Mensaje publicado exitosamente"}

@app.get("/colas/{nombre}/mensajes")
def recibir_cola(nombre: str, authorization: Optional[str] = Header(None)):
    get_username_from_token(authorization)
    mensaje = broker.get_message_from_queue(nombre)
    if not mensaje:
        return {"mensaje": "No hay mensajes en la cola"}
    return {"cola": nombre, "mensaje": mensaje}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50051)
