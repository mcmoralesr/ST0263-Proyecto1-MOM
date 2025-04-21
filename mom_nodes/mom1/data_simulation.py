# mom_nodes/mom1/data_simulation.py

import threading
import time
from mom_nodes.mom1 import grpc_client
from mom_nodes.mom1.grpc_server import serve


def replicate_all():
    grpc_client.replicar_crear_cola("q1", "mom1")
    grpc_client.replicar_crear_topico("t1", "mom1")
    grpc_client.replicar_publicar_en_cola("q1", "Mensaje replicado en cola", "mom1")
    grpc_client.replicar_publicar_en_topico("t1", "Mensaje replicado en tópico", "mom1")


if __name__ == "__main__":
    threading.Thread(target=serve, daemon=True).start()
    time.sleep(2)
    replicate_all()
