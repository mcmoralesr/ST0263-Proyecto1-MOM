# mom_nodes/mom1/data_simulation.py

from mom_nodes.mom1.message_broker import broker
from mom_nodes.mom1.grpc_client import replicator

def simulate_data():
    # Propios de MOM1
    broker.create_queue("q1", description="Cola principal MOM1")
    broker.create_topic("t1", description="Tópico principal MOM1")

    broker.publish_to_queue("q1", "Primer mensaje en q1 - generado por MOM1", emisor="mom1")
    broker.publish_to_topic("t1", "Noticia t1 publicada por MOM1", emisor="mom1")

    # Replicar a MOM2 y MOM3
    replicator.replicate_create_queue("q1", description="Cola principal MOM1")
    replicator.replicate_create_topic("t1", description="Tópico principal MOM1")

    replicator.replicate_publish_to_queue("q1", "Primer mensaje en q1 - generado por MOM1")
    replicator.replicate_publish_to_topic("t1", "Noticia t1 publicada por MOM1")

if __name__ == "__main__":
    simulate_data()
