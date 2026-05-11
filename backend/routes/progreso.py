from fastapi import APIRouter
import json
import os

router = APIRouter(prefix="/progreso", tags=["Progreso"])

ARCHIVO = "progreso.json"

MODULOS_POR_LENGUAJE = {
    "python": 25,
    "javascript": 10,
    "cpp": 10
}

def cargar():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "xp": 0,
        "nivel": 1,
        "python": [],
        "javascript": [],
        "cpp": []
    }

def guardar(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=2)

def calcular_nivel(xp):
    return (xp // 150) + 1

@router.get("/")
def progreso():
    return cargar()

@router.post("/completar/{lenguaje}/{modulo_id}")
def completar(lenguaje: str, modulo_id: int):
    if lenguaje not in MODULOS_POR_LENGUAJE:
        return {"error": f"Lenguaje inválido: {lenguaje}"}

    data = cargar()
    completados = data.get(lenguaje, [])

    # Verificar orden secuencial
    if modulo_id > 1 and (modulo_id - 1) not in completados:
        return {"error": f"Completá el módulo {modulo_id - 1} primero"}

    if modulo_id not in completados:
        completados.append(modulo_id)
        data[lenguaje] = completados
        data["xp"] += 30
        data["nivel"] = calcular_nivel(data["xp"])
        guardar(data)

    return {"mensaje": "Módulo completado", "progreso": data}

@router.post("/resetear")
def resetear():
    data = {"xp": 0, "nivel": 1, "python": [], "javascript": [], "cpp": []}
    guardar(data)
    return {"mensaje": "Progreso reiniciado", "progreso": data}
