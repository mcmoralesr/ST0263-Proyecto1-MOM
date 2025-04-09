# mom_nodes/mom2/message_broker.py

from datetime import datetime

class MessageBroker:
    def __init__(self):
        self.colas = {}
        self.topicos = {}
        self.mensajes_colas = {}
        self.mensajes_topicos = {}

    def create_queue(self, nombre, description=""):
        if nombre not in self.colas:
            self.colas[nombre] = description
            self.mensajes_colas[nombre] = []

    def create_topic(self, nombre, description=""):
        if nombre not in self.topicos:
            self.topicos[nombre] = description
            self.mensajes_topicos[nombre] = []

    def publish_to_queue(self, nombre, mensaje, emisor="replica"):
        if nombre in self.mensajes_colas:
            self.mensajes_colas[nombre].append({
                "contenido": mensaje,
                "emisor": emisor,
                "timestamp": datetime.now().isoformat()
            })

    def publish_to_topic(self, nombre, mensaje, emisor="replica"):
        if nombre in self.mensajes_topicos:
            self.mensajes_topicos[nombre].append({
                "contenido": mensaje,
                "emisor": emisor,
                "timestamp": datetime.now().isoformat()
            })

broker = MessageBroker()
