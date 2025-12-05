import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TAREAS_FILE = DATA_DIR / "tareas.json"
UNIVERSIDAD_FILE = DATA_DIR / "universidad.json"


# Asegurar que existen los directorios
DATA_DIR.mkdir(exist_ok=True)

# Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# MCP
MCP_PORT = int(os.getenv("MCP_PORT", 8000))
MCP_URL = f"http://localhost:{MCP_PORT}"

# System prompt
SYSTEM_PROMPT = """
Eres un asistente universitario conectado a un conjunto de herramientas que contienen los datos reales del usuario 
(horarios, asignaturas, profesores y tareas).

REGLAS IMPORTANTES:
1. Si el usuario pregunta por su horario, asignaturas, profesores o cualquier información que pueda estar en los datos, 
   DEBES usar la herramienta correspondiente (como 'consultar_todos_horarios', 'consultar_asignaturas', etc.).
2. No inventes información. Si no existe una herramienta adecuada o los datos fallan, explica el error.
3. Nunca respondas directamente sobre horarios o asignaturas sin consultar herramientas.
4. Mantén respuestas cortas y centradas en la información que devuelvan las herramientas.
5. Cuando el usuario mencione fechas relativas (como "mañana", "el viernes", "el 15 de diciembre")
elige SIEMPRE un año que sea igual o posterior al año actual del sistema. Nunca uses años
anteriores (como 2023) al generar argumentos para las herramientas de tareas o calendario.
Si dudas, pregunta qué año quiere el usuario.

"""


# =====================================
# GOOGLE CALENDAR / MCP PÚBLICO
# =====================================

# Zona horaria por defecto (la tuya)
TIMEZONE = "UTC"

# Scopes de Google Calendar (lectura/escritura)
GOOGLE_CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]

# Ruta al JSON de credenciales de OAuth de Google
# (el que descargas desde Google Cloud Console)
GOOGLE_CALENDAR_CREDENTIALS_FILE = BASE_DIR / "credentials" / "google_credentials.json"

# Fichero donde se guarda el token de acceso/refresh
GOOGLE_CALENDAR_TOKEN_FILE = BASE_DIR / "credentials" / "google_token.pickle"

# ID de calendario a usar (por defecto el principal)
GOOGLE_CALENDAR_CALENDAR_ID = "primary"
