# mom1/mom1_server.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import jwt, JWTError
from mom1.message_broker import broker

app = FastAPI()
security = HTTPBearer()

# === CONFIG ===

SECRET_KEY = "1b5e7a8dc5ea4e68a1fc9c8a19874df63e39475ee1d3c2f1c03f7a8bd66b8ed7"
ALGORITHM = "HS256"

# === MODELOS ===

class PublishRequest(BaseModel):
    target: str  # Tópico o Cola
    content: str

class SubscribeRequest(BaseModel):
    target: str
    key: Optional[str] = None

# === AUTENTICACIÓN ===

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido o expirado")

# === ENDPOINTS ===

@app.get("/topics", dependencies=[Depends(verify_token)])
def list_topics():
    return {"topics": list(broker.topics.keys())}

@app.get("/queues", dependencies=[Depends(verify_token)])
def list_queues():
    return {"queues": list(broker.queues.keys())}

@app.post("/publish", dependencies=[Depends(verify_token)])
def publish(request: PublishRequest):
    if request.target in broker.topics:
        broker.publish_to_topic(request.target, request.content)
        return {"status": f"Publicado en tópico '{request.target}'"}
    elif request.target in broker.queues:
        broker.publish_to_queue(request.target, request.content)
        return {"status": f"Publicado en cola '{request.target}'"}
    else:
        raise HTTPException(status_code=404, detail="Destino no encontrado")

@app.post("/subscribe", dependencies=[Depends(verify_token)])
def subscribe(request: SubscribeRequest):
    if request.target in broker.topics:
        broker.subscribe_to_topic(request.target, request.key or "default")
        return {"status": f"Suscrito al tópico '{request.target}' con clave '{request.key}'"}
    elif request.target in broker.queues:
        broker.subscribe_to_queue(request.target)
        return {"status": f"Suscrito a la cola '{request.target}'"}
    else:
        raise HTTPException(status_code=404, detail="Destino no encontrado")

@app.get("/consume/{queue_name}", dependencies=[Depends(verify_token)])
def consume(queue_name: str):
    if queue_name not in broker.queues:
        raise HTTPException(status_code=404, detail="Cola no encontrada")
    message = broker.consume_from_queue(queue_name)
    if message is None:
        return {"status": "No hay mensajes disponibles"}
    return {"message": message}
