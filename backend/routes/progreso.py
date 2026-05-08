from fastapi import APIRouter

router = APIRouter(
    prefix="/progreso",
    tags=["Progreso"]
)

usuario = {
    "xp": 0,
    "nivel": 1,
    "modulos_completados": []
}

@router.get("/")
def obtener_progreso():
    return usuario

@router.post("/completar/{modulo_id}")
def completar_modulo(modulo_id: int):
    usuario["xp"] += 50
    usuario["modulos_completados"].append(modulo_id)

    if usuario["xp"] >= 100:
        usuario["nivel"] = 2

    return {
        "mensaje": "Módulo completado",
        "usuario": usuario
    }