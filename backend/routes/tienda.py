import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

PROGRESO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "progreso.json")

ITEMS_TIENDA = [
    # ── Temas ──────────────────────────────────────────────────────────────
    {
        "id": "tema_matrix",
        "nombre": "Modo Matrix",
        "descripcion": "Terminal verde hacker. El código corre más profundo.",
        "lore": "Solo los elegidos ven el código caer.",
        "categoria": "tema",
        "precio": 500,
        "icono": "🟩",
        "unico": True,
    },
    {
        "id": "tema_oceano",
        "nombre": "Modo Océano",
        "descripcion": "Azules profundos para programar bajo el mar.",
        "lore": "Las mejores ideas vienen de las profundidades.",
        "categoria": "tema",
        "precio": 500,
        "icono": "🌊",
        "unico": True,
    },
    {
        "id": "tema_fuego",
        "nombre": "Modo Fuego",
        "descripcion": "Naranjas y rojos. Para los que programan ardiendo.",
        "lore": "Compilar sin errores nunca fue tan caliente.",
        "categoria": "tema",
        "precio": 600,
        "icono": "🔥",
        "unico": True,
    },
    {
        "id": "tema_sakura",
        "nombre": "Modo Sakura",
        "descripcion": "Estética pastel rosa. Porque el código puede ser bonito.",
        "lore": "La elegancia es el mejor algoritmo.",
        "categoria": "tema",
        "precio": 700,
        "icono": "🌸",
        "unico": True,
    },
    # ── Títulos ────────────────────────────────────────────────────────────
    {
        "id": "titulo_bug_hunter",
        "nombre": "Bug Hunter",
        "descripcion": "Mostrá que cazás errores como nadie.",
        "lore": "El error existe. Yo lo encuentro.",
        "categoria": "titulo",
        "precio": 300,
        "icono": "🐛",
        "unico": True,
    },
    {
        "id": "titulo_pythonista",
        "nombre": "Pythonista",
        "descripcion": "Para los que eligieron el lado de la serpiente.",
        "lore": "import antigravity",
        "categoria": "titulo",
        "precio": 400,
        "icono": "🐍",
        "unico": True,
    },
    {
        "id": "titulo_code_ninja",
        "nombre": "Code Ninja",
        "descripcion": "Sigiloso, rápido, sin bugs visibles.",
        "lore": "El mejor código es el que nadie sabe que existe.",
        "categoria": "titulo",
        "precio": 600,
        "icono": "🥷",
        "unico": True,
    },
    {
        "id": "titulo_hacker",
        "nombre": "Hacker",
        "descripcion": "El que hackea primero, pregunta después.",
        "lore": "No rompo sistemas. Los entiendo mejor que sus creadores.",
        "categoria": "titulo",
        "precio": 800,
        "icono": "👾",
        "unico": True,
    },
    {
        "id": "titulo_10x",
        "nombre": "10x Dev",
        "descripcion": "El título más exclusivo de la tienda.",
        "lore": "Productividad no es escribir más código. Es escribir el correcto.",
        "categoria": "titulo",
        "precio": 1500,
        "icono": "⚡",
        "unico": True,
    },
    # ── Power-ups ──────────────────────────────────────────────────────────
    {
        "id": "racha_shield",
        "nombre": "Escudo de Racha",
        "descripcion": "Si te saltás un día, tu racha sobrevive intacta.",
        "lore": "La consistencia tiene su recompensa.",
        "categoria": "powerup",
        "precio": 500,
        "icono": "🛡️",
        "unico": False,
    },
    {
        "id": "boost_xp",
        "nombre": "Boost XP ×2",
        "descripcion": "Doble XP en los próximos 5 módulos que completes.",
        "lore": "El tiempo es XP. Aprovechalo.",
        "categoria": "powerup",
        "precio": 400,
        "icono": "✨",
        "unico": False,
    },
    {
        "id": "llave_maestra",
        "nombre": "Llave Maestra",
        "descripcion": "Desbloquea cualquier módulo sin completar el anterior.",
        "lore": "Toda puerta tiene su precio.",
        "categoria": "powerup",
        "precio": 600,
        "icono": "🗝️",
        "unico": False,
    },
    # ── Cosméticos ─────────────────────────────────────────────────────────
    {
        "id": "lluvia_codigo",
        "nombre": "Lluvia de Código",
        "descripcion": "Efecto Matrix animado en el fondo. Solo los elegidos lo ven.",
        "lore": "¿Ves el código o ves una mujer de vestido rojo?",
        "categoria": "cosmetico",
        "precio": 800,
        "icono": "🌧️",
        "unico": True,
    },
]


