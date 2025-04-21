# mom_nodes/mom1/grpc_server.py

import grpc
from concurrent import futures
import message_pb2 as pb
import message_pb2_grpc as pb_grpc
from mom_nodes.mom1 import message_broker


class ReplicationServicer(pb_grpc.ReplicationServiceServicer):
    def ReplicateCreateTopic(self, request, context):
        message_broker.broker.create_topic(request.name, description="replicado")
        return pb.ReplicationReply(status="OK", error="")

    def ReplicateCreateQueue(self, request, context):
        message_broker.broker.create_queue(request.name, description="replicado")
        return pb.ReplicationReply(status="OK", error="")

    def ReplicatePublishToTopic(self, request, context):
        message_broker.broker.publish_to_topic(request.name, request.message, user="replica")
        return pb.ReplicationReply(status="OK", error="")

    def ReplicatePublishToQueue(self, request, context):
        message_broker.broker.publish_to_queue(request.name, request.message, user="replica")
        return pb.ReplicationReply(status="OK", error="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_ReplicationServiceServicer_to_server(ReplicationServicer(), server)

    port = server.add_insecure_port('0.0.0.0:50051')
    if port == 0:
        print("❌ Fallo al hacer bind en 0.0.0.0:50051")
    else:
        print(f"🚀 MOM1 gRPC Server escuchando en 0.0.0.0:{port}")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

