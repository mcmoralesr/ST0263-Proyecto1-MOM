# mom_nodes/supervisor/mom_monitor.py

import grpc
import time
import threading
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../grpc')))
import mom_pb2
import mom_pb2_grpc

class MOMMonitor:
    def __init__(self, targets):
        self.targets = targets
        self.status = {name: "unknown" for name in targets}

    def check_mom(self, name, address):
        try:
            with grpc.insecure_channel(address) as channel:
                stub = mom_pb2_grpc.ReplicationServiceStub(channel)
                response = stub.Ping(mom_pb2.Empty())
                self.status[name] = response.status
        except Exception:
            self.status[name] = "offline"

    def loop(self, interval=5):
        while True:
            for name, addr in self.targets.items():
                self.check_mom(name, addr)
            time.sleep(interval)

    def start_background(self):
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

# Ejemplo de uso dentro de FastAPI:
MONITOR_TARGETS = {
    "mom1": "localhost:50051",
    "mom2": "localhost:50052",
    "mom3": "localhost:50053"
}

monitor = MOMMonitor(MONITOR_TARGETS)
