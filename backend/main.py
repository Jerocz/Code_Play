from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routes.python import router as python_router
from routes.progreso import router as progreso_router
from routes.ia import router as ia_router

app = FastAPI(
    title="CodeTutor API",
    description="Backend del juego para aprender a programar",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(python_router)
app.include_router(progreso_router)
app.include_router(ia_router)

@app.get("/")
def home():
    return {
        "app": "CodeTutor 🚀",
        "version": "2.0",
        "docs": "/docs",
        "endpoints": {
            "modulos": "/python/modulos",
            "progreso": "/progreso",
            "ia": "/ia/preguntar",
            "estado_ia": "/ia/estado"
        }
    }
