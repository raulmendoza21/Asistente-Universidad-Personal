# Asistente Universidad Personal

Autores: Raul Mendoza, Nestor Ortega\
Asignatura: Procesamiento del Lenguaje Natural (PLN)\
Universidad de Las Palmas de Gran Canaria (ULPGC)

## Descripcion

Asistente Universidad Personal es una aplicacion en Python disenada para
ayudar a estudiantes universitarios a gestionar informacion academica y
tareas mediante un agente conversacional basado en Qwen 2.5-Instruct con
soporte nativo para llamadas a herramientas (tool calling).

El sistema permite consultar horarios, profesores, aulas, crear tareas,
listarlas, completarlas y mantener un historial conversacional
persistente durante la sesion. Todo ello se ejecuta mediante linea de
comandos (CLI) con una interfaz clara y funcional.

## Caracteristicas principales

-   Agente conversacional Qwen 2.5-Instruct mediante API de HuggingFace.
-   Soporte completo para tool calling.
-   Gestor de tareas con almacenamiento en formato JSON.
-   Consulta de horarios, profesores y aulas desde datos locales.
-   Sistema de comandos a traves de una interfaz en linea de comandos.
-   Carga de configuracion mediante variables de entorno en archivo
    .env.
-   Implementacion modular que facilita ampliaciones y mantenimiento.

## Requisitos

-   Python 3.10 o superior.
-   Cuenta de HuggingFace con token de acceso valido.
-   Bibliotecas incluidas en requirements.txt.

## Instalacion

1.  Clonar el repositorio:

git clone
https://github.com/raulmendoza21/Asistente-Universidad-Personal.git cd
Asistente-Universidad-Personal

2.  Crear un entorno virtual:

Windows PowerShell:

python -m venv venv venv`\Scripts`{=tex}`\Activate`{=tex}.ps1

Linux o macOS:

python3 -m venv venv source venv/bin/activate

3.  Instalar las dependencias:

pip install -r requirements.txt

4.  Crear el archivo .env con las variables necesarias:

HF_TOKEN=tu_token_de_huggingface MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

Guardar el archivo con codificacion UTF-8.

## Estructura del proyecto

Asistente-Universidad-Personal/ \|-- main.py \|-- agent.py \|--
mcp_server.py \|-- data_manager.py \|-- config.py \|-- utils.py \|--
data/ \| \|-- tareas.json \| \|-- universidad.json \|-- requirements.txt
\|-- .env \|-- README.md

## Ejecucion

Para iniciar el asistente:

python main.py

## Uso y comandos

Consultar informacion: Que clase tengo el lunes

Crear tareas: Recuerdame entregar la practica el 15 de diciembre

Listar tareas: Muestrame mis tareas pendientes

Completar tareas: Marca la tarea 1 como completada

Comandos especiales: /reset /salir

## Autores

Raul Mendoza\
Nestor Ortega\
Asignatura: Procesamiento del Lenguaje Natural (PLN)\
Universidad de Las Palmas de Gran Canaria (ULPGC)