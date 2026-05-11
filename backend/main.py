from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routes.python import router as python_router
from routes.javascript import router as javascript_router
from routes.cpp import router as cpp_router
from routes.progreso import router as progreso_router
from routes.ia import router as ia_router

app = FastAPI(title="CodeTutor API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(python_router)
app.include_router(javascript_router)
app.include_router(cpp_router)
app.include_router(progreso_router)
app.include_router(ia_router)

# Servir el frontend desde el servidor
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/api")
def api_info():
    return {
        "app": "CodeTutor 🚀",
        "version": "3.0",
        "lenguajes": ["python", "javascript", "cpp"],
        "docs": "/docs"
    }
