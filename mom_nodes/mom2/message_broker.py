class MessageBroker:
    def __init__(self):
        self.queues = {}
        self.topics = {}

    def create_queue(self, name, description=""):
        if name not in self.queues:
            self.queues[name] = []
            print(f"[Broker MOM2] ✅ Cola creada: '{name}' - {description}")
        else:
            print(f"[Broker MOM2] ⚠️ La cola '{name}' ya existe.")

    def create_topic(self, name, description=""):
        if name not in self.topics:
            self.topics[name] = []
            print(f"[Broker MOM2] ✅ Tópico creado: '{name}' - {description}")
        else:
            print(f"[Broker MOM2] ⚠️ El tópico '{name}' ya existe.")

    def publish_to_queue(self, queue_name, message, user=""):
        if queue_name in self.queues:
            self.queues[queue_name].append(message)
            print(f"[Broker MOM2] 📩 Mensaje en cola '{queue_name}' por '{user}': {message}")
        else:
            print(f"[Broker MOM2] ❌ Cola '{queue_name}' no existe.")

    def publish_to_topic(self, topic_name, message, user=""):
        if topic_name in self.topics:
            self.topics[topic_name].append(message)
            print(f"[Broker MOM2] 📢 Mensaje en tópico '{topic_name}' por '{user}': {message}")
        else:
            print(f"[Broker MOM2] ❌ Tópico '{topic_name}' no existe.")

    def consume_from_queue(self, queue_name):
        if queue_name in self.queues and self.queues[queue_name]:
            message = self.queues[queue_name].pop(0)
            print(f"[Broker MOM2] 📨 Consumido de cola '{queue_name}': {message}")
            return message
        else:
            print(f"[Broker MOM2] ⚠️ Cola '{queue_name}' vacía o no existe.")
            return None

    def consume_from_topic(self, topic_name):
        if topic_name in self.topics and self.topics[topic_name]:
            message = self.topics[topic_name][-1]
            print(f"[Broker MOM2] 🔁 Último mensaje en tópico '{topic_name}': {message}")
            return message
        else:
            print(f"[Broker MOM2] ⚠️ Tópico '{topic_name}' vacío o no existe.")
            return None


# Instancia global
broker = MessageBroker()
