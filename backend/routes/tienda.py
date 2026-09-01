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
    {
        "id": "tema_medianoche",
        "nombre": "Modo Medianoche",
        "descripcion": "Azul índigo profundo para sesiones de código nocturnas.",
        "lore": "El sistema nunca duerme. Vos tampoco, aparentemente.",
        "categoria": "tema",
        "precio": 550,
        "icono": "🌌",
        "unico": True,
    },
    {
        "id": "tema_ambar",
        "nombre": "Modo Ámbar",
        "descripcion": "Terminal ámbar retro, como las consolas de antes de que existiera el color.",
        "lore": "Antes de los píxeles verdes, hubo ámbar.",
        "categoria": "tema",
        "precio": 550,
        "icono": "🟠",
        "unico": True,
    },
    {
        "id": "tema_glaciar",
        "nombre": "Modo Glaciar",
        "descripcion": "Blancos y celestes helados. Precisión bajo cero.",
        "lore": "Cada bug se congela antes de propagarse.",
        "categoria": "tema",
        "precio": 650,
        "icono": "🧊",
        "unico": True,
    },
    {
        "id": "tema_vaporwave",
        "nombre": "Modo Vaporwave",
        "descripcion": "Rosa y violeta synthwave. Nostalgia de una década que nunca viviste.",
        "lore": "Estética de los 80, lógica del futuro.",
        "categoria": "tema",
        "precio": 750,
        "icono": "🌆",
        "unico": True,
    },
    {
        "id": "tema_apagon",
        "nombre": "Modo Apagón",
        "descripcion": "Negro puro, sin distracciones. Solo vos, el cursor y el texto.",
        "lore": "Cuando todo lo demás falla, queda el texto.",
        "categoria": "tema",
        "precio": 600,
        "icono": "⚫",
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
    {
        "id": "titulo_rubber_duck",
        "nombre": "Rubber Duck",
        "descripcion": "Le explicaste el bug a un pato de goma antes que a un humano.",
        "lore": "El pato nunca opina, pero siempre ayuda.",
        "categoria": "titulo",
        "precio": 350,
        "icono": "🦆",
        "unico": True,
    },
    {
        "id": "titulo_full_stack",
        "nombre": "Full Stack",
        "descripcion": "Del frontend a la base de datos, sin miedo a ninguna capa.",
        "lore": "Si se rompe en algún lado, vas a saber dónde mirar.",
        "categoria": "titulo",
        "precio": 500,
        "icono": "🧩",
        "unico": True,
    },
    {
        "id": "titulo_refactor",
        "nombre": "Refactor Master",
        "descripcion": "Dejaste el código mejor de lo que lo encontraste.",
        "lore": "El mejor commit es el que borra más líneas de las que agrega.",
        "categoria": "titulo",
        "precio": 550,
        "icono": "🛠️",
        "unico": True,
    },
    {
        "id": "titulo_segfault",
        "nombre": "Cazador de Segfaults",
        "descripcion": "Ni la memoria se le escapa. Los punteros le tienen respeto.",
        "lore": "Segmentation fault (core dumped). Ya no, con vos cerca.",
        "categoria": "titulo",
        "precio": 700,
        "icono": "💥",
        "unico": True,
    },
    {
        "id": "titulo_arquitecto_nexus",
        "nombre": "Arquitecto del NEXUS",
        "descripcion": "Diseñó sistemas que el resto del equipo solo puede mantener.",
        "lore": "Cada línea que escribe es una decisión que otros van a heredar.",
        "categoria": "titulo",
        "precio": 1200,
        "icono": "🏛️",
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
    # ── Cosméticos (fondos animados) ──────────────────────────────────────
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
    {
        "id": "nieve_bits",
        "nombre": "Nieve de Bits",
        "descripcion": "Ceros y unos cayendo despacio, como nieve. Un fondo tranquilo para pensar.",
        "lore": "Cada copo es una decisión binaria.",
        "categoria": "cosmetico",
        "precio": 700,
        "icono": "❄️",
        "unico": True,
    },
    {
        "id": "lluvia_meteoros",
        "nombre": "Lluvia de Meteoros",
        "descripcion": "Rachas de luz cruzando el fondo en diagonal, cada tanto.",
        "lore": "Pedí un deseo antes de que el build termine.",
        "categoria": "cosmetico",
        "precio": 850,
        "icono": "☄️",
        "unico": True,
    },
    {
        "id": "pulso_datos",
        "nombre": "Pulso de Datos",
        "descripcion": "Anillos de sonar que laten desde distintos puntos del NEXUS.",
        "lore": "Algo ahí afuera sigue respondiendo ping.",
        "categoria": "cosmetico",
        "precio": 750,
        "icono": "📡",
        "unico": True,
    },
    {
        "id": "ascenso_chispas",
        "nombre": "Ascenso de Chispas",
        "descripcion": "Chispas naranjas subiendo desde abajo, como brasas de un sistema al rojo vivo.",
        "lore": "Todo compilador tiene un poco de incendio adentro.",
        "categoria": "cosmetico",
        "precio": 750,
        "icono": "🔥",
        "unico": True,
    },
    {
        "id": "iconos_lenguajes",
        "nombre": "Logos del Lenguaje",
        "descripcion": "Etiquetas de PY, JS, C++, TS, GO y RS flotando por el fondo.",
        "lore": "Todos los lenguajes que todavía no aprendiste, mirándote.",
        "categoria": "cosmetico",
        "precio": 800,
        "icono": "🏷️",
        "unico": True,
    },
    {
        "id": "fauna_nexus",
        "nombre": "Fauna del NEXUS",
        "descripcion": "La serpiente, el bug, el pato de goma y demás mascotas del oficio, flotando en el fondo.",
        "lore": "Ningún programador trabaja solo. Siempre hay una mascota de por medio.",
        "categoria": "cosmetico",
        "precio": 800,
        "icono": "🐍",
        "unico": True,
    },
    {
        "id": "confeti_build",
        "nombre": "Confeti de Build",
        "descripcion": "Confeti de colores cayendo, como si cada build exitoso mereciera una fiesta.",
        "lore": "BUILD OK merece más que un mensaje en la terminal.",
        "categoria": "cosmetico",
        "precio": 700,
        "icono": "🎉",
        "unico": True,
    },
    {
        "id": "engranajes",
        "nombre": "Engranajes del Sistema",
        "descripcion": "Engranajes metálicos girando despacio de fondo, como si el NEXUS nunca dejara de procesar.",
        "lore": "Todo sistema, por más limpio que se vea, es mecánico por dentro.",
        "categoria": "cosmetico",
        "precio": 700,
        "icono": "⚙️",
        "unico": True,
    },
]

FONDOS_VALIDOS = {
    "lluvia_codigo", "nieve_bits", "lluvia_meteoros", "pulso_datos", "ascenso_chispas",
    "iconos_lenguajes", "fauna_nexus", "confeti_build", "engranajes",
}


def _migrar_equipado(equipado: dict) -> dict:
    # Versión vieja: {"lluvia": true/false}. Versión nueva: {"fondo": "<item_id>"|null},
    # para poder tener más de un fondo animado entre los que elegir.
    if "fondo" not in equipado:
        equipado["fondo"] = "lluvia_codigo" if equipado.get("lluvia") else None
    equipado.pop("lluvia", None)
    return equipado


def _cargar_progreso():
    ruta = os.path.abspath(PROGRESO_FILE)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("inventario", [])
            data.setdefault("equipado", {"tema": None, "titulo": None, "fondo": None})
            data["equipado"] = _migrar_equipado(data["equipado"])
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
        "equipado": progreso.get("equipado", {"tema": None, "titulo": None, "fondo": None}),
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

    equipado = _migrar_equipado(progreso.get("equipado", {"tema": None, "titulo": None, "fondo": None}))

    if item["categoria"] == "tema":
        equipado["tema"] = None if req.desequipar else req.item_id.replace("tema_", "")
    elif item["categoria"] == "titulo":
        equipado["titulo"] = None if req.desequipar else item["nombre"]
    elif item["categoria"] == "cosmetico" and item["id"] in FONDOS_VALIDOS:
        equipado["fondo"] = None if req.desequipar else item["id"]

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
