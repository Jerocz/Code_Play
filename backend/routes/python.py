from fastapi import APIRouter

router = APIRouter(
    prefix="/python",
    tags=["Python"]
)

modulos = [
    {"id": 1, "titulo": "Primeros pasos", "xp": 50},
    {"id": 2, "titulo": "Strings", "xp": 75},
    {"id": 3, "titulo": "Decisiones", "xp": 100},
    {"id": 4, "titulo": "Loops", "xp": 120},
    {"id": 5, "titulo": "Funciones", "xp": 150},
]

@router.get("/modulos")
def obtener_modulos():
    return modulos

@router.get("/modulos/{modulo_id}")
def obtener_modulo(modulo_id: int):
    for modulo in modulos:
        if modulo["id"] == modulo_id:
            return modulo
    return {"error": "Módulo no encontrado"}