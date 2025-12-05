from datetime import datetime, date
from typing import Dict, List

def format_horario(horarios: List[Dict]) -> str:
    """Formatea una lista de horarios para mostrar"""
    if not horarios:
        return "No se encontraron horarios"

    lines = []
    for h in horarios:
        lines.append(
            f"📅 {h['dia']} | ⏰ {h['hora_inicio']}-{h['hora_fin']} | "
            f"🏫 {h['aula']} | 👨‍🏫 {h['profesor']}"
        )

    return "\n".join(lines)


def format_tarea(tarea: Dict) -> str:
    """Formatea una tarea para mostrar"""
    estado = "✅" if tarea["completada"] else "⏳"
    prioridad_emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}

    return (
        f"{estado} **[{tarea['id']}]** {tarea['titulo']} "
        f"{prioridad_emoji.get(tarea['prioridad'], '')} | "
        f"📅 {tarea['fecha_vencimiento']}"
    )


def es_fecha_valida(fecha_str: str) -> bool:
    """Valida formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def normalizar_fecha_futura(fecha_str: str) -> str:
    """
    Recibe una fecha 'YYYY-MM-DD' (posiblemente en pasado, ej. 2023-12-20)
    y la ajusta para que sea como mínimo en el año actual, y si aún así
    queda en el pasado, la mueve al año siguiente.

    Ejemplos (suponiendo hoy = 2025-11-28):
      - '2023-12-20' -> '2025-12-20'
      - '2024-05-10' -> '2025-05-10'
      - '2025-01-01' (si ya pasó) -> '2026-01-01'
      - '2026-03-01' -> '2026-03-01' (se respeta porque ya es futuro)
    """
    dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    hoy = date.today()

    # Si el año es menor que el actual, súbelo al año actual
    if dt.year < hoy.year:
        dt = dt.replace(year=hoy.year)

    # Si sigue siendo una fecha pasada, súbela al año siguiente
    if dt < hoy:
        dt = dt.replace(year=dt.year + 1)

    return dt.strftime("%Y-%m-%d")
