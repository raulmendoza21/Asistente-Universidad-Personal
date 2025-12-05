#!/usr/bin/env python3
"""
Asistente Universitario Personal con Qwen2.5-72B-Instruct + FastMCP (modo servidor/cliente)
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint  # noqa: F401
import sys

from agent import QwenAgent
from mcp_client_wrapper import call_mcp_tool


console = Console()


def print_banner():
    """Muestra el banner de inicio"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║   🎓 ASISTENTE UNIVERSITARIO PERSONAL 🎓    ║
    ║                                              ║
    ║   Powered by Qwen2.5-72B + FastMCP          ║
    ╚══════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


# ==============================
# WRAPPERS QUE LLAMAN AL MCP SERVER
# ==============================

def tool_consultar_horario(asignatura: str):
    return call_mcp_tool("consultar_horario", asignatura=asignatura)


def tool_consultar_todos_horarios():
    return call_mcp_tool("consultar_todos_horarios")


def tool_buscar_profesor(nombre: str):
    return call_mcp_tool("buscar_profesor", nombre=nombre)


def tool_consultar_aula(codigo_aula: str):
    return call_mcp_tool("consultar_aula", codigo_aula=codigo_aula)


def tool_crear_tarea(
    titulo: str,
    fecha_vencimiento: str,
    descripcion: str = "",
    prioridad: str = "media",
):
    return call_mcp_tool(
        "crear_tarea",
        titulo=titulo,
        fecha_vencimiento=fecha_vencimiento,
        descripcion=descripcion,
        prioridad=prioridad,
    )


def tool_listar_tareas(filtro: str = "pendientes"):
    return call_mcp_tool("listar_tareas", filtro=filtro)


def tool_completar_tarea(id_tarea: int):
    return call_mcp_tool("completar_tarea", id_tarea=id_tarea)


def tool_eliminar_tarea(id_tarea: int):
    return call_mcp_tool("eliminar_tarea", id_tarea=id_tarea)


def tool_listar_eventos_calendario(
    fecha_inicio: str,
    fecha_fin: str,
    max_resultados: int = 10,
):
    return call_mcp_tool(
        "listar_eventos_calendario",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        max_resultados=max_resultados,
    )


def tool_crear_evento_calendario(
    titulo: str,
    fecha_inicio: str,
    fecha_fin: str,
    descripcion: str | None = None,
    ubicacion: str | None = None,
):
    return call_mcp_tool(
        "crear_evento_calendario",
        titulo=titulo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        descripcion=descripcion,
        ubicacion=ubicacion,
    )


def tool_eliminar_evento_calendario(event_id: str):
    return call_mcp_tool("eliminar_evento_calendario", event_id=event_id)


# ==============================
# REGISTRO DE HERRAMIENTAS EN EL AGENTE
# ==============================

def register_tools(agent: QwenAgent):
    """Registra todas las herramientas MCP (vía cliente) en el agente"""

    # ----- Consulta de datos universitarios -----

    agent.register_tool(
        name="consultar_horario",
        function=tool_consultar_horario,
        description="Consulta el horario de una asignatura específica",
        parameters={
            "type": "object",
            "properties": {
                "asignatura": {
                    "type": "string",
                    "description": "Nombre de la asignatura"
                }
            },
            "required": ["asignatura"]
        }
    )

    agent.register_tool(
        name="consultar_todos_horarios",
        function=tool_consultar_todos_horarios,
        description="Obtiene el horario completo de todas las asignaturas",
        parameters={"type": "object", "properties": {}}
    )

    agent.register_tool(
        name="buscar_profesor",
        function=tool_buscar_profesor,
        description="Busca información sobre un profesor",
        parameters={
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Nombre del profesor a buscar"
                }
            },
            "required": ["nombre"]
        }
    )

    agent.register_tool(
        name="consultar_aula",
        function=tool_consultar_aula,
        description="Obtiene información sobre un aula",
        parameters={
            "type": "object",
            "properties": {
                "codigo_aula": {
                    "type": "string",
                    "description": "Código del aula (ej: A-201)"
                }
            },
            "required": ["codigo_aula"]
        }
    )

    # ----- Gestión de tareas -----

    agent.register_tool(
        name="crear_tarea",
        function=tool_crear_tarea,
        description="Crea una nueva tarea o recordatorio",
        parameters={
            "type": "object",
            "properties": {
                "titulo": {
                    "type": "string",
                    "description": "Título de la tarea"
                },
                "fecha_vencimiento": {
                    "type": "string",
                    "description": "Fecha de vencimiento (YYYY-MM-DD)"
                },
                "descripcion": {
                    "type": "string",
                    "description": "Descripción de la tarea (opcional)"
                },
                "prioridad": {
                    "type": "string",
                    "enum": ["baja", "media", "alta"],
                    "description": "Prioridad de la tarea"
                }
            },
            "required": ["titulo", "fecha_vencimiento"]
        }
    )

    agent.register_tool(
        name="listar_tareas",
        function=tool_listar_tareas,
        description="Lista las tareas según un filtro",
        parameters={
            "type": "object",
            "properties": {
                "filtro": {
                    "type": "string",
                    "enum": ["todas", "pendientes", "completadas"],
                    "description": "Filtro para las tareas"
                }
            }
        }
    )

    agent.register_tool(
        name="completar_tarea",
        function=tool_completar_tarea,
        description="Marca una tarea como completada",
        parameters={
            "type": "object",
            "properties": {
                "id_tarea": {
                    "type": "integer",
                    "description": "ID de la tarea a completar"
                }
            },
            "required": ["id_tarea"]
        }
    )

    agent.register_tool(
        name="eliminar_tarea",
        function=tool_eliminar_tarea,
        description="Elimina una tarea",
        parameters={
            "type": "object",
            "properties": {
                "id_tarea": {
                    "type": "integer",
                    "description": "ID de la tarea a eliminar"
                }
            },
            "required": ["id_tarea"]
        }
    )

    # ----- Google Calendar -----

    agent.register_tool(
        name="listar_eventos_calendario",
        function=tool_listar_eventos_calendario,
        description=(
            "Lista eventos del Google Calendar del usuario entre dos fechas y horas. "
            "Úsalo cuando el usuario quiera saber qué tiene en su calendario "
            "en un rango de tiempo concreto."
        ),
        parameters={
            "type": "object",
            "properties": {
                "fecha_inicio": {
                    "type": "string",
                    "description": (
                        "Fecha y hora de inicio en formato 'YYYY-MM-DD HH:MM'. "
                        "Ejemplo: '2025-11-28 09:00'"
                    )
                },
                "fecha_fin": {
                    "type": "string",
                    "description": (
                        "Fecha y hora de fin en formato 'YYYY-MM-DD HH:MM'. "
                        "Ejemplo: '2025-11-28 23:59'"
                    )
                },
                "max_resultados": {
                    "type": "integer",
                    "description": "Número máximo de eventos a devolver (por defecto 10)",
                    "default": 10
                }
            },
            "required": ["fecha_inicio", "fecha_fin"]
        }
    )

    agent.register_tool(
        name="crear_evento_calendario",
        function=tool_crear_evento_calendario,
        description=(
            "Crea un nuevo evento en Google Calendar. "
            "Siempre debes convertir expresiones como 'hoy', 'mañana' o "
            "'el viernes que viene' a una fecha completa usando la fecha "
            "actual que se indica en el mensaje de sistema. "
            "Las fechas deben ir en formato 'YYYY-MM-DD HH:MM'. "
            "Nunca utilices años anteriores al año actual salvo que el "
            "usuario lo pida explícitamente."
        ),
        parameters={
            "type": "object",
            "properties": {
                "titulo": {
                    "type": "string",
                    "description": "Título del evento (ej: 'Examen de IA')"
                },
                "fecha_inicio": {
                    "type": "string",
                    "description": (
                        "Fecha y hora de inicio en formato 'YYYY-MM-DD HH:MM'. "
                        "Ejemplo: '2025-12-15 10:00'"
                    )
                },
                "fecha_fin": {
                    "type": "string",
                    "description": (
                        "Fecha y hora de fin en formato 'YYYY-MM-DD HH:MM'. "
                        "Ejemplo: '2025-12-15 12:00'"
                    )
                },
                "descripcion": {
                    "type": "string",
                    "description": "Descripción del evento (opcional)"
                },
                "ubicacion": {
                    "type": "string",
                    "description": "Ubicación del evento (opcional, ej: 'Aula A-201')"
                }
            },
            "required": ["titulo", "fecha_inicio", "fecha_fin"]
        }
    )

    agent.register_tool(
        name="eliminar_evento_calendario",
        function=tool_eliminar_evento_calendario,
        description=(
            "Elimina un evento del Google Calendar por su ID. "
            "Úsalo cuando el usuario indique claramente qué evento quiere borrar."
        ),
        parameters={
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": (
                        "ID del evento en Google Calendar. Normalmente se obtiene "
                        "usando listar_eventos_calendario."
                    )
                }
            },
            "required": ["event_id"]
        }
    )


# ==============================
# MAIN CLI
# ==============================

def main():
    print_banner()

    console.print("\n[yellow]⏳ Inicializando agente Qwen2.5-72B...[/yellow]")

    try:
        agent = QwenAgent()
        register_tools(agent)
        console.print("[green]✓ Agente listo![/green]\n")
    except Exception as e:
        console.print(f"[bold red]❌ Error al inicializar:[/bold red] {e}")
        console.print("\n[yellow]Verifica que:[/yellow]")
        console.print("  1. Tienes un token válido de Hugging Face en .env")
        console.print("  2. El token tiene acceso al modelo Qwen2.5-72B-Instruct")
        console.print("  3. Tienes conexión a internet")
        sys.exit(1)

    console.print(Panel.fit(
        "[bold]Comandos / ejemplos:[/bold]\n\n"
        "  • Horarios / universidad:\n"
        "      - '¿Qué clases tengo de IA el martes?'\n"
        "      - 'Muéstrame todos los horarios de este cuatrimestre'\n\n"
        "  • Profesores / aulas:\n"
        "      - '¿Que imparte Dra. López Fernández?'\n"
        "      - '¿Dónde está el aula A-201?'\n\n"
        "  • Tareas locales (JSON):\n"
        "      - 'Crea una tarea para entregar la práctica el 2025-12-15'\n"
        "      - 'Muéstrame mis tareas pendientes'\n"
        "      - 'Marca la tarea 1 como completada'\n\n"
        "  • Google Calendar:\n"
        "      - '¿Qué eventos tengo hoy en mi calendario?'\n"
        "      - 'Crea un evento mañana a las 10:00 para estudiar MCP'\n"
        "      - 'Borra el evento del calendario que creaste para hoy'\n\n"
        "  /reset - Reinicia la conversación\n"
        "  /salir - Termina el programa",
        title="Ayuda",
        border_style="blue"
    ))

    console.print()

    # Loop conversacional
    while True:
        try:
            user_input = console.input("[bold cyan]Tú:[/bold cyan] ").strip()

            if user_input.lower() in ["/salir", "/exit", "/quit"]:
                console.print("\n[yellow]👋 ¡Hasta luego! Que tengas un buen día.[/yellow]\n")
                break

            if user_input.lower() == "/reset":
                agent.reset_conversation()
                console.print("[green]✓ Conversación reiniciada[/green]\n")
                continue

            if not user_input:
                continue

            console.print()
            with console.status("[bold yellow]🤔 Pensando...", spinner="dots"):
                response = agent.chat(user_input)

            console.print("[bold magenta]Asistente:[/bold magenta]")
            console.print(Panel(
                Markdown(response),
                border_style="magenta",
                padding=(1, 2)
            ))
            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️  Interrumpido por el usuario[/yellow]")
            confirm = console.input("[yellow]¿Quieres salir? (s/n):[/yellow] ")
            if confirm.lower() in ["s", "si", "sí", "y", "yes"]:
                break
            console.print()

        except Exception as e:
            console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")


if __name__ == "__main__":
    main()
