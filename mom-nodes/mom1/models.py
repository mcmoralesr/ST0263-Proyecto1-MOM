# mom1/models.py

from typing import List, Dict
from uuid import uuid4
from datetime import datetime


class Message:
    def __init__(self, content: str, sender: str):
        self.id = str(uuid4())
        self.content = content
        self.sender = sender
        self.timestamp = datetime.utcnow().isoformat()


class Queue:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_message(self) -> Message | None:
        if self.messages:
            return self.messages.pop(0)
        return None


class Topic:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.subscribers: Dict[str, List[Message]] = {}

    def publish_message(self, key: str, message: Message):
        if key not in self.subscribers:
            self.subscribers[key] = []
        self.subscribers[key].append(message)

    def consume_messages(self, key: str) -> List[Message]:
        return self.subscribers.pop(key, [])


# Instancias de ejemplo (listas para replicación)

queues: Dict[str, Queue] = {
    "revista-historia": Queue("revista-historia", "Revista mensual sobre historia colombiana"),
    "revista-tecnologia": Queue("revista-tecnologia", "Novedades de tecnología y gadgets"),
    "revista-cultura": Queue("revista-cultura", "Publicaciones de eventos y cultura general"),
}

topics: Dict[str, Topic] = {
    "noticias-politica": Topic("noticias-politica", "Noticias actuales sobre política"),
    "noticias-deporte": Topic("noticias-deporte", "Resumenes deportivos y transmisiones"),
    "noticias-economia": Topic("noticias-economia", "Información de mercados y economía"),
}

# Agregar mensajes iniciales
queues["revista-historia"].add_message(Message("Artículo sobre independencia de Colombia", "editor_historia"))
queues["revista-tecnologia"].add_message(Message("Nuevos lanzamientos de IA 2025", "editor_tech"))
queues["revista-cultura"].add_message(Message("Festival de teatro en Medellín", "editor_cultura"))

topics["noticias-politica"].publish_message("colombia", Message("Elecciones regionales 2025", "reportero1"))
topics["noticias-deporte"].publish_message("futbol", Message("Resultado Colombia vs Brasil", "deportes_tv"))
topics["noticias-economia"].publish_message("bolsa", Message("Suben acciones tecnológicas", "analista1"))
