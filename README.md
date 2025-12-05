# Asistente Universidad Personal

Autores: Raul Mendoza, Nestor Ortega  
Asignatura: Procesamiento del Lenguaje Natural (PLN)  
Universidad de Las Palmas de Gran Canaria (ULPGC)

## Descripcion

Asistente Universidad Personal es una aplicacion en Python disenada para
ayudar a estudiantes universitarios a gestionar informacion academica y
tareas mediante un agente conversacional basado en el modelo Qwen 2.5-Instruct
(vía HuggingFace) con soporte nativo para llamadas a herramientas
(tool calling).

Aunque el enunciado de la practica menciona el uso de la API de OpenAI,
este proyecto utiliza Qwen 2.5-Instruct a traves de la Inference API de
HuggingFace, opcion aceptada por el profesor para el desarrollo de la
practica.

El sistema permite:

- Consultar horarios, profesores y aulas desde datos locales en JSON.
- Crear, listar, completar y eliminar tareas almacenadas en JSON.
- Consultar y gestionar eventos en Google Calendar mediante herramientas
  especificas.
- Mantener un historial conversacional durante la sesion para dar
  respuestas coherentes con el contexto.

La interaccion se realiza mediante linea de comandos (CLI), lo que permite
observar claramente las peticiones al modelo, las llamadas a herramientas
y el flujo conversacional completo.

## Caracteristicas principales

- Agente conversacional basado en Qwen 2.5-Instruct mediante API de HuggingFace.
- Soporte completo para tool calling (formato de funciones tipo OpenAI).
- Servidor FastMCP que expone herramientas para:
  - Consultar horarios, profesores y aulas.
  - Gestionar tareas (crear, listar, completar, eliminar) en un archivo JSON.
  - Gestionar eventos en Google Calendar (listar, crear, eliminar).
- Conversacion con historial persistente durante la sesion.
- Interfaz en linea de comandos con mensajes legibles y estructurados.
- Configuracion mediante variables de entorno en archivo .env.

## Requisitos

- Python 3.10 o superior.
- Cuenta de HuggingFace con token de acceso valido.
- Credenciales validas de Google Cloud para usar Google Calendar
  (fichero JSON de OAuth 2.0 y token generado).
- Bibliotecas incluidas en requirements.txt.

## Instalacion

1. Clonar el repositorio

   git clone https://github.com/raulmendoza21/Asistente-Universidad-Personal.git
   cd Asistente-Universidad-Personal

2. Crear un entorno virtual

   Windows (PowerShell):

     python -m venv venv
     .\venv\Scripts\Activate.ps1

   Linux o macOS:

     python3 -m venv venv
     source venv/bin/activate

3. Instalar las dependencias

   pip install -r requirements.txt

4. Configurar el archivo .env

   Crear un archivo llamado .env en la raiz del proyecto con al menos:

   HF_TOKEN=tu_token_de_huggingface
   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
   MCP_PORT=8000

   El token de HuggingFace se obtiene en:
   https://huggingface.co/settings/tokens

5. Configurar credenciales de Google Calendar

   - Crear un proyecto en Google Cloud Console.
   - Activar la API de Google Calendar.
   - Crear credenciales de tipo "Aplicacion de escritorio" (OAuth 2.0).
   - Descargar el JSON de credenciales y guardarlo en:

     credentials/google_credentials.json

   La primera vez que se utilice Google Calendar, se abrira una ventana
   de navegador para autorizar el acceso y se generara automaticamente
   el fichero de token en:

     credentials/google_token.pickle

## Estructura del proyecto

Asistente-Universidad-Personal/
  agent.py                 Logica del agente Qwen y tool calling
  main.py                  Aplicacion CLI (punto de entrada)
  mcp_server.py            Servidor FastMCP con las herramientas
  data_manager.py          Gestion de datos locales (JSON)
  config.py                Configuracion general y rutas
  utils.py                 Funciones auxiliares de formato y fechas
  data/
    tareas.json            Almacen local de tareas
    universidad.json       Datos de ejemplo de horarios, profesores y aulas
  requirements.txt         Dependencias del proyecto
  .env                     Variables de entorno (no se sube al repositorio)
  README.md                Documentacion del proyecto

## Ejecucion

1. Asegurarse de tener el entorno virtual activado y las dependencias instaladas.
2. Comprobar que el archivo .env contiene un token HF_TOKEN valido.
3. Ejecutar la aplicacion desde la raiz del proyecto:

   python main.py

Si el token es valido y la conexion con HuggingFace funciona, se iniciara
el asistente y se mostrara un banner en la consola.

## Uso y ejemplos de comandos

Una vez iniciado el programa, se puede interactuar escribiendo mensajes
en lenguaje natural. Algunos ejemplos:

- Horarios y universidad:
  - Que clases tengo de Inteligencia Artificial el lunes
  - Muestrame todos los horarios de este cuatrimestre

- Profesores y aulas:
  - Quien imparte Bases de Datos
  - Donde esta el aula A-201

- Tareas locales (archivo JSON):
  - Crea una tarea para entregar la practica el 2025-12-15
  - Muestrame mis tareas pendientes
  - Marca la tarea 1 como completada
  - Elimina la tarea 2

- Google Calendar:
  - Que eventos tengo hoy en mi calendario
  - Crea un evento mañana a las 10:00 para estudiar MCP
  - Borra el evento del calendario que creaste para hoy

- Comandos especiales:
  - /reset  Reinicia la conversacion interna del agente
  - /salir  Cierra la aplicacion

## Notas sobre fechas y anos antiguos

El sistema esta configurado para evitar que se creen tareas o eventos
en anos pasados por error al usar expresiones como "hoy" o "manana".

- En el agente, el mensaje de sistema incluye siempre la fecha actual
  y se indica explicitamente que no se deben usar anos anteriores al
  actual salvo que el usuario lo pida.
- En la capa de utilidades y en el cliente de Google Calendar se
  normalizan las fechas para que, si el ano es menor que el actual,
  se adapte al ano actual o siguiente en caso de que la fecha ya haya
  pasado.

De esta forma, si el modelo propone por ejemplo una fecha en 2023,
el sistema ajusta el ano automaticamente para que coincida con el
contexto temporal real de la ejecucion.

## Autores

Raul Mendoza  
Nestor Ortega  
Asignatura: Procesamiento del Lenguaje Natural (PLN)  
Universidad de Las Palmas de Gran Canaria (ULPGC)
