from datetime import datetime

class MessageBroker:
    def __init__(self):
        self.topics = {}
        self.topic_owners = {}
        self.topic_messages = {}

        self.queues = {}
        self.queue_owners = {}
        self.queue_messages = {}

    def create_topic(self, name, owner=None, description=None):
        self.topics[name] = {"name": name, "owner": owner or "simulado", "description": description}
        self.topic_owners[name] = owner or "simulado"
        self.topic_messages[name] = []

    def delete_topic(self, name):
        self.topics.pop(name, None)
        self.topic_owners.pop(name, None)
        self.topic_messages.pop(name, None)

    def topic_exists(self, name):
        return name in self.topics

    def can_user_modify_topic(self, name, user):
        return self.topic_owners.get(name) == user

    def publish_to_topic(self, name, message, user):
        self.topic_messages[name].append({
            "contenido": message,
            "emisor": user,
            "timestamp": datetime.now().isoformat()
        })

    def get_messages_from_topic(self, name):
        return self.topic_messages.get(name, [])

    def create_queue(self, name, owner=None, description=None):
        self.queues[name] = {"name": name, "owner": owner or "simulado", "description": description}
        self.queue_owners[name] = owner or "simulado"
        self.queue_messages[name] = []

    def delete_queue(self, name):
        self.queues.pop(name, None)
        self.queue_owners.pop(name, None)
        self.queue_messages.pop(name, None)

    def queue_exists(self, name):
        return name in self.queues

    def can_user_modify_queue(self, name, user):
        return self.queue_owners.get(name) == user

    def send_to_queue(self, name, message, user):
        self.queue_messages[name].append({
            "contenido": message,
            "emisor": user,
            "timestamp": datetime.now().isoformat(),
            "entregado": False
        })

    def consume_from_queue(self, name):
        cola = self.queue_messages.get(name, [])
        for m in cola:
            if not m["entregado"]:
                m["entregado"] = True
                return m
        return None

broker = MessageBroker()
