# status_checker.py

import socket

NODES = {
    "MOM1": {
        "gRPC": "52.203.79.134:50051",
        "REST": "52.203.79.134:8001"
    },
    "MOM2": {
        "gRPC": "52.23.81.232:50052",
        "REST": "52.23.81.232:8002"
    },
    "MOM3": {
        "gRPC": "54.163.98.1:50053",
        "REST": "54.163.98.1:8003"
    }
}

def check_connection(host: str, port: int, timeout=1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

for node, services in NODES.items():
    grpc_host, grpc_port = services["gRPC"].split(":")
    rest_host, rest_port = services["REST"].split(":")

    grpc_status = "🟢" if check_connection(grpc_host, int(grpc_port)) else "🔴"
    rest_status = "🟢" if check_connection(rest_host, int(rest_port)) else "🔴"

    print(f"{grpc_status} {node} gRPC ({services['gRPC']})")
    print(f"{rest_status} {node} REST ({services['REST']})")
    print("-" * 50)
