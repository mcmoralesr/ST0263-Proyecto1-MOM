
# mom_nodes/supervisor/grpc_client.py

import grpc
import mom_pb2
import mom_pb2_grpc

class MOMClient:
    def __init__(self, targets):
        self.targets = targets

    def send_queue_message(self, queue_name, message):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.EnqueueMessage(mom_pb2.QueueMessage(name=queue_name, content=message))
            except Exception as e:
                print(f"[Supervisor] Error replicating to {target}: {e}")

    def send_topic_message(self, topic_name, message):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.PublishMessage(mom_pb2.TopicMessage(name=topic_name, content=message))
            except Exception as e:
                print(f"[Supervisor] Error replicating to {target}: {e}")

# Ejemplo de uso:
# client = MOMClient(["52.203.79.134:50051", "52.23.81.232:50052", "54.163.98.1:50053"])
# client.send_queue_message("backup_q", "mensaje de respaldo")
