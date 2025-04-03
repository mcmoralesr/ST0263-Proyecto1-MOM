# info de la materia: ST0263 <Tópicos especiales en telemático>
#
# Estudiante(s): Manuel Arango Gomez - marangog3@eafit.edu.co
# Sebastián Cano Rincón - scanor2@eafit.edu.co
# Maria Camila Morales - mcmorales@eafit.edu.co
#
# Profesor: Alvaro Enrique Ospina Sanjuan - aeospinas@eafit.brightspace.com


# PROYECTO 1: Diseño e Implementación de un Middleware que Implemente un Servicio de Mensajería Asincrónica entre Aplicaciones
#
# 1. breve descripción de la actividad
El objetivo del proyecto es diseñar e implementar un Middleware Orientado a Mensajes (MOM), que permita a un conjunto de clientes comunicarse de manera asincrónica usando colas y tópicos replicados en un clúster de nodos MOM. El MOM maneja funcionalidades como: autenticación, gestión de colas y tópicos, envío y recepción de mensajes, y replicación entre nodos usando gRPC.
#
<texto descriptivo>
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Arquitectura distribuida de 3 MOMs en clúster

Comunicación REST cliente-MOM

Comunicación gRPC entre MOMs

Replicación activa con modelo push

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
C++ (C++17)
#Librerías y paquetes

Crow (v1.0+1) - Para implementar la API REST que comunica a los clientes con el Middleware MOM, se utilizó Crow, un microframework web en C++ ligero, moderno y eficiente, ideal para exponer endpoints RESTful desde un servidor C++. El cliente frontend (carpeta revistas-app/) se conecta a esta API para interactuar con los tópicos y colas.

SQLite3

Boost

CMake

# Requisitos por sistema operativo
🔵 macOS (Apple Silicon o Intel)

brew install sqlite3 boost cmake
curl -L https://github.com/CrowCpp/Crow/releases/download/v1.0%2B1/crow_all.h -o crow_all.h

Compilación:

clang++ mom1_server.cpp -o mom1_server \
  -I/usr/local/include -L/usr/local/lib \
  -lsqlite3 -lboost_system -lpthread
Si se usa Apple Silicon, puede que se necesite reemplazar /usr/local por /opt/homebrew.

🟢 Linux (Ubuntu / Debian / WSL)

sudo apt update
sudo apt install build-essential libsqlite3-dev libboost-system-dev cmake curl
curl -L https://github.com/CrowCpp/Crow/releases/download/v1.0%2B1/crow_all.h -o crow_all.h

Compilación:

g++ mom1_server.cpp -o mom1_server \
  -lsqlite3 -lboost_system -lpthread
  
🟠 Windows (con WSL o MinGW)

Instala WSL + Ubuntu (recomendado)
o usa MSYS2 / MinGW + Boost precompilado

En WSL:

sudo apt install build-essential libsqlite3-dev libboost-system-dev cmake curl
curl -L https://github.com/CrowCpp/Crow/releases/download/v1.0%2B1/crow_all.h -o crow_all.h
g++ mom1_server.cpp -o mom1_server -lsqlite3 -lboost_system -lpthread

En MSYS2:
pacman -S mingw-w64-x86_64-boost mingw-w64-x86_64-sqlite3
g++ mom1_server.cpp -o mom1_server -lsqlite3 -lboost_system -lws2_32 -lshlwapi

## como se compila y ejecuta.
## detalles del desarrollo.
## detalles técnicos
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## url de donde tomo info para desarrollar este proyecto

## https://crowcpp.org

## https://www.sqlite.org

## https://grpc.io

## https://github.com/CrowCpp/Crow
