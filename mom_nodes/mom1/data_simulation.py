# mom_nodes/mom1/data_simulation.py

from mom_nodes.mom1.message_broker import broker
from mom_nodes.mom1.grpc_client import replicator

def load_sample_data():
    # Crear recursos locales en MOM1
    broker.create_queue("q1", description="Cola principal MOM1")
    broker.create_topic("t1", description="Tópico principal MOM1")

    # Publicar mensaje (se requiere el parámetro 'user')
    broker.publish_to_topic("t1", "Noticia t1 publicada por MOM1", "mom1")

    # Replicar a MOM2 y MOM3
    replicator.replicate_create_queue("q1", description="Cola principal MOM1")
    replicator.replicate_create_topic("t1", description="Tópico principal MOM1")
    replicator.replicate_publish_to_topic("t1", "Noticia t1 publicada por MOM1")

if __name__ == "__main__":
    load_sample_data()
