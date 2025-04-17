#!/bin/bash

SESSION="mom2"
PROJECT_DIR="ST0263-Proyecto1-MOM"

echo "🔁 Lanzando MOM2: REST (8002) + gRPC (50052)..."

# Activar entorno
cd $PROJECT_DIR || exit
source venv/bin/activate

# Crear sesión tmux si no existe
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION

  # Ventana 1: FastAPI
  tmux rename-window -t $SESSION 'fastapi'
  tmux send-keys -t $SESSION "PYTHONPATH=. uvicorn mom_nodes.mom2.mom2_server:app --host 0.0.0.0 --port 8002 --reload" C-m

  # Ventana 2: gRPC
  tmux new-window -t $SESSION -n 'grpc'
  tmux send-keys -t $SESSION "python3 -m mom_nodes.mom2.grpc_server" C-m
fi

tmux attach -t $SESSION

#./start_mom2.sh
