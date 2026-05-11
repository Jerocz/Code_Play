import subprocess
import tempfile
import os
import time
import shutil
import glob
from fastapi import APIRouter
from pydantic import BaseModel


def _find_executable(name: str) -> str | None:
    """shutil.which pero también busca en rutas conocidas de WinGet/MinGW."""
    found = shutil.which(name)
    if found:
        return found
    # Rutas adicionales donde WinGet instala MinGW en Windows
    extra_patterns = [
        os.path.expanduser(
            f"~/AppData/Local/Microsoft/WinGet/Packages/BrechtSanders.*/"
            f"mingw64/bin/{name}.exe"
        ),
        r"C:\mingw64\bin\\" + name + ".exe",
        r"C:\msys64\mingw64\bin\\" + name + ".exe",
        r"C:\Program Files\mingw-w64\**\bin\\" + name + ".exe",
    ]
    for pattern in extra_patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            return matches[0]
    return None

router = APIRouter()

TIMEOUT_PYTHON = 10
TIMEOUT_JS = 10
TIMEOUT_CPP_COMPILE = 15
TIMEOUT_CPP_RUN = 10
MAX_OUTPUT = 8000


class EjecutarRequest(BaseModel):
    lenguaje: str
    codigo: str


def _truncar(texto: str) -> str:
    if len(texto) > MAX_OUTPUT:
        return texto[:MAX_OUTPUT] + "\n\n[... salida truncada ...]"
    return texto


@router.post("/ejecutar")
def ejecutar_codigo(req: EjecutarRequest):
    lenguaje = req.lenguaje.lower()

    if lenguaje == "python":
        return _ejecutar_python(req.codigo)
    elif lenguaje == "javascript":
        return _ejecutar_javascript(req.codigo)
    elif lenguaje == "cpp":
        return _ejecutar_cpp(req.codigo)
    else:
        return {"exito": False, "output": f"Lenguaje '{lenguaje}' no soportado.", "tiempo": 0}


def _ejecutar_python(codigo: str) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", encoding="utf-8", delete=False) as f:
        f.write(codigo)
        ruta = f.name

    inicio = time.time()
    try:
        result = subprocess.run(
            ["python", ruta],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_PYTHON,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = round(time.time() - inicio, 3)
        if result.returncode == 0:
            return {"exito": True, "output": _truncar(result.stdout or "(sin salida)"), "tiempo": elapsed}
        else:
            error = result.stderr or result.stdout or "Error desconocido"
            return {"exito": False, "output": _truncar(error), "tiempo": elapsed}
    except subprocess.TimeoutExpired:
        return {"exito": False, "output": f"⏱ Tiempo de ejecución superado ({TIMEOUT_PYTHON}s). Revisá si tenés bucles infinitos.", "tiempo": TIMEOUT_PYTHON}
    except FileNotFoundError:
        return {"exito": False, "output": "❌ Python no encontrado. Asegurate de tener Python instalado y en el PATH.", "tiempo": 0}
    finally:
        try:
            os.unlink(ruta)
        except Exception:
            pass


def _ejecutar_javascript(codigo: str) -> dict:
    node_path = _find_executable("node")
    if not node_path:
        return {
            "exito": False,
            "output": "❌ Node.js no está instalado.\n\nPara instalarlo:\n• Descargá el instalador de https://nodejs.org\n• Elegí la versión LTS\n• Reiniciá la terminal después de instalar",
            "tiempo": 0,
        }

    with tempfile.NamedTemporaryFile(suffix=".js", mode="w", encoding="utf-8", delete=False) as f:
        f.write(codigo)
        ruta = f.name

    inicio = time.time()
    try:
        result = subprocess.run(
            [node_path, ruta],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_JS,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = round(time.time() - inicio, 3)
        if result.returncode == 0:
            return {"exito": True, "output": _truncar(result.stdout or "(sin salida)"), "tiempo": elapsed}
        else:
            error = result.stderr or result.stdout or "Error desconocido"
            return {"exito": False, "output": _truncar(error), "tiempo": elapsed}
    except subprocess.TimeoutExpired:
        return {"exito": False, "output": f"⏱ Tiempo superado ({TIMEOUT_JS}s). Revisá si tenés bucles infinitos.", "tiempo": TIMEOUT_JS}
    finally:
        try:
            os.unlink(ruta)
        except Exception:
            pass


def _ejecutar_cpp(codigo: str) -> dict:
    gpp_path = _find_executable("g++")
    if not gpp_path:
        return {
            "exito": False,
            "output": (
                "❌ g++ no está instalado.\n\n"
                "Para instalar en Windows:\n"
                "• Instalá MinGW-w64 desde https://winlibs.com\n"
                "• O usá MSYS2: pacman -S mingw-w64-x86_64-gcc\n"
                "• Agregá C:\\mingw64\\bin al PATH del sistema\n"
                "• Reiniciá la terminal"
            ),
            "tiempo": 0,
        }

    tmpdir = tempfile.mkdtemp()
    src = os.path.join(tmpdir, "programa.cpp")
    exe = os.path.join(tmpdir, "programa.exe")

    with open(src, "w", encoding="utf-8") as f:
        f.write(codigo)

    inicio = time.time()
    try:
        # Compilar
        compile_result = subprocess.run(
            [gpp_path, "-o", exe, src, "-std=c++17", "-Wall"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_CPP_COMPILE,
            encoding="utf-8",
            errors="replace",
        )
        if compile_result.returncode != 0:
            elapsed = round(time.time() - inicio, 3)
            return {
                "exito": False,
                "output": "❌ Error de compilación:\n\n" + _truncar(compile_result.stderr),
                "tiempo": elapsed,
            }

        # Ejecutar
        run_result = subprocess.run(
            [exe],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_CPP_RUN,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = round(time.time() - inicio, 3)
        if run_result.returncode == 0:
            return {"exito": True, "output": _truncar(run_result.stdout or "(sin salida)"), "tiempo": elapsed}
        else:
            error = run_result.stderr or run_result.stdout or "Error en ejecución"
            return {"exito": False, "output": _truncar(error), "tiempo": elapsed}

    except subprocess.TimeoutExpired:
        return {"exito": False, "output": f"⏱ Tiempo superado durante compilación/ejecución.", "tiempo": TIMEOUT_CPP_COMPILE}
    finally:
        try:
            import shutil as sh
            sh.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass
