# mom_nodes/mom1/grpc_server.py
import grpc
from concurrent import futures
from mom_nodes.mom1 import mom_pb2_grpc, mom_pb2, message_broker

class ReplicationService(mom_pb2_grpc.ReplicationServiceServicer):
    def ReplicateCreateQueue(self, request, context):
        message_broker.broker.create_queue(request.queue, request.description)
        return mom_pb2.ReplicationReply(status="OK")

    def ReplicateCreateTopic(self, request, context):
        message_broker.broker.create_topic(request.topic, request.description)
        return mom_pb2.ReplicationReply(status="OK")

    def ReplicatePublishToQueue(self, request, context):
        message_broker.broker.publish_to_queue(request.name, request.message, user="replicator")
        return mom_pb2.ReplicationReply(status="OK")

    def ReplicatePublishToTopic(self, request, context):
        message_broker.broker.publish_to_topic(request.name, request.message, user="replicator")
        return mom_pb2.ReplicationReply(status="OK")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_ReplicationServiceServicer_to_server(ReplicationService(), server)
    server.add_insecure_port('[::]:50051')
    print("[gRPC] MOM1 Replication server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
