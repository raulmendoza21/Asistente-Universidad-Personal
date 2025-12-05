import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from config import TAREAS_FILE, UNIVERSIDAD_FILE
from utils import normalizar_fecha_futura

class DataManager:
    def __init__(self):
        self._init_files()
    
    def _init_files(self):
        """Inicializa los archivos JSON si no existen"""
        # Archivo de tareas
        if not TAREAS_FILE.exists():
            self._save_json(TAREAS_FILE, {"tareas": [], "next_id": 1})
        
        # Archivo de universidad (datos de ejemplo)
        if not UNIVERSIDAD_FILE.exists():
            self._save_json(UNIVERSIDAD_FILE, {
                "horarios": [
                    {
                        "asignatura": "Inteligencia Artificial",
                        "dia": "Lunes",
                        "hora_inicio": "10:00",
                        "hora_fin": "12:00",
                        "aula": "A-201",
                        "profesor": "Dr. García Martínez"
                    },
                    {
                        "asignatura": "Bases de Datos",
                        "dia": "Martes",
                        "hora_inicio": "16:00",
                        "hora_fin": "18:00",
                        "aula": "B-105",
                        "profesor": "Dra. López Fernández"
                    },
                    {
                        "asignatura": "Desarrollo Web",
                        "dia": "Miércoles",
                        "hora_inicio": "09:00",
                        "hora_fin": "11:00",
                        "aula": "C-302",
                        "profesor": "Prof. Rodríguez Pérez"
                    },
                    {
                        "asignatura": "Inteligencia Artificial",
                        "dia": "Jueves",
                        "hora_inicio": "12:00",
                        "hora_fin": "14:00",
                        "aula": "A-201",
                        "profesor": "Dr. García Martínez"
                    }
                ],
                "profesores": [
                    {
                        "nombre": "Dr. García Martínez",
                        "departamento": "Informática",
                        "email": "garcia@universidad.es",
                        "despacho": "Edificio A, 3ª planta",
                        "tutorias": "Martes y Jueves 15:00-17:00"
                    },
                    {
                        "nombre": "Dra. López Fernández",
                        "departamento": "Sistemas de Información",
                        "email": "lopez@universidad.es",
                        "despacho": "Edificio B, 2ª planta",
                        "tutorias": "Lunes y Miércoles 11:00-13:00"
                    },
                    {
                        "nombre": "Prof. Rodríguez Pérez",
                        "departamento": "Ingeniería del Software",
                        "email": "rodriguez@universidad.es",
                        "despacho": "Edificio C, 1ª planta",
                        "tutorias": "Viernes 10:00-14:00"
                    }
                ],
                "aulas": [
                    {
                        "codigo": "A-201",
                        "edificio": "A",
                        "capacidad": 60,
                        "equipamiento": ["Proyector", "Pizarra digital", "Ordenadores"]
                    },
                    {
                        "codigo": "B-105",
                        "edificio": "B",
                        "capacidad": 30,
                        "equipamiento": ["Proyector", "Laboratorio informático"]
                    },
                    {
                        "codigo": "C-302",
                        "edificio": "C",
                        "capacidad": 40,
                        "equipamiento": ["Proyector", "Sistema de audio"]
                    }
                ]
            })
    
    def _load_json(self, filepath: Path) -> dict:
        """Carga un archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, filepath: Path, data: dict):
        """Guarda datos en un archivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ========== HORARIOS ==========
    
    def get_horario(self, asignatura: str) -> List[Dict]:
        """Obtiene el horario de una asignatura"""
        data = self._load_json(UNIVERSIDAD_FILE)
        asignatura_lower = asignatura.lower()
        
        horarios = [
            h for h in data["horarios"]
            if asignatura_lower in h["asignatura"].lower()
        ]
        
        return horarios
    
    def get_todos_horarios(self) -> List[Dict]:
        """Obtiene todos los horarios"""
        data = self._load_json(UNIVERSIDAD_FILE)
        return data["horarios"]
    
    # ========== PROFESORES ==========
    
    def get_profesor(self, nombre: str) -> Optional[Dict]:
        """Busca un profesor por nombre"""
        data = self._load_json(UNIVERSIDAD_FILE)
        nombre_lower = nombre.lower()
        
        for prof in data["profesores"]:
            if nombre_lower in prof["nombre"].lower():
                return prof
        
        return None
    
    def get_todos_profesores(self) -> List[Dict]:
        """Obtiene todos los profesores"""
        data = self._load_json(UNIVERSIDAD_FILE)
        return data["profesores"]
    
    # ========== AULAS ==========
    
    def get_aula(self, codigo: str) -> Optional[Dict]:
        """Obtiene información de un aula"""
        data = self._load_json(UNIVERSIDAD_FILE)
        codigo_upper = codigo.upper()
        
        for aula in data["aulas"]:
            if codigo_upper == aula["codigo"].upper():
                return aula
        
        return None
    
    # ========== TAREAS (CRUD) ==========
    
    def crear_tarea(self, titulo: str, fecha_vencimiento: str, 
                    descripcion: str = "", prioridad: str = "media") -> Dict:
        """Crea una nueva tarea"""
        data = self._load_json(TAREAS_FILE)
        fecha_vencimiento = normalizar_fecha_futura(fecha_vencimiento)
        nueva_tarea = {
            "id": data["next_id"],
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_vencimiento": fecha_vencimiento,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completada": False,
            "prioridad": prioridad
        }
        
        data["tareas"].append(nueva_tarea)
        data["next_id"] += 1
        
        self._save_json(TAREAS_FILE, data)
        
        return nueva_tarea
    
    def listar_tareas(self, filtro: str = "pendientes") -> List[Dict]:
        """Lista tareas según filtro"""
        data = self._load_json(TAREAS_FILE)
        tareas = data["tareas"]
        
        if filtro == "completadas":
            return [t for t in tareas if t["completada"]]
        elif filtro == "pendientes":
            return [t for t in tareas if not t["completada"]]
        else:  # "todas"
            return tareas
    
    def completar_tarea(self, id_tarea: int) -> Dict:
        """Marca una tarea como completada"""
        data = self._load_json(TAREAS_FILE)
        
        for tarea in data["tareas"]:
            if tarea["id"] == id_tarea:
                tarea["completada"] = True
                tarea["fecha_completada"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self._save_json(TAREAS_FILE, data)
                return {"success": True, "tarea": tarea}
        
        return {"success": False, "error": "Tarea no encontrada"}
    
    def eliminar_tarea(self, id_tarea: int) -> Dict:
        """Elimina una tarea"""
        data = self._load_json(TAREAS_FILE)
        
        tareas_filtradas = [t for t in data["tareas"] if t["id"] != id_tarea]
        
        if len(tareas_filtradas) == len(data["tareas"]):
            return {"success": False, "error": "Tarea no encontrada"}
        
        data["tareas"] = tareas_filtradas
        self._save_json(TAREAS_FILE, data)
        
        return {"success": True, "message": f"Tarea {id_tarea} eliminada"}