def _cargar_progreso():
    ruta = os.path.abspath(PROGRESO_FILE)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("inventario", [])
            data.setdefault("equipado", {"tema": None, "titulo": None, "lluvia": False})
            data.setdefault("boost_xp_restantes", 0)
            data.setdefault("racha_shields", 0)
            data.setdefault("llaves_maestras", 0)
            data.setdefault("desbloqueos", [])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _guardar_progreso(data: dict):
    ruta = os.path.abspath(PROGRESO_FILE)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class ComprarRequest(BaseModel):
    item_id: str


class EquiparRequest(BaseModel):
    item_id: str
    desequipar: bool = False


class UsarLlaveRequest(BaseModel):
    lenguaje: str
    modulo_id: int


@router.get("/tienda")
def obtener_tienda():
    progreso = _cargar_progreso()
    return {
        "items": ITEMS_TIENDA,
        "inventario": progreso.get("inventario", []),
        "equipado": progreso.get("equipado", {"tema": None, "titulo": None, "lluvia": False}),
        "boost_xp_restantes": progreso.get("boost_xp_restantes", 0),
        "racha_shields": progreso.get("racha_shields", 0),
        "llaves_maestras": progreso.get("llaves_maestras", 0),
        "desbloqueos": progreso.get("desbloqueos", []),
        "xp": progreso.get("xp", 0),
    }


@router.post("/tienda/comprar")
def comprar_item(req: ComprarRequest):
    item = next((i for i in ITEMS_TIENDA if i["id"] == req.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    progreso = _cargar_progreso()
    inventario = progreso.get("inventario", [])
    xp = progreso.get("xp", 0)

    if item["unico"] and req.item_id in inventario:
        raise HTTPException(status_code=400, detail="Ya tenés este item")

    if xp < item["precio"]:
        raise HTTPException(
            status_code=400,
            detail=f"XP insuficiente (tenés {xp}, necesitás {item['precio']})"
        )

    progreso["xp"] -= item["precio"]

    if item["unico"]:
        inventario.append(req.item_id)
        progreso["inventario"] = inventario

    if req.item_id == "boost_xp":
        progreso["boost_xp_restantes"] = progreso.get("boost_xp_restantes", 0) + 5
    elif req.item_id == "racha_shield":
        progreso["racha_shields"] = progreso.get("racha_shields", 0) + 1
    elif req.item_id == "llave_maestra":
        progreso["llaves_maestras"] = progreso.get("llaves_maestras", 0) + 1

    _guardar_progreso(progreso)

    return {
        "message": f"¡{item['nombre']} comprado!",
        "xp_restante": progreso["xp"],
        "inventario": progreso.get("inventario", []),
        "boost_xp_restantes": progreso.get("boost_xp_restantes", 0),
        "racha_shields": progreso.get("racha_shields", 0),
        "llaves_maestras": progreso.get("llaves_maestras", 0),
    }


@router.post("/tienda/equipar")
def equipar_item(req: EquiparRequest):
    item = next((i for i in ITEMS_TIENDA if i["id"] == req.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    progreso = _cargar_progreso()
    inventario = progreso.get("inventario", [])

    if req.item_id not in inventario:
        raise HTTPException(status_code=400, detail="No tenés este item en el inventario")

    equipado = progreso.get("equipado", {"tema": None, "titulo": None, "lluvia": False})

    if item["categoria"] == "tema":
        equipado["tema"] = None if req.desequipar else req.item_id.replace("tema_", "")
    elif item["categoria"] == "titulo":
        equipado["titulo"] = None if req.desequipar else item["nombre"]
    elif item["id"] == "lluvia_codigo":
        equipado["lluvia"] = not req.desequipar

    progreso["equipado"] = equipado
    _guardar_progreso(progreso)

    return {"message": "¡Listo!", "equipado": equipado}


@router.post("/tienda/usar-llave")
def usar_llave(req: UsarLlaveRequest):
    lenguaje = req.lenguaje.lower()
    if lenguaje not in ["python", "javascript", "cpp"]:
        raise HTTPException(status_code=400, detail="Lenguaje inválido")

    progreso = _cargar_progreso()

    if progreso.get("llaves_maestras", 0) < 1:
        raise HTTPException(status_code=400, detail="No tenés Llaves Maestras")

    clave = f"{lenguaje}_{req.modulo_id}"
    desbloqueos = progreso.get("desbloqueos", [])

    if clave in desbloqueos or req.modulo_id in progreso.get(lenguaje, []):
        raise HTTPException(status_code=400, detail="Ese módulo ya está desbloqueado o completado")

    progreso["llaves_maestras"] -= 1
    desbloqueos.append(clave)
    progreso["desbloqueos"] = desbloqueos
    _guardar_progreso(progreso)

    return {
        "message": "¡Módulo desbloqueado con Llave Maestra!",
        "desbloqueos": desbloqueos,
        "llaves_maestras": progreso["llaves_maestras"],
    }
