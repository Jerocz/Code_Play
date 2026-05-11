import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes import python, javascript, cpp, progreso, ejecutar, ia

app = FastAPI(title="CodeTutor API", version="1.0.0")

# Registrar routers
app.include_router(python.router, prefix="/api")
app.include_router(javascript.router, prefix="/api")
app.include_router(cpp.router, prefix="/api")
app.include_router(progreso.router, prefix="/api")
app.include_router(ejecutar.router, prefix="/api")
app.include_router(ia.router)

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
