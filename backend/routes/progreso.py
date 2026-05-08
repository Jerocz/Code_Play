from fastapi import APIRouter
from routes.python import modulos
import json
import os

router = APIRouter(prefix="/progreso", tags=["Progreso"])

ARCHIVO_PROGRESO = "progreso.json"

def cargar_progreso():
    """Carga el progreso desde archivo JSON. Si no existe, crea uno nuevo."""
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r") as f:
                return json.load(f)
        except:
            pass
    return {"xp": 0, "nivel": 1, "modulos_completados": []}

def guardar_progreso(usuario):
    """Guarda el progreso en archivo JSON para que persista."""
    with open(ARCHIVO_PROGRESO, "w") as f:
        json.dump(usuario, f, indent=2)

def calcular_nivel(xp: int) -> int:
    return (xp // 100) + 1

@router.get("/")
def progreso():
    return cargar_progreso()

@router.post("/completar/{modulo_id}")
def completar(modulo_id: int):
    modulo = next((m for m in modulos if m["id"] == modulo_id), None)
    if modulo is None:
        return {"error": "Módulo no encontrado"}

    # Verificar que el módulo anterior esté completado (orden secuencial)
    usuario = cargar_progreso()
    if modulo_id > 1 and (modulo_id - 1) not in usuario["modulos_completados"]:
        return {"error": f"Primero completá el módulo {modulo_id - 1}"}

    if modulo_id not in usuario["modulos_completados"]:
        usuario["modulos_completados"].append(modulo_id)
        usuario["xp"] += modulo["xp"]
        usuario["nivel"] = calcular_nivel(usuario["xp"])
        guardar_progreso(usuario)

    return {"mensaje": "Módulo completado", "usuario": usuario}

@router.post("/resetear")
def resetear():
    """Reinicia todo el progreso (útil para testing)."""
    usuario = {"xp": 0, "nivel": 1, "modulos_completados": []}
    guardar_progreso(usuario)
    return {"mensaje": "Progreso reiniciado", "usuario": usuario}
