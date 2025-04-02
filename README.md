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

Crow (v1.0+1)

SQLite3

Boost

CMake

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
