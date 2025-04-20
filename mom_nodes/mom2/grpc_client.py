# mom_nodes/mom1/grpc_client.py
import grpc
from mom_nodes.mom1 import mom_pb2 as pb, mom_pb2_grpc as pb_grpc

MOM_GRPC_SERVERS = [
    "54.163.98.1:50051",  # mom3
    "52.23.81.232:50051",  # mom2
]

def replicar_crear_topico(nombre, descripcion):
    for address in MOM_GRPC_SERVERS:
        try:
            channel = grpc.insecure_channel(address)
            stub = pb_grpc.ReplicationServiceStub(channel)
            request = pb.TopicRequest(topic=nombre, description=descripcion)
            response = stub.ReplicateCreateTopic(request)
            print(f"[gRPC] {address} => {response.status}")
        except grpc.RpcError as e:
            print(f"[gRPC ERROR] {address}: {e}")

def replicar_crear_cola(nombre, descripcion):
    for address in MOM_GRPC_SERVERS:
        try:
            channel = grpc.insecure_channel(address)
            stub = pb_grpc.ReplicationServiceStub(channel)
            request = pb.QueueRequest(queue=nombre, description=descripcion)
            response = stub.ReplicateCreateQueue(request)
            print(f"[gRPC] {address} => {response.status}")
        except grpc.RpcError as e:
            print(f"[gRPC ERROR] {address}: {e}")

def replicar_publicar_en_topico(nombre, mensaje):
    for address in MOM_GRPC_SERVERS:
        try:
            channel = grpc.insecure_channel(address)
            stub = pb_grpc.ReplicationServiceStub(channel)
            request = pb.MessageRequest(name=nombre, message=mensaje)
            response = stub.ReplicatePublishToTopic(request)
            print(f"[gRPC] {address} => {response.status}")
        except grpc.RpcError as e:
            print(f"[gRPC ERROR] {address}: {e}")

def replicar_publicar_en_cola(nombre, mensaje):
    for address in MOM_GRPC_SERVERS:
        try:
            channel = grpc.insecure_channel(address)
            stub = pb_grpc.ReplicationServiceStub(channel)
            request = pb.MessageRequest(name=nombre, message=mensaje)
            response = stub.ReplicatePublishToQueue(request)
            print(f"[gRPC] {address} => {response.status}")
        except grpc.RpcError as e:
            print(f"[gRPC ERROR] {address}: {e}")
