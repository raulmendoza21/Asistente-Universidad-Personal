from fastmcp import FastMCP
from typing import List, Dict

from data_manager import DataManager
from google_calendar_client import GoogleCalendarClient
from config import MCP_PORT

# Inicializar servidor MCP
mcp = FastMCP("Universidad Assistant")
dm = DataManager()
calendar_client = GoogleCalendarClient()

# ========== HERRAMIENTAS DE CONSULTA ==========

@mcp.tool()
def consultar_horario(asignatura: str) -> List[Dict]:
    """
    Consulta el horario de clases de una asignatura específica.

    Args:
        asignatura: Nombre de la asignatura a consultar

    Returns:
        Lista con los horarios de la asignatura
    """
    return dm.get_horario(asignatura)


@mcp.tool()
def consultar_todos_horarios() -> List[Dict]:
    """
    Obtiene el horario completo de todas las asignaturas.

    Returns:
        Lista con todos los horarios
    """
    return dm.get_todos_horarios()


@mcp.tool()
def buscar_profesor(nombre: str) -> Dict:
    """
    Busca información sobre un profesor por su nombre.

    Args:
        nombre: Nombre completo o parcial del profesor

    Returns:
        Información del profesor (email, despacho, tutorías) o error
    """
    profesor = dm.get_profesor(nombre)
    if profesor:
        return profesor
    return {"error": f"Profesor '{nombre}' no encontrado"}


@mcp.tool()
def consultar_aula(codigo_aula: str) -> Dict:
    """
    Obtiene información sobre un aula específica.

    Args:
        codigo_aula: Código del aula (ej: "A-201")

    Returns:
        Información del aula (edificio, capacidad, equipamiento) o error
    """
    aula = dm.get_aula(codigo_aula)
    if aula:
        return aula
    return {"error": f"Aula '{codigo_aula}' no encontrada"}


# ========== HERRAMIENTAS DE GESTIÓN DE TAREAS ==========

@mcp.tool()
def crear_tarea(
    titulo: str,
    fecha_vencimiento: str,
    descripcion: str = "",
    prioridad: str = "media",
) -> Dict:
    """
    Crea una nueva tarea o recordatorio académico.

    Args:
        titulo: Título de la tarea
        fecha_vencimiento: Fecha de vencimiento en formato YYYY-MM-DD
        descripcion: Descripción opcional de la tarea
        prioridad: Prioridad de la tarea (baja, media, alta)

    Returns:
        Información de la tarea creada
    """
    return dm.crear_tarea(titulo, fecha_vencimiento, descripcion, prioridad)


@mcp.tool()
def listar_tareas(filtro: str = "pendientes") -> List[Dict]:
    """
    Lista las tareas del estudiante según un filtro.

    Args:
        filtro: Tipo de tareas a mostrar ("todas", "pendientes", "completadas")

    Returns:
        Lista de tareas según el filtro aplicado
    """
    return dm.listar_tareas(filtro)


@mcp.tool()
def completar_tarea(id_tarea: int) -> Dict:
    """
    Marca una tarea como completada.

    Args:
        id_tarea: ID de la tarea a completar

    Returns:
        Confirmación de la operación
    """
    return dm.completar_tarea(id_tarea)


@mcp.tool()
def eliminar_tarea(id_tarea: int) -> Dict:
    """
    Elimina una tarea permanentemente.

    Args:
        id_tarea: ID de la tarea a eliminar

    Returns:
        Confirmación de la eliminación
    """
    return dm.eliminar_tarea(id_tarea)


# ========== HERRAMIENTAS DE GOOGLE CALENDAR ==========

@mcp.tool()
def listar_eventos_calendario(
    fecha_inicio: str,
    fecha_fin: str,
    max_resultados: int = 10,
) -> list[dict]:
    """
    Lista eventos del Google Calendar asociado entre dos fechas.

    Parámetros:
    - fecha_inicio: fecha y hora inicio en formato 'YYYY-MM-DD HH:MM'
    - fecha_fin: fecha y hora fin en formato 'YYYY-MM-DD HH:MM'
    - max_resultados: número máximo de eventos a recuperar.

    Devuelve:
    - Lista de eventos con id, summary, description, location, start, end.
    """
    return calendar_client.list_events(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        max_resultados=max_resultados,
    )


@mcp.tool()
def crear_evento_calendario(
    titulo: str,
    fecha_inicio: str,
    fecha_fin: str,
    descripcion: str | None = None,
    ubicacion: str | None = None,
) -> dict:
    """
    Crea un nuevo evento en Google Calendar.

    Parámetros:
    - titulo: título del evento.
    - fecha_inicio: 'YYYY-MM-DD HH:MM'
    - fecha_fin: 'YYYY-MM-DD HH:MM'
    - descripcion: texto opcional describiendo el evento.
    - ubicacion: ubicación opcional del evento.

    Devuelve:
    - Un diccionario con id, summary y htmlLink del evento creado.
    """
    return calendar_client.create_event(
        titulo=titulo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        descripcion=descripcion,
        ubicacion=ubicacion,
    )


@mcp.tool()
def eliminar_evento_calendario(event_id: str) -> dict:
    """
    Elimina un evento de Google Calendar por su ID.

    Parámetros:
    - event_id: identificador del evento en Google Calendar,
      normalmente obtenido de listar_eventos_calendario.

    Devuelve:
    - Un diccionario con el estado de la operación.
    """
    return calendar_client.delete_event(event_id)


# ==========================
# EJECUCIÓN DEL SERVIDOR MCP
# ==========================

if __name__ == "__main__":
    # Servidor MCP HTTP en localhost:MCP_PORT
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=MCP_PORT,
    )
