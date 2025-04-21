# mom_nodes/mom1/grpc_client.py

import grpc
from grpc_files import message_pb2 as pb2
from grpc_files import message_pb2_grpc as pb2_grpc

MOM2 = "52.23.81.232:50052"
MOM3 = "54.163.98.1:50053"

def get_stub(addr):
    channel = grpc.insecure_channel(addr)
    return pb2_grpc.ReplicationServiceStub(channel)


def replicar_crear_cola(name, user):
    request = pb2.QueueRequest(name=name, user=user)
    for addr in [MOM2, MOM3]:
        try:
            stub = get_stub(addr)
            response = stub.ReplicateCreateQueue(request)
            print(f"[✔] Cola replicada a {addr}: {response.status}")
        except Exception as e:
            print(f"[✘] Error replicando cola a {addr}: {e}")


def replicar_crear_topico(name, user):
    request = pb2.TopicRequest(name=name, user=user)
    for addr in [MOM2, MOM3]:
        try:
            stub = get_stub(addr)
            response = stub.ReplicateCreateTopic(request)
            print(f"[✔] Tópico replicado a {addr}: {response.status}")
        except Exception as e:
            print(f"[✘] Error replicando tópico a {addr}: {e}")


def replicar_publicar_en_cola(name, message, user):
    request = pb2.MessageRequest(name=name, message=message, user=user)
    for addr in [MOM2, MOM3]:
        try:
            stub = get_stub(addr)
            response = stub.ReplicatePublishToQueue(request)
            print(f"[✔] Mensaje en cola replicado a {addr}: {response.status}")
        except Exception as e:
            print(f"[✘] Error replicando mensaje a {addr}: {e}")


def replicar_publicar_en_topico(name, message, user):
    request = pb2.MessageRequest(name=name, message=message, user=user)
    for addr in [MOM2, MOM3]:
        try:
            stub = get_stub(addr)
            response = stub.ReplicatePublishToTopic(request)
            print(f"[✔] Mensaje en tópico replicado a {addr}: {response.status}")
        except Exception as e:
            print(f"[✘] Error replicando mensaje a {addr}: {e}")
