# mom_nodes/mom3/data_simulation.py

from mom_nodes.mom3.message_broker import broker
from mom_nodes.mom3.grpc_client import replicator

def simulate_data():
    # Propios de MOM3
    broker.create_queue("q3", description="Cola de MOM3")
    broker.create_topic("t3", description="Tópico de MOM3")

    broker.publish_to_queue("q3", "Mensaje en q3 desde MOM3", emisor="mom3")
    broker.publish_to_topic("t3", "Anuncio en t3 desde MOM3", emisor="mom3")

    # Replicar a MOM1
    replicator.replicate_create_queue("q3", description="Replica desde MOM3")
    replicator.replicate_create_topic("t3", description="Replica desde MOM3")

    replicator.replicate_publish_to_queue("q3", "Mensaje en q3 desde MOM3")
    replicator.replicate_publish_to_topic("t3", "Anuncio en t3 desde MOM3")

if __name__ == "__main__":
    simulate_data()
