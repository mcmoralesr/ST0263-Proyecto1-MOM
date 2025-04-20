#!/bin/bash
echo "🚀 Lanzando todos los servicios..."

# Directorio raíz del proyecto
PROJECT_DIR=$(pwd)

# Lanzar gRPC MOM1
echo "🛰️ Iniciando gRPC MOM1..."
nohup python3 -m mom_nodes.mom1.grpc_server > grpc_mom1.log 2>&1 &

# Lanzar REST MOM1
echo "🔧 Iniciando REST MOM1 (FastAPI)..."
nohup python3 -m mom_nodes.mom1.mom1_server > mom1_api.log 2>&1 &

# Lanzar gRPC MOM2
echo "🛰️ Iniciando gRPC MOM2..."
nohup python3 -m mom_nodes.mom2.grpc_server > grpc_mom2.log 2>&1 &

# Lanzar REST MOM2
echo "🔧 Iniciando REST MOM2 (FastAPI)..."
nohup python3 -m mom_nodes.mom2.mom2_server > mom2_api.log 2>&1 &

# Lanzar gRPC MOM3
echo "🛰️ Iniciando gRPC MOM3..."
nohup python3 -m mom_nodes.mom3.grpc_server > grpc_mom3.log 2>&1 &

# Lanzar REST MOM3
echo "🔧 Iniciando REST MOM3 (FastAPI)..."
nohup python3 -m mom_nodes.mom3.mom3_server > mom3_api.log 2>&1 &

echo "✅ Todos los servicios fueron lanzados correctamente. Puedes revisar los logs en *.log"
