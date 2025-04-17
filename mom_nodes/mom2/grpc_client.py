# mom_nodes/mom2/grpc_client.py

import grpc
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../grpc')))
import mom_pb2
import mom_pb2_grpc

MOM1_ADDRESS = "localhost:50051"
MOM3_ADDRESS = "localhost:50053"

class MOMReplicator:
    def __init__(self, targets):
        self.targets = targets

    def _send(self, method, *args, **kwargs):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.ReplicationServiceStub(channel)
                    method(stub, *args, **kwargs)
            except Exception as e:
                print(f"⚠️ Error replicando en {target}: {e}")

    def replicate_create_queue(self, name, description=""):
        self._send(lambda stub: stub.CreateQueue(
            mom_pb2.QueueRequest(name=name, description=description)
        ))

    def replicate_create_topic(self, name, description=""):
        self._send(lambda stub: stub.CreateTopic(
            mom_pb2.TopicRequest(name=name, description=description)
        ))

    def replicate_publish_to_queue(self, name, message):
        self._send(lambda stub: stub.PublishToQueue(
            mom_pb2.PublishRequest(name=name, message=message)
        ))

    def replicate_publish_to_topic(self, name, message):
        self._send(lambda stub: stub.PublishToTopic(
            mom_pb2.PublishRequest(name=name, message=message)
        ))

replicator = MOMReplicator([MOM1_ADDRESS, MOM3_ADDRESS])
