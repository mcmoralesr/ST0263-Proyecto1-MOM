#!/bin/bash

SESSION="mom3"
PROJECT_DIR="ST0263-Proyecto1-MOM"

echo "🔁 Lanzando MOM3: REST (8003) + gRPC (50053)..."

# Activar entorno
cd $PROJECT_DIR || exit
source venv/bin/activate

# Crear sesión tmux si no existe
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION

  # Ventana 1: FastAPI
  tmux rename-window -t $SESSION 'fastapi'
  tmux send-keys -t $SESSION "PYTHONPATH=. uvicorn mom_nodes.mom3.mom3_server:app --host 0.0.0.0 --port 8003 --reload" C-m

  # Ventana 2: gRPC
  tmux new-window -t $SESSION -n 'grpc'
  tmux send-keys -t $SESSION "python3 -m mom_nodes.mom3.grpc_server" C-m
fi

tmux attach -t $SESSION

#./start_mom3.sh 