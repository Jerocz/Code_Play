from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import os
import httpx

router = APIRouter(prefix="/ia", tags=["IA"])

historial: list[dict] = []
MAX_HISTORIAL = 20

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

MODULOS_INFO = {
    1:  "Hola Mundo — usar print() para mostrar texto",
    2:  "Comentarios — líneas que Python ignora con #",
    3:  "Variables — guardar datos con nombres",
    4:  "Tipos de datos — int, float, str, bool",
    5:  "Operadores — suma, resta, multiplicación, división",
    6:  "Input — pedirle datos al usuario",
    7:  "Strings — texto y sus métodos",
    8:  "Condiciones — if, elif, else",
    9:  "Loops for — repetir con secuencias",
    10: "Loops while — repetir mientras se cumpla algo",
    11: "Listas — colecciones ordenadas",
    12: "Diccionarios — pares clave-valor",
    13: "Funciones — organizar código con def",
    14: "Archivos y JSON — guardar datos",
    15: "Clases y OOP — programación orientada a objetos",
    16: "Manejo de errores — try, except",
    17: "Caso real: Calculadora de consola",
    18: "Caso real: Agenda de contactos",
    19: "Caso real: Sistema de inventario",
    20: "Caso real: Juego de adivinar el número",
    21: "Caso real: API REST con FastAPI",
    22: "Caso real: Base de datos con SQL",
    23: "Estructuras de datos: Stack y Queue",
    24: "Estructuras de datos: Hash Map y LRU Cache",
    25: "Algoritmos: Búsqueda y Ordenamiento",
}

SYSTEM_PROMPT = """Eres CodeTutor, un tutor de programación para principiantes absolutos.
Tu trabajo es guiar, nunca dar la respuesta completa.

Reglas:
- NUNCA escribís el código completo que resuelve el ejercicio
- Das pistas graduales: primero muy general, luego más específica
- Explicás con analogías del mundo real (ej: una variable es como una caja con nombre)
- Celebrás los avances del estudiante
- Respondés en español latinoamericano, tono amigable y directo
- Máximo 4 oraciones por respuesta
- Si el estudiante está frustrado, primero validás cómo se siente
- Si el código tiene un error, señalás QUÉ está mal pero no cómo arreglarlo directamente"""

class Pregunta(BaseModel):
    mensaje: str
    modulo_id: Optional[int] = None

@router.post("/preguntar")
async def preguntar(data: Pregunta):
    if not GEMINI_API_KEY:
        return {"error": "Falta configurar GEMINI_API_KEY. Seguí las instrucciones del README."}

    contexto_modulo = ""
    if data.modulo_id and data.modulo_id in MODULOS_INFO:
        contexto_modulo = f"\n\nEl estudiante está trabajando en: {MODULOS_INFO[data.modulo_id]}."

    system_con_contexto = SYSTEM_PROMPT + contexto_modulo

    historial.append({"role": "user", "parts": [{"text": data.mensaje}]})
    if len(historial) > MAX_HISTORIAL:
        del historial[0:2]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                json={
                    "system_instruction": {"parts": [{"text": system_con_contexto}]},
                    "contents": historial,
                    "generationConfig": {"maxOutputTokens": 400, "temperature": 0.7}
                },
                timeout=30.0
            )

        if response.status_code != 200:
            historial.pop()
            return {"error": f"Error de Gemini ({response.status_code}): {response.text[:200]}"}

        contenido = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        historial.append({"role": "model", "parts": [{"text": contenido}]})
        return {"respuesta": contenido}

    except httpx.TimeoutException:
        if historial and historial[-1]["role"] == "user":
            historial.pop()
        return {"error": "La IA tardó demasiado. Intentá de nuevo."}
    except Exception as e:
        if historial and historial[-1]["role"] == "user":
            historial.pop()
        return {"error": f"Error inesperado: {str(e)}"}

@router.delete("/historial")
def limpiar_historial():
    historial.clear()
    return {"mensaje": "Conversación reiniciada"}

@router.get("/estado")
def estado_ia():
    return {
        "configurada": bool(GEMINI_API_KEY),
        "mensaje": "IA lista (Gemini gratuito)" if GEMINI_API_KEY else "Falta GEMINI_API_KEY — leé el README",
        "mensajes_en_historial": len(historial)
    }
