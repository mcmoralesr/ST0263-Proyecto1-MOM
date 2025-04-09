# mom_nodes/mom2/data_simulation.py

from mom_nodes.mom2.message_broker import broker
from mom_nodes.mom2.grpc_client import replicator

def simulate_data():
    # Propias de MOM2
    broker.create_queue("q2", description="Cola exclusiva de MOM2")
    broker.create_topic("t2", description="Tópico exclusivo de MOM2")

    broker.publish_to_queue("q2", "Mensaje propio de q2 - MOM2", emisor="mom2")
    broker.publish_to_topic("t2", "Noticia propia de t2 - MOM2", emisor="mom2")

    # Replicar a MOM3
    replicator.replicate_create_queue("q2", description="Replica desde MOM2")
    replicator.replicate_create_topic("t2", description="Replica desde MOM2")

    replicator.replicate_publish_to_queue("q2", "Mensaje propio de q2 - MOM2")
    replicator.replicate_publish_to_topic("t2", "Noticia propia de t2 - MOM2")
