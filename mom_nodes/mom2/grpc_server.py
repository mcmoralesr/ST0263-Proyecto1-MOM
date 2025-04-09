# mom_nodes/mom2/grpc_server.py

import grpc
from concurrent import futures
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../grpc')))

import mom_pb2
import mom_pb2_grpc
from mom_nodes.mom2.message_broker import broker

class ReplicationService(mom_pb2_grpc.ReplicationServiceServicer):
    def CreateQueue(self, request, context):
        broker.create_queue(request.name, description=request.description)
        return mom_pb2.Response(status=f"Queue '{request.name}' created.")

    def CreateTopic(self, request, context):
        broker.create_topic(request.name, description=request.description)
        return mom_pb2.Response(status=f"Topic '{request.name}' created.")

    def PublishToQueue(self, request, context):
        broker.publish_to_queue(request.name, request.message, emisor="replica")
        return mom_pb2.Response(status=f"Message sent to queue '{request.name}'.")

    def PublishToTopic(self, request, context):
        broker.publish_to_topic(request.name, request.message, emisor="replica")
        return mom_pb2.Response(status=f"Message published to topic '{request.name}'.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_ReplicationServiceServicer_to_server(ReplicationService(), server)
    server.add_insecure_port('[::]:50052')  # MOM2 escucha en puerto 50052
    server.start()
    print("✅ gRPC MOM2 server running on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
