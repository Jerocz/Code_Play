from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import tempfile
import os
import sys
import time

router = APIRouter(prefix="/ejecutar", tags=["Ejecutar"])

class Codigo(BaseModel):
    codigo: str
    lenguaje: str  # python | javascript | cpp

@router.post("/")
def ejecutar(data: Codigo):
    inicio = time.time()

    if data.lenguaje == "python":
        return ejecutar_python(data.codigo, inicio)
    elif data.lenguaje == "javascript":
        return ejecutar_javascript(data.codigo, inicio)
    elif data.lenguaje == "cpp":
        return ejecutar_cpp(data.codigo, inicio)
    else:
        return {"output": "", "error": f"Lenguaje no soportado: {data.lenguaje}", "tiempo": 0}


def ejecutar_python(codigo: str, inicio: float):
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py",
                                         delete=False, encoding="utf-8") as f:
            f.write(codigo)
            ruta = f.name

        resultado = subprocess.run(
            [sys.executable, ruta],
            capture_output=True, text=True,
            timeout=10, encoding="utf-8"
        )
        os.unlink(ruta)
        tiempo = round(time.time() - inicio, 3)

        return {
            "output": resultado.stdout,
            "error":  resultado.stderr,
            "tiempo": tiempo,
            "ok":     resultado.returncode == 0
        }

    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Tiempo límite excedido (10s). ¿Tenés un loop infinito?", "tiempo": 10, "ok": False}
    except Exception as e:
        return {"output": "", "error": str(e), "tiempo": 0, "ok": False}


def ejecutar_javascript(codigo: str, inicio: float):
    # Verificar si Node.js está instalado
    try:
        subprocess.run(["node", "--version"], capture_output=True, timeout=5)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {
            "output": "",
            "error": "Node.js no está instalado. Para correr JavaScript necesitás instalar Node.js desde nodejs.org",
            "tiempo": 0,
            "ok": False
        }

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js",
                                          delete=False, encoding="utf-8") as f:
            f.write(codigo)
            ruta = f.name

        resultado = subprocess.run(
            ["node", ruta],
            capture_output=True, text=True,
            timeout=10, encoding="utf-8"
        )
        os.unlink(ruta)
        tiempo = round(time.time() - inicio, 3)

        return {
            "output": resultado.stdout,
            "error":  resultado.stderr,
            "tiempo": tiempo,
            "ok":     resultado.returncode == 0
        }

    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Tiempo límite excedido (10s).", "tiempo": 10, "ok": False}
    except Exception as e:
        return {"output": "", "error": str(e), "tiempo": 0, "ok": False}


def ejecutar_cpp(codigo: str, inicio: float):
    # Verificar si g++ está instalado
    try:
        subprocess.run(["g++", "--version"], capture_output=True, timeout=5)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {
            "output": "",
            "error": "g++ no está instalado. Para correr C++ en Windows instalá MinGW desde mingw-w64.org",
            "tiempo": 0,
            "ok": False
        }

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp",
                                          delete=False, encoding="utf-8") as f:
            f.write(codigo)
            ruta_cpp = f.name

        ruta_exe = ruta_cpp.replace(".cpp", ".exe" if os.name == "nt" else "")

        # Compilar
        compilar = subprocess.run(
            ["g++", ruta_cpp, "-o", ruta_exe],
            capture_output=True, text=True,
            timeout=15, encoding="utf-8"
        )

        if compilar.returncode != 0:
            os.unlink(ruta_cpp)
            return {
                "output": "",
                "error": "Error de compilación:\n" + compilar.stderr,
                "tiempo": round(time.time() - inicio, 3),
                "ok": False
            }

        # Ejecutar
        resultado = subprocess.run(
            [ruta_exe],
            capture_output=True, text=True,
            timeout=10, encoding="utf-8"
        )

        os.unlink(ruta_cpp)
        if os.path.exists(ruta_exe):
            os.unlink(ruta_exe)

        tiempo = round(time.time() - inicio, 3)
        return {
            "output": resultado.stdout,
            "error":  resultado.stderr,
            "tiempo": tiempo,
            "ok":     resultado.returncode == 0
        }

    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Tiempo límite excedido (10s).", "tiempo": 10, "ok": False}
    except Exception as e:
        return {"output": "", "error": str(e), "tiempo": 0, "ok": False}
