# ST0263 - Proyecto 1: Middleware de Mensajería Asíncrona (MOM)

## Información del curso
- **Materia:** ST0263 - Tópicos Especiales en Telemática
- **Estudiantes:**
  - Manuel Arango Gómez - marangog3@eafit.edu.co
  - Sebastián Cano Rincón - scanor2@eafit.edu.co
  - Maria Camila Morales - mcmorales@eafit.edu.co
- **Profesor:** Alvaro Enrique Ospina Sanjuan - aeospinas@eafit.brightspace.com

---

## Proyecto 1: Diseño e Implementación de un Middleware que Implementea un Servicio de Mensajería Asincrónica entre Aplicaciones

### 1. Breve descripción de la actividad
El objetivo del proyecto es diseñar e implementar un Middleware Orientado a Mensajes (MOM), que permita a un conjunto de clientes comunicarse de manera asincrónica usando colas y tópicos replicados en un clúster de nodos MOM. El MOM maneja funcionalidades como autenticación, gestión de colas y tópicos, envío y recepción de mensajes, y replicación entre nodos usando gRPC.

### 1.1 Aspectos desarrollados
- Autenticación JWT entre cliente y MOM.
- Comunicación REST cliente-MOM.
- Comunicación gRPC entre MOMs.
- Replicación activa tipo *push* de colas y tópicos entre MOMs.
- Simulación de datos para colas/tópicos con contenido de ejemplo.
- Arquitectura distribuida de 3 MOMs (mom1, mom2, mom3).
- - Replicación activa tipo push entre MOMs con topología circular:

  Nodo  | Propias       | Réplicas
  ------|---------------|------------------
  MOM1  | q1, t1        | q2, t3
  MOM2  | q2, t2        | q3, t1
  MOM3  | q3, t3        | q1, t2

### 1.2 Aspectos NO desarrollados
_(A completar al final del proyecto si queda algo pendiente)_
- Persistencia en disco o BD (los datos son in-memory).
- Seguridad de gRPC (TLS).
---

### 2. Diseño de Alto Nivel y Arquitectura
- Arquitectura distribuida con 3 nodos MOM.
- Comunicación REST: cliente → API → MOM1
- Comunicación gRPC: MOM1 ↔ MOM2 ↔ MOM3
- Replicación activa entre nodos.
- Simulación de colas/tópicos como estructuras `dict` compartibles.
  
[ CLIENTE ] ← REST → [ API REST Flask ] ← REST → [ MOM1 ] ← gRPC → [ MOM2 ] ← gRPC → [ MOM3 ]

![image](https://github.com/user-attachments/assets/5be7ef5d-d4e6-4f42-8d4f-2232875d58cd)

---

### 3. Ambiente de Desarrollo

#### Tecnologías (nueva versión en Python)
- Python 3.12
- FastAPI `v0.115.12`
- Uvicorn `v0.34.0`
- python-jose `[cryptography]`
- python-multipart
- grpcio (para comunicación entre MOMs) / grpcio-tools
5. Guía rápida de uso
Cliente obtiene JWT desde el API (otro equipo).

Cliente envía Bearer <TOKEN> en los headers.

Cliente publica/consume mensajes de colas o tópicos (revistas).

MOM1 replica automáticamente a MOM2 y MOM3 vía gRPC.



# Setup inicial (una sola vez)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Compilar proto
python -m grpc_tools.protoc -Igrpc --python_out=grpc --grpc_python_out=grpc grpc/mom.proto

# Levantar API REST (puerto 5000)
cd api
python3 app.py

# Levantar MOM1 (puerto 8001)
cd mom_nodes/mom1
uvicorn mom1_server:app --reload --port 8001

# Levantar MOM2 (puerto 50052)
python3 -m mom_nodes.mom2.grpc_server

# Levantar MOM3 (puerto 50053)

▶️ Lanzar MOM1:
source venv/bin/activate
cd ST0263-Proyecto1-MOM
uvicorn mom_nodes.mom1.mom1_server:app --host 0.0.0.0 --port 8001

▶️ Lanzar MOM2:
python3 -m mom_nodes.mom2.grpc_server

5. Organización de carpetas

ST0263-Proyecto1-MOM/
├── api/                  # API Flask REST
├── mom_nodes/
│   ├── mom1/             # MOM1 - REST & gRPC client
│   ├── mom2/             # MOM2 - gRPC server + replicator
│   ├── mom3/             # MOM3 - gRPC server + replicator
├── grpc/                 # mom.proto + compilados


#Referencias
- https://fastapi.tiangolo.com
- https://grpc.io/docs/languages/python/
- https://flask.palletsprojects.com/
- https://testdriven.io/blog/fastapi-jwt-auth/

