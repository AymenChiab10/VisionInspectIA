"""
Point d'entree de l'application FastAPI.

Cree l'application, configure le CORS, enregistre le routeur principal
de l'API et expose un endpoint racine de verification.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.router import api_router
from app.ml.model_loader import model_loader

# backend/app/main.py -> backend/uploads
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"

# Importe Base + tous les modeles (User, Inspection) une seule fois, au
# demarrage de l'application. Necessaire pour que SQLAlchemy puisse
# resoudre les relationship() declarees par nom de classe (ex: "Inspection"
# dans models/user.py), quel que soit l'ordre d'import des routes ensuite.
from app.db import base  # noqa: F401

# Origines autorisees pour le CORS.
# A ce stade, seul le frontend React (Vite, port par defaut 5173) est autorise.
# Liste volontairement isolee ici pour rester facile a completer plus tard
# (environnement de staging, production, etc.).
ALLOWED_ORIGINS = [
    "http://localhost:5173",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modele MobileNetV2 une seule fois, au demarrage du serveur."""
    model_loader.load_model()
    print("MobileNetV2 loaded successfully", flush=True)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

# Sert les images uploadees en fichiers statiques (ex: /uploads/xxx.png),
# necessaire pour que le frontend puisse afficher les miniatures de
# l'historique. Le chemin stocke en base (Inspection.image_path,
# ex: "uploads/xxx.png") correspond directement a cette URL.
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


@app.get("/")
def read_root() -> dict:
    """Endpoint racine : confirme que l'API est en ligne."""
    return {
        "message": "Bottle Defect Detection API",
        "status": "running",
        "version": settings.API_VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
