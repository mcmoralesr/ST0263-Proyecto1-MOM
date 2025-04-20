# mom_nodes/mom1/data_simulation.py
from mom_nodes.mom1.message_broker import broker
from mom_nodes.mom1 import grpc_client

def simulate_data():
    broker.create_queue("q1", description="Cola principal MOM1")
    broker.create_topic("t1", description="Tópico principal MOM1")

    broker.publish_to_queue("q1", "Mensaje q1 publicado por MOM1", emisor="mom1")
    broker.publish_to_topic("t1", "Noticia t1 publicada por MOM1", emisor="mom1")

    grpc_client.replicar_crear_cola("q1", "Cola principal MOM1")
    grpc_client.replicar_crear_topico("t1", "Tópico principal MOM1")
    grpc_client.replicar_publicar_en_cola("q1", "Mensaje q1 publicado por MOM1")
    grpc_client.replicar_publicar_en_topico("t1", "Noticia t1 publicada por MOM1")

if __name__ == "__main__":
    simulate_data()

