# mom_nodes/mom3/message_broker.py

from datetime import datetime

class MessageBroker:
    def __init__(self):
        self.topics = {}
        self.queues = {}

    def create_topic(self, name, description=""):
        if name not in self.topics:
            self.topics[name] = {"description": description, "messages": []}

    def create_queue(self, name, description=""):
        if name not in self.queues:
            self.queues[name] = {"description": description, "messages": []}

    def publish_to_topic(self, name, message, emisor="local"):
        if name in self.topics:
            self.topics[name]["messages"].append({
                "contenido": message,
                "timestamp": datetime.now().isoformat(),
                "emisor": emisor
            })

    def publish_to_queue(self, name, message, emisor="local"):
        if name in self.queues:
            self.queues[name]["messages"].append({
                "contenido": message,
                "timestamp": datetime.now().isoformat(),
                "emisor": emisor,
                "entregado": False
            })

broker = MessageBroker()
