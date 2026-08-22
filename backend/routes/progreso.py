import json
import os
from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

PROGRESO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "progreso.json")

NIVELES = [
    {"nivel": 1, "titulo": "Principiante", "min_xp": 0},
    {"nivel": 2, "titulo": "Aprendiz", "min_xp": 200},
    {"nivel": 3, "titulo": "Estudiante", "min_xp": 500},
    {"nivel": 4, "titulo": "Desarrollador", "min_xp": 1000},
    {"nivel": 5, "titulo": "Programador", "min_xp": 2000},
    {"nivel": 6, "titulo": "Experto", "min_xp": 3000},
    {"nivel": 7, "titulo": "Maestro", "min_xp": 4500},
]

XP_POR_MODULO = {
    "python": {
        1: 50, 2: 50, 3: 50, 4: 50, 5: 50, 6: 50,
        7: 75, 8: 75,
        9: 75, 10: 75,
        11: 100, 12: 100, 13: 100,
        14: 100, 15: 100,
        16: 125, 17: 125,
        18: 125, 19: 125,
        20: 150, 21: 150,
        22: 200, 23: 200, 24: 200, 25: 200,
        26: 150, 27: 150, 28: 175,
        29: 150, 30: 175,
        31: 150,
        32: 125, 33: 175,
        34: 175, 35: 175, 36: 150,
        37: 150,
    },
    "javascript": {
        1: 50, 2: 50, 3: 50, 4: 50, 5: 50,
        6: 75, 7: 75, 8: 75,
        9: 100,
        10: 125,
        11: 100, 12: 100,
        13: 75, 14: 75, 15: 75,
        16: 100, 17: 100,
        18: 125, 19: 125,
        20: 150,
        21: 100, 22: 125,
        23: 175, 24: 175, 25: 200,
        26: 150, 27: 150, 28: 175,
        29: 150, 30: 125,
        31: 200,
        32: 150, 33: 175, 34: 175,
    },
    "cpp": {
        1: 50, 2: 50, 3: 50, 4: 50,
        5: 75, 6: 75,
        7: 100, 8: 100,
        9: 125, 10: 125, 11: 125,
        12: 150, 13: 150, 14: 150,
        15: 175, 16: 175,
        17: 150,
        18: 175,
        19: 125,
        20: 175,
        21: 150, 22: 150,
        23: 125,
        24: 175, 25: 150,
        26: 200,
    },
}


def _default_progreso():
    return {
        "python": [], "javascript": [], "cpp": [],
        "xp": 0, "nivel": 1,
        "racha": 0, "mejor_racha": 0, "ultima_actividad": None,
        "proyectos": {"python": [], "javascript": [], "cpp": []},
        "proyectos_pasos": {},
    }


def _cargar_progreso():
    ruta = os.path.abspath(PROGRESO_FILE)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("racha", 0)
            data.setdefault("mejor_racha", 0)
            data.setdefault("ultima_actividad", None)
            proyectos = data.setdefault("proyectos", {})
            for lang in ["python", "javascript", "cpp"]:
                proyectos.setdefault(lang, [])
            data.setdefault("proyectos_pasos", {})
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_progreso()


def _guardar_progreso(data: dict):
    ruta = os.path.abspath(PROGRESO_FILE)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _calcular_nivel(xp: int) -> dict:
    nivel_actual = NIVELES[0]
    for n in NIVELES:
        if xp >= n["min_xp"]:
            nivel_actual = n
    idx = NIVELES.index(nivel_actual)
    siguiente = NIVELES[idx + 1] if idx + 1 < len(NIVELES) else None
    xp_siguiente = siguiente["min_xp"] if siguiente else nivel_actual["min_xp"]
    xp_actual_nivel = nivel_actual["min_xp"]
    progreso_nivel = ((xp - xp_actual_nivel) / (xp_siguiente - xp_actual_nivel) * 100) if siguiente else 100
    return {
        **nivel_actual,
        "xp_siguiente": xp_siguiente,
        "progreso_pct": round(progreso_nivel, 1),
    }


def _calcular_racha(progreso: dict):
    racha = progreso.get("racha", 0)
    mejor = progreso.get("mejor_racha", 0)
    ultima = progreso.get("ultima_actividad")
    today = date.today().isoformat()

    if ultima is None:
        racha = 1
        es_nueva = True
    else:
        today_date = date.fromisoformat(today)
        ultima_date = date.fromisoformat(ultima)
        diff = (today_date - ultima_date).days
        if diff == 0:
            es_nueva = False
        elif diff == 1:
            racha += 1
            es_nueva = True
        else:
            racha = 1
            es_nueva = True

    mejor = max(mejor, racha)
    return racha, mejor, today, es_nueva


def _bonus_racha(racha: int, xp_base: int) -> int:
    if racha >= 10:
        return round(xp_base * 0.5)
    elif racha >= 5:
        return round(xp_base * 0.25)
    elif racha >= 2:
        return round(xp_base * 0.1)
    return 0


class CompletarRequest(BaseModel):
    lenguaje: str
    modulo_id: int


@router.get("/progreso")
def obtener_progreso():
    progreso = _cargar_progreso()
    nivel_info = _calcular_nivel(progreso.get("xp", 0))
    return {
        **progreso,
        "nivel_info": nivel_info,
    }


@router.post("/progreso/completar")
def completar_modulo(req: CompletarRequest):
    lenguaje = req.lenguaje.lower()
    if lenguaje not in ["python", "javascript", "cpp"]:
        raise HTTPException(status_code=400, detail="Lenguaje inválido")

    progreso = _cargar_progreso()
    completados = progreso.get(lenguaje, [])

    if req.modulo_id in completados:
        return {
            "message": "Ya completado anteriormente",
            "ya_estaba": True,
            "xp_ganado": 0,
            "xp_bonus_racha": 0,
            "xp_total_ganado": 0,
            "xp_total": progreso["xp"],
            "nivel_info": _calcular_nivel(progreso["xp"]),
            "completados": completados,
            "racha": progreso.get("racha", 0),
            "mejor_racha": progreso.get("mejor_racha", 0),
            "es_nueva_racha": False,
        }

    racha, mejor_racha, today, es_nueva_racha = _calcular_racha(progreso)
    xp_ganado = XP_POR_MODULO.get(lenguaje, {}).get(req.modulo_id, 50)
    xp_bonus = _bonus_racha(racha, xp_ganado)
    xp_total_ganado = xp_ganado + xp_bonus

    completados.append(req.modulo_id)
    progreso[lenguaje] = completados
    progreso["xp"] = progreso.get("xp", 0) + xp_total_ganado
    progreso["racha"] = racha
    progreso["mejor_racha"] = mejor_racha
    progreso["ultima_actividad"] = today

    nivel_info = _calcular_nivel(progreso["xp"])
    progreso["nivel"] = nivel_info["nivel"]

    _guardar_progreso(progreso)

    return {
        "message": "¡Módulo completado!",
        "ya_estaba": False,
        "xp_ganado": xp_ganado,
        "xp_bonus_racha": xp_bonus,
        "xp_total_ganado": xp_total_ganado,
        "xp_total": progreso["xp"],
        "nivel_info": nivel_info,
        "completados": completados,
        "racha": racha,
        "mejor_racha": mejor_racha,
        "es_nueva_racha": es_nueva_racha,
    }


@router.delete("/progreso")
def resetear_progreso():
    _guardar_progreso(_default_progreso())
    return {"message": "Progreso reseteado"}
