from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.python import router as python_router
from routes.progreso import router as progreso_router

app = FastAPI(
    title="CodeTutor API",
    description="Backend del juego educativo para aprender programación",
    version="1.0.0"
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

@app.get("/")
def home():
    return {
        "mensaje": "CodeTutor API funcionando 🚀"
    }