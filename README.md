# ST0263 - Proyecto 1: Middleware de Mensajería Asíncrona (MOM)

## Información del curso
- **Materia:** ST0263 - Tópicos Especiales en Telemática
- **Estudiantes:**
  - Manuel Arango Gómez - marangog3@eafit.edu.co
  - Sebastián Cano Rincón - scanor2@eafit.edu.co
  - Maria Camila Morales - mcmorales@eafit.edu.co
- **Profesor:** Alvaro Enrique Ospina Sanjuan - aeospinas@eafit.brightspace.com

---

## Proyecto 1: Diseño e Implementación de un Middleware que Implemente un Servicio de Mensajería Asíncrona entre Aplicaciones

### 1. Breve descripción de la actividad
Diseñamos e implementamos un Middleware Orientado a Mensajes (MOM) que permite a un conjunto de clientes comunicarse de manera asincrónica mediante colas y tópicos replicados en un clúster distribuido de nodos MOM. Cada MOM puede enviar, recibir y replicar mensajes usando REST (con autenticación JWT) y gRPC.

### 1.1 Aspectos desarrollados
- Autenticación JWT entre cliente y MOM.
- API REST para interacción cliente-MOM.
- Comunicación gRPC entre nodos MOM.
- Replicación activa tipo *push* entre nodos MOM.
- Simulación de colas y tópicos por nodo.
- Arquitectura distribuida con 3 nodos MOM (MOM1, MOM2, MOM3).
- Pruebas con curl y Postman.

| Nodo  | Propias       | Réplicas        |
|-------|---------------|------------------|
| MOM1  | q1, t1        | q2, t3           |
| MOM2  | q2, t2        | q3, t1           |
| MOM3  | q3, t3        | q1, t2           |

![image](https://github.com/user-attachments/assets/5be7ef5d-d4e6-4f42-8d4f-2232875d58cd)

### 1.2 Aspectos NO desarrollados
- Persistencia en disco o base de datos (datos en RAM).
- Seguridad en gRPC (TLS).
---

### 2. Diseño de Alto Nivel y Arquitectura

- Arquitectura distribuida con 3 nodos MOM.
- Cliente se conecta por REST a un API central que reenvía a MOM1.
- MOM1 replica a MOM2 y MOM3 mediante gRPC.
- Cada nodo tiene su propio broker y lógica de publicación/consumo.

```
[ CLIENTE ] ← REST → [ API Flask ] ← REST → [ MOM1 ] ↔ gRPC ↔ [ MOM2 ] ↔ gRPC ↔ [ MOM3 ]
```

---

### 3. Ambiente de desarrollo (local)

- **Lenguaje:** Python 3.12
- **Frameworks & Paquetes:**
  - Flask 3.x (API REST)
  - grpcio 1.62
  - grpcio-tools 1.62
  - fastapi 0.110 (en pruebas)
  - python-jose, bcrypt, python-multipart, etc.
- **Protocolo:** gRPC para replicación

#### Instalación:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Compilar protobuf:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. mom.proto
```

#### Lanzar servidores MOM:

**MOM1:**
```bash
uvicorn api.app:app --host 0.0.0.0 --port 8001
```

**MOM2:**
```bash
python3 -m mom_nodes.mom2.grpc_server
```

**MOM3:**
```bash
python3 -m mom_nodes.mom3.grpc_server
```

---

### 4. Ambiente de ejecución en nube

- **Infraestructura:** AWS EC2 (t2.micro)
- **Región:** us-east-1
- **Cada nodo tiene IP elástica asignada.**

| Nodo  | IP Pública      | gRPC | REST |
|-------|------------------|------|------|
| MOM1  | 52.203.79.134    | 50051| 8001 |
| MOM2  | 52.23.81.232     | 50052| 8002 |
| MOM3  | 54.163.98.1      | 50053| 8003 |

#### Ejemplo de uso:
```bash
curl -X POST http://52.203.79.134:8001/colas -H "Authorization: Bearer <token>" -d '{"nombre": "q_test"}'
```

---

### 5. Organización del repositorio
```
ST0263-Proyecto1-MOM/
├── api/                  # API Flask REST
├── mom_nodes/
│   ├── mom1/             # MOM1 - gRPC client
│   ├── mom2/             # MOM2 - gRPC server + replicador
│   ├── mom3/             # MOM3 - gRPC server + replicador
│   └── supervisor/       # Nodo supervisor (en desarrollo)
├── mom.proto             # Archivo protobuf
├── requirements.txt      # Paquetes
```

---

### 6. Referencias
- https://fastapi.tiangolo.com
- https://grpc.io/docs/languages/python/
- https://flask.palletsprojects.com/
- https://testdriven.io/blog/fastapi-jwt-auth/
