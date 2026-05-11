import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
MAX_HISTORIAL = 20

SYSTEM_PROMPT = """Sos CodeTutor, un tutor de programación amigable y entusiasta. Tu misión es ayudar a estudiantes a aprender a programar.

Reglas estrictas:
1. NUNCA des el código completo como solución. Guiá con pistas graduales.
2. Si el estudiante pide la respuesta directa, explicá el concepto y dales una pista, no el código.
3. Cuando el código tiene errores, señalá QUÉ está mal y POR QUÉ, pero no lo corrijas directamente.
4. Celebrá los avances y errores que muestran aprendizaje: los errores son parte del proceso.
5. Hablá en español latinoamericano informal: "vos", "tenés", "podés", "mirá".
6. Máximo 5 oraciones por respuesta. Sé conciso y claro.
7. Usá emojis con moderación para hacer la experiencia más amena.
8. Si el código funciona bien, ¡celebralo! y sugerí cómo podría mejorarse.
9. Enfocate en el módulo actual cuando sea relevante.
10. Si te preguntan algo completamente fuera de programación, redirigí amablemente al tema."""

historial: list = []


def _get_api_key() -> Optional[str]:
    return os.environ.get("GEMINI_API_KEY")


async def _llamar_gemini(mensajes: list, system: str = SYSTEM_PROMPT) -> str:
    api_key = _get_api_key()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY no configurada. Configurá la variable de entorno para usar el tutor IA."
        )

    contents = []
    for msg in mensajes:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": system}]},
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
            "topP": 0.9,
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                f"{GEMINI_URL}?key={api_key}",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise HTTPException(status_code=400, detail="API key inválida o request malformado.")
            elif e.response.status_code == 429:
                raise HTTPException(status_code=429, detail="Límite de solicitudes alcanzado. Esperá un momento.")
            raise HTTPException(status_code=502, detail=f"Error de la API de Gemini: {e.response.status_code}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="La IA tardó demasiado. Intentá de nuevo.")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error conectando con la IA: {str(e)}")


class PreguntaRequest(BaseModel):
    mensaje: str
    contexto_modulo: Optional[str] = None
    lenguaje: Optional[str] = None


class AnalizarRequest(BaseModel):
    codigo: str
    output: str
    exito: bool
    modulo_titulo: Optional[str] = None
    modulo_ejercicio: Optional[str] = None
    lenguaje: Optional[str] = None


@router.get("/ia/estado")
def estado_ia():
    api_key = _get_api_key()
    if api_key:
        return {"configurada": True, "mensaje": "Tutor IA listo para ayudarte 🤖"}
    return {"configurada": False, "mensaje": "Configurá GEMINI_API_KEY para activar el tutor IA"}


@router.post("/ia/preguntar")
async def preguntar(req: PreguntaRequest):
    global historial

    contexto = ""
    if req.contexto_modulo:
        contexto = f"[Contexto: el estudiante está trabajando en el módulo '{req.contexto_modulo}'"
        if req.lenguaje:
            contexto += f" de {req.lenguaje}"
        contexto += f"]\n\n{req.mensaje}"
    else:
        contexto = req.mensaje

    historial.append({"role": "user", "content": contexto})

    if len(historial) > MAX_HISTORIAL:
        historial = historial[-MAX_HISTORIAL:]

    respuesta = await _llamar_gemini(historial)
    historial.append({"role": "assistant", "content": respuesta})

    return {"respuesta": respuesta, "mensajes_en_historial": len(historial)}


@router.post("/ia/analizar")
async def analizar_codigo(req: AnalizarRequest):
    partes = []

    if req.modulo_titulo:
        partes.append(f"Módulo actual: '{req.modulo_titulo}'")
    if req.lenguaje:
        partes.append(f"Lenguaje: {req.lenguaje}")
    if req.modulo_ejercicio:
        partes.append(f"Ejercicio: {req.modulo_ejercicio}")

    partes.append(f"\nCódigo del estudiante:\n```\n{req.codigo}\n```")
    partes.append(f"\nResultado de ejecutar el código:")
    partes.append(f"Estado: {'✅ Funcionó' if req.exito else '❌ Hubo un error'}")
    partes.append(f"Output:\n{req.output}")

    if req.exito:
        partes.append("\nEl código funcionó. Analizá si resuelve correctamente el ejercicio del módulo, felicitá al estudiante y sugerí una mejora o extensión interesante.")
    else:
        partes.append("\nHubo un error. Ayudá al estudiante a entender QUÉ falló y POR QUÉ, con una pista para resolverlo. No des el código correcto.")

    mensaje_analisis = "\n".join(partes)

    mensajes_analisis = [{"role": "user", "content": mensaje_analisis}]
    respuesta = await _llamar_gemini(mensajes_analisis)

    historial.append({"role": "user", "content": f"[Análisis automático de código ejecutado]\n{mensaje_analisis}"})
    historial.append({"role": "assistant", "content": respuesta})

    if len(historial) > MAX_HISTORIAL:
        historial = historial[-MAX_HISTORIAL:]

    return {"respuesta": respuesta}


@router.delete("/ia/historial")
def limpiar_historial():
    global historial
    historial = []
    return {"message": "Historial de conversación limpiado"}
