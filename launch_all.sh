
#!/bin/bash

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

log() {
  echo -e "[$(date +'%H:%M:%S')] $1"
}

log "🚀 Lanzando todos los servicios..."

log "🛸 Iniciando gRPC MOM1..."
nohup python3 -m mom_nodes.mom1.grpc_server > "$LOG_DIR/grpc_mom1.log" 2>&1 &

log "🔧 Iniciando REST MOM1 (FastAPI)..."
nohup python3 -m mom_nodes.mom1.mom1_server > "$LOG_DIR/mom1_api.log" 2>&1 &

log "🛸 Iniciando gRPC MOM2..."
nohup python3 -m mom_nodes.mom2.grpc_server > "$LOG_DIR/grpc_mom2.log" 2>&1 &

log "🔧 Iniciando REST MOM2 (FastAPI)..."
nohup python3 -m mom_nodes.mom2.mom2_server > "$LOG_DIR/mom2_api.log" 2>&1 &

log "🛸 Iniciando gRPC MOM3..."
nohup python3 -m mom_nodes.mom3.grpc_server > "$LOG_DIR/grpc_mom3.log" 2>&1 &

log "🔧 Iniciando REST MOM3 (FastAPI)..."
nohup python3 -m mom_nodes.mom3.mom3_server > "$LOG_DIR/mom3_api.log" 2>&1 &

log "✅ Todos los servicios fueron lanzados correctamente. Revisa la carpeta 'logs/' para verificar su estado."
