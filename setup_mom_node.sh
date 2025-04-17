#!/bin/bash

echo " Iniciando setup para nodo MOM..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3-pip python3-venv git

# Clonar el repositorio
if [ ! -d "ST0263-Proyecto1-MOM" ]; then
    git clone https://github.com/mcmoralesr/ST0263-Proyecto1-MOM.git
fi

cd ST0263-Proyecto1-MOM

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

# Crear carpetas necesarias si no existen
mkdir -p grpc
mkdir -p supervisor
mkdir -p mom_nodes/mom1 mom_nodes/mom2 mom_nodes/mom3

# Añadir __init__.py si faltan
touch grpc/__init__.py
touch supervisor/__init__.py
touch mom_nodes/__init__.py
touch mom_nodes/mom1/__init__.py
touch mom_nodes/mom2/__init__.py
touch mom_nodes/mom3/__init__.py

echo " Setup completado. Activa el entorno con: source venv/bin/activate"

#chmod +x setup_mom_node.sh ./setup_mom_node.sh en EC2
