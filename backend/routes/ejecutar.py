import asyncio
import codecs
import contextlib
import glob
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


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

TIMEOUT_CPP_COMPILE = 15
HARD_TIMEOUT = 300      # tope absoluto de una sesión interactiva (segundos)
MAX_OUTPUT = 20000      # caracteres totales antes de truncar y matar el proceso
CHUNK = 4096

# Preámbulo de una sola línea: fuerza que stdout/stderr salgan sin buffer,
# porque por defecto (proceso no conectado a una consola real) el runtime de
# C++ guarda todo en un buffer de 4KB y no lo vacía hasta que el programa
# termina — entonces un "cout <<" antes de "cin >>" nunca se vería hasta el
# final. #line 1 resetea la numeración para que los errores de compilación
# sigan apuntando a la línea real del alumno.
_PREAMBULO_CPP = (
    "#include<cstdio>\n"
    "namespace{struct __au{__au(){std::setvbuf(stdout,nullptr,_IONBF,0);"
    "std::setvbuf(stderr,nullptr,_IONBF,0);}}__aui;}\n"
    '#line 1 "programa.cpp"\n'
)


async def _preparar_comando(lenguaje: str, codigo: str, tmpdir: str) -> tuple[list[str] | None, str | None]:
    """Deja el código fuente listo en tmpdir y devuelve (comando, error)."""
    if lenguaje == "python":
        src = os.path.join(tmpdir, "programa.py")
        with open(src, "w", encoding="utf-8") as f:
            f.write(codigo)
        return ["python", "-u", src], None

    if lenguaje == "javascript":
        node_path = _find_executable("node")
        if not node_path:
            return None, (
                "❌ Node.js no está instalado.\n\n"
                "Para instalarlo:\n"
                "• Descargá el instalador de https://nodejs.org\n"
                "• Elegí la versión LTS\n"
                "• Reiniciá la terminal después de instalar"
            )
        src = os.path.join(tmpdir, "programa.js")
        with open(src, "w", encoding="utf-8") as f:
            f.write(codigo)
        return [node_path, src], None

    if lenguaje == "cpp":
        gpp_path = _find_executable("g++")
        if not gpp_path:
            return None, (
                "❌ g++ no está instalado.\n\n"
                "Para instalar en Windows:\n"
                "• Instalá MinGW-w64 desde https://winlibs.com\n"
                "• O usá MSYS2: pacman -S mingw-w64-x86_64-gcc\n"
                "• Agregá C:\\mingw64\\bin al PATH del sistema\n"
                "• Reiniciá la terminal"
            )
        src = os.path.join(tmpdir, "programa.cpp")
        exe = os.path.join(tmpdir, "programa.exe")
        with open(src, "w", encoding="utf-8") as f:
            f.write(_PREAMBULO_CPP + codigo)

        compile_result = await asyncio.to_thread(
            subprocess.run,
            [gpp_path, "-o", exe, src, "-std=c++17", "-Wall"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_CPP_COMPILE,
            encoding="utf-8",
            errors="replace",
        )
        if compile_result.returncode != 0:
            return None, "❌ Error de compilación:\n\n" + compile_result.stderr
        return [exe], None

    return None, f"Lenguaje '{lenguaje}' no soportado."


@router.websocket("/ws/ejecutar")
async def ejecutar_interactivo(ws: WebSocket):
    """Ejecuta código de forma interactiva: el proceso corre de verdad y se
    pausa en input()/cin/readline como en una terminal real. La entrada que
    escribe el alumno viaja por este mismo socket y se conecta al stdin del
    proceso."""
    await ws.accept()
    tmpdir = tempfile.mkdtemp(prefix="ejec_")
    proc: subprocess.Popen | None = None
    inicio = time.time()

    try:
        try:
            raw = await ws.receive_text()
            msg = json.loads(raw)
        except (WebSocketDisconnect, json.JSONDecodeError):
            return

        lenguaje = str(msg.get("lenguaje", "")).lower()
        codigo = str(msg.get("codigo", ""))

        cmd, error = await _preparar_comando(lenguaje, codigo, tmpdir)
        if error:
            with contextlib.suppress(Exception):
                await ws.send_json({"tipo": "error", "mensaje": error})
                await ws.send_json({"tipo": "fin", "exito": False, "tiempo": 0})
            return

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"

        proc = subprocess.Popen(
            cmd,
            cwd=tmpdir,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )

        loop = asyncio.get_event_loop()
        salida_q: asyncio.Queue = asyncio.Queue()
        estado_lectura = {"total": 0, "truncado": False}

        def leer_stdout():
            decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
            try:
                while True:
                    b = proc.stdout.read(CHUNK)
                    if not b:
                        break
                    texto = decoder.decode(b)
                    if not texto or estado_lectura["truncado"]:
                        continue
                    estado_lectura["total"] += len(texto)
                    if estado_lectura["total"] > MAX_OUTPUT:
                        estado_lectura["truncado"] = True
                        recorte = len(texto) - (estado_lectura["total"] - MAX_OUTPUT)
                        if recorte > 0:
                            loop.call_soon_threadsafe(
                                salida_q.put_nowait, {"tipo": "salida", "texto": texto[:recorte]}
                            )
                        loop.call_soon_threadsafe(
                            salida_q.put_nowait,
                            {"tipo": "error", "mensaje": "⚠ Salida truncada: el programa imprimió demasiado texto."},
                        )
                        with contextlib.suppress(Exception):
                            proc.kill()
                        continue
                    loop.call_soon_threadsafe(salida_q.put_nowait, {"tipo": "salida", "texto": texto})
            finally:
                loop.call_soon_threadsafe(salida_q.put_nowait, None)

        threading.Thread(target=leer_stdout, daemon=True).start()

        async def bombear_stdin():
            deadline = inicio + HARD_TIMEOUT
            try:
                while True:
                    restante = deadline - time.time()
                    if restante <= 0:
                        await salida_q.put({
                            "tipo": "error",
                            "mensaje": f"⏱ Se cerró la sesión: tiempo máximo de {HARD_TIMEOUT}s superado.",
                        })
                        with contextlib.suppress(Exception):
                            proc.kill()
                        return
                    try:
                        data = await asyncio.wait_for(ws.receive_text(), timeout=restante)
                    except asyncio.TimeoutError:
                        continue
                    try:
                        m = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    if m.get("tipo") == "entrada" and proc.poll() is None:
                        try:
                            proc.stdin.write((str(m.get("texto", "")) + "\n").encode("utf-8"))
                            proc.stdin.flush()
                        except (BrokenPipeError, OSError):
                            pass
                    elif m.get("tipo") == "detener":
                        with contextlib.suppress(Exception):
                            proc.kill()
                        return
            except WebSocketDisconnect:
                if proc.poll() is None:
                    with contextlib.suppress(Exception):
                        proc.kill()

        tarea_stdin = asyncio.create_task(bombear_stdin())

        try:
            while True:
                item = await salida_q.get()
                if item is None:
                    break
                try:
                    await ws.send_json(item)
                except Exception:
                    break
        finally:
            tarea_stdin.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await tarea_stdin

        try:
            codigo_salida = proc.wait(timeout=10)
        except Exception:
            codigo_salida = proc.poll()
        tiempo = round(time.time() - inicio, 3)
        with contextlib.suppress(Exception):
            await ws.send_json({"tipo": "fin", "exito": codigo_salida == 0, "tiempo": tiempo})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        with contextlib.suppress(Exception):
            await ws.send_json({"tipo": "error", "mensaje": f"Error interno del servidor: {e}"})
    finally:
        if proc is not None and proc.poll() is None:
            with contextlib.suppress(Exception):
                proc.kill()
        shutil.rmtree(tmpdir, ignore_errors=True)
        with contextlib.suppress(Exception):
            await ws.close()
