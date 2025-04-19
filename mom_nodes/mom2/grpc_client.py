import grpc
import mom_pb2
import mom_pb2_grpc

class Replicator:
    def __init__(self):
        self.targets = ['54.163.98.1:50053', '52.203.79.134:50051']

    def replicate_queue(self, name):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.CreateQueue(mom_pb2.QueueRequest(name=name))
            except Exception:
                pass

    def replicate_queue_message(self, name, msg):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.EnqueueMessage(mom_pb2.QueueMessage(name=name, content=msg))
            except Exception:
                pass

    def replicate_topic(self, name):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.CreateTopic(mom_pb2.TopicRequest(name=name))
            except Exception:
                pass

    def replicate_topic_message(self, name, msg):
        for target in self.targets:
            try:
                with grpc.insecure_channel(target) as channel:
                    stub = mom_pb2_grpc.MOMReplicatorStub(channel)
                    stub.PublishMessage(mom_pb2.TopicMessage(name=name, content=msg))
            except Exception:
                pass

replicator = Replicator()
