class MessageBroker:
    def __init__(self):
        self.queues = {}  # Diccionario para colas
        self.topics = {}  # Diccionario para tópicos

        # Crear por defecto q1 y t1 si no existen
        self.create_queue("q1", description="Cola por defecto")
        self.create_topic("t1", description="Tópico por defecto")

    def create_queue(self, name, description=""):
        if name not in self.queues:
            self.queues[name] = []
            print(f"[Broker MOM1] ✅ Cola creada: '{name}' - {description}")
        else:
            print(f"[Broker MOM1] ⚠️ La cola '{name}' ya existe")

    def create_topic(self, name, description=""):
        if name not in self.topics:
            self.topics[name] = []
            print(f"[Broker MOM1] ✅ Tópico creado: '{name}' - {description}")
        else:
            print(f"[Broker MOM1] ⚠️ El tópico '{name}' ya existe")

    def publish_to_queue(self, queue_name, message, user=None):
        if queue_name in self.queues:
            self.queues[queue_name].append({
                "emisor": user,
                "contenido": message
            })
            print(f"[Broker MOM1] 📩 Mensaje en cola '{queue_name}' por '{user}': {message}")
        else:
            print(f"[Broker MOM1] ❌ Cola '{queue_name}' no encontrada")

    def publish_to_topic(self, topic_name, message, emisor=None):
        if topic_name in self.topics:
            self.topics[topic_name].append({
                "emisor": emisor,
                "contenido": message
            })
            print(f"[Broker MOM1] 📢 Mensaje en tópico '{topic_name}' por '{emisor}': {message}")
        else:
            print(f"[Broker MOM1] ❌ Tópico '{topic_name}' no encontrado")

    def consume_from_queue(self, queue_name):
        if queue_name in self.queues and self.queues[queue_name]:
            message = self.queues[queue_name].pop(0)
            print(f"[Broker MOM1] 📨 Consumido de cola '{queue_name}': {message}")
            return message
        else:
            print(f"[Broker MOM1] ⚠️ Cola '{queue_name}' vacía o no encontrada")
            return None

    def consume_from_topic(self, topic_name):
        if topic_name in self.topics and self.topics[topic_name]:
            message = self.topics[topic_name][-1]
            print(f"[Broker MOM1] 🔁 Último mensaje en tópico '{topic_name}': {message}")
            return message
        else:
            print(f"[Broker MOM1] ⚠️ Tópico '{topic_name}' vacío o no encontrado")
            return None

# Instancia global del broker
broker = MessageBroker()

