import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ==========================
# RUTAS BASE Y ARCHIVOS
# ==========================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TAREAS_FILE = DATA_DIR / "tareas.json"
UNIVERSIDAD_FILE = DATA_DIR / "universidad.json"

# Asegurar que existe el directorio de datos
DATA_DIR.mkdir(exist_ok=True)

# ==========================
# HUGGING FACE / MODELO
# ==========================

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# ==========================
# MCP (FASTMCP)
# ==========================

# Puerto del servidor MCP (HTTP)
MCP_PORT = int(os.getenv("MCP_PORT", 8000))
MCP_URL = f"http://localhost:{MCP_PORT}/mcp"

# ==========================
# SYSTEM PROMPT DEL MODELO
# ==========================

SYSTEM_PROMPT = """
Eres un asistente universitario conectado a un conjunto de herramientas
que contienen los datos reales del usuario (horarios, asignaturas,
profesores, aulas y tareas), asi como acceso a su Google Calendar.

REGLAS IMPORTANTES:
1. Si el usuario pregunta por su horario, asignaturas, profesores, aulas
   o tareas, DEBES usar siempre la herramienta correspondiente
   (consultar_horario, consultar_todos_horarios, buscar_profesor,
   consultar_aula, listar_tareas, etc.).
2. No inventes informacion. Si no existe una herramienta adecuada o los
   datos fallan, explica el error de forma clara.
3. Nunca respondas directamente sobre horarios, asignaturas, profesores
   o aulas sin consultar las herramientas.
4. Mantén respuestas breves y centradas en la informacion que devuelvan
   las herramientas.
5. Cuando el usuario mencione fechas relativas (como "mañana",
   "el viernes", "el 15 de diciembre"), elige SIEMPRE un año que sea
   igual o posterior al año actual del sistema. Nunca uses años
   anteriores (como 2023) al generar argumentos para las herramientas
   de tareas o calendario. Si dudas, pregunta qué año quiere el usuario.
"""

# ==========================
# GOOGLE CALENDAR / ZONA HORARIA
# ==========================

# Zona horaria por defecto (se usa principalmente para Calendar; para el
# agente se hace un manejo robusto en caso de que esta zona no exista
# en el sistema).
TIMEZONE = "UTC"

# Scopes de Google Calendar (lectura/escritura)
GOOGLE_CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]

# Ruta al JSON de credenciales de OAuth de Google
GOOGLE_CALENDAR_CREDENTIALS_FILE = BASE_DIR / "credentials" / "google_credentials.json"

# Fichero donde se guarda el token de acceso/refresh
GOOGLE_CALENDAR_TOKEN_FILE = BASE_DIR / "credentials" / "google_token.pickle"

# ID de calendario a usar (por defecto el principal)
GOOGLE_CALENDAR_CALENDAR_ID = "primary"
