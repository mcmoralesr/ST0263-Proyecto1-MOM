# mom_nodes/mom1/data_simulation.py
from message_broker import broker

def simulate_data():
    broker.create_queue("Revista_1", description="Revista sobre inteligencia artificial")
    broker.create_queue("Revista_2", description="Revista de ciencia de datos")
    broker.create_queue("Revista_3", description="Revista académica de redes y sistemas distribuidos")
    broker.create_queue("Revista_4", description="Revista de tecnologías móviles")
    broker.create_topic("Eventos", description="Tópico de eventos universitarios")
    broker.create_topic("Convocatorias", description="Tópico para oportunidades académicas")
    broker.create_topic("Noticias", description="Tópico para noticias recientes")
    broker.create_topic("Charlas", description="Charlas de profesores y expertos")

    broker.send_to_queue("Revista_1", "Nuevo artículo sobre LLMs", user="admin")
    broker.send_to_queue("Revista_2", "Edición especial sobre visualización de datos", user="admin")
    broker.publish_to_topic("Eventos", "Simposio de telecomunicaciones, 15 de abril", user="admin")
    broker.publish_to_topic("Convocatorias", "Convocatoria de becas abiertas hasta el 30 de abril", user="admin")
    broker.publish_to_topic("Noticias", "Nuevo laboratorio de redes inaugurado", user="admin")
    broker.publish_to_topic("Charlas", "Conferencia sobre Web3 y descentralización", user="admin")
