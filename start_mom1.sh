#!/bin/bash

SESSION="mom1"
PROJECT_DIR="ST0263-Proyecto1-MOM"

echo " Lanzando MOM1: REST (8001) + gRPC (50051)..."

# Activar entorno
cd $PROJECT_DIR || exit
source venv/bin/activate

# Crear sesión tmux si no existe
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION

  # Ventana 1: FastAPI
  tmux rename-window -t $SESSION 'fastapi'
  tmux send-keys -t $SESSION "PYTHONPATH=. uvicorn mom_nodes.mom1.mom1_server:app --host 0.0.0.0 --port 8001 --reload" C-m

  # Ventana 2: gRPC
  tmux new-window -t $SESSION -n 'grpc'
  tmux send-keys -t $SESSION "python3 -m mom_nodes.mom1.grpc_server" C-m
fi

tmux attach -t $SESSION
