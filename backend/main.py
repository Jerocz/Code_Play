import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes import python, javascript, cpp, progreso, ejecutar, ia, proyectos, tienda

app = FastAPI(title="CodeTutor API", version="1.0.0")


@app.middleware("http")
async def sin_cache_estaticos(request: Request, call_next):
    # Evita que el navegador cachee agresivamente el frontend (CSS/JS/HTML):
    # sin esto, el browser puede seguir mostrando una versión vieja de los
    # archivos aunque ya se hayan editado en disco.
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache"
    return response

# Registrar routers
app.include_router(python.router, prefix="/api")
app.include_router(javascript.router, prefix="/api")
app.include_router(cpp.router, prefix="/api")
app.include_router(progreso.router, prefix="/api")
app.include_router(ejecutar.router, prefix="/api")
app.include_router(ia.router)
app.include_router(proyectos.router, prefix="/api")
app.include_router(tienda.router, prefix="/api")

# Directorio frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
FRONTEND_DIR = os.path.abspath(FRONTEND_DIR)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/{path:path}")
def serve_frontend(path: str):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
