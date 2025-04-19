
# mom_nodes/supervisor/grpc_server.py

import grpc
from concurrent import futures
import time
import mom_pb2
import mom_pb2_grpc
from mom_nodes.supervisor.message_backup import backup

class SupervisorServicer(mom_pb2_grpc.MOMReplicatorServicer):
    def CreateQueue(self, request, context):
        backup.backup_queue(request.name, "[CREATED]")
        return mom_pb2.StatusResponse(success=True)

    def EnqueueMessage(self, request, context):
        backup.backup_queue(request.name, request.content)
        return mom_pb2.StatusResponse(success=True)

    def CreateTopic(self, request, context):
        backup.backup_topic(request.name, "[CREATED]")
        return mom_pb2.StatusResponse(success=True)

    def PublishMessage(self, request, context):
        backup.backup_topic(request.name, request.content)
        return mom_pb2.StatusResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_MOMReplicatorServicer_to_server(SupervisorServicer(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("[SUPERVISOR] gRPC server listening on port 50054")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
