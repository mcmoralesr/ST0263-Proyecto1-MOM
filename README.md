# ST0263 - Proyecto 1: Middleware de Mensajería Asíncrona (MOM)

## Información del curso
- **Materia:** ST0263 - Tópicos Especiales en Telemática
- **Estudiantes:**
  - Manuel Arango Gómez - marangog3@eafit.edu.co
  - Sebastián Cano Rincón - scanor2@eafit.edu.co
  - Maria Camila Morales - mcmorales@eafit.edu.co
- **Profesor:** Alvaro Enrique Ospina Sanjuan - aeospinas@eafit.brightspace.com

---

## Proyecto 1: Diseño e Implementación de un Middleware que Implemente un Servicio de Mensajería Asincrónica entre Aplicaciones

### 1. Breve descripción de la actividad
El objetivo del proyecto es diseñar e implementar un Middleware Orientado a Mensajes (MOM), que permita a un conjunto de clientes comunicarse de manera asincrónica usando colas y tópicos replicados en un clúster de nodos MOM. El MOM maneja funcionalidades como autenticación, gestión de colas y tópicos, envío y recepción de mensajes, y replicación entre nodos usando gRPC.

### 1.1 Aspectos desarrollados
- Autenticación JWT entre cliente y MOM.
- Comunicación REST cliente-MOM.
- Comunicación gRPC entre MOMs.
- Replicación activa tipo *push* de colas y tópicos entre MOMs.
- Simulación de datos para colas/tópicos con contenido de ejemplo.
- Arquitectura distribuida de 3 MOMs (mom1, mom2, mom3).

### 1.2 Aspectos NO desarrollados
_(A completar al final del proyecto si queda algo pendiente)_

---

### 2. Diseño de Alto Nivel y Arquitectura
- Arquitectura distribuida con 3 nodos MOM.
- Comunicación REST entre cliente y nodo MOM.
- Comunicación gRPC entre MOMs.
- Replicación activa entre nodos.
- Simulación de colas/tópicos como estructuras `dict` compartibles.

![image](https://github.com/user-attachments/assets/5be7ef5d-d4e6-4f42-8d4f-2232875d58cd)

---

### 3. Ambiente de Desarrollo

#### Tecnologías (nueva versión en Python)
- Python 3.12
- FastAPI `v0.115.12`
- Uvicorn `v0.34.0`
- python-jose `[cryptography]`
- python-multipart
- grpcio (para comunicación entre MOMs)
5. Guía rápida de uso
Cliente obtiene JWT desde el API (otro equipo).

Cliente envía Bearer <TOKEN> en los headers.

Cliente publica/consume mensajes de colas o tópicos (revistas).

MOM1 replica automáticamente a MOM2 y MOM3 vía gRPC.
