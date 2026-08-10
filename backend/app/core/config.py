"""
Configuration centrale de l'application.

Contient les parametres necessaires au demarrage du backend (Partie 3),
a la connexion MySQL (Partie 4) et au JWT (Partie 5).

Les parametres lies a TensorFlow et aux uploads seront ajoutes dans les
parties suivantes, au fur et a mesure de leur implementation.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parametres de configuration, surchargeables via un fichier .env."""

    # Informations sur le projet (utilisees pour Swagger / ReDoc)
    PROJECT_NAME: str = "Bottle Defect Detection API"
    PROJECT_DESCRIPTION: str = (
        "API de detection de defauts sur bouteilles par vision par ordinateur (MobileNetV2)."
    )
    API_VERSION: str = "1.0.0"

    # Prefixe commun a toutes les routes de la version 1 de l'API
    API_PREFIX: str = "/api/v1"

    # Mode debug (reload, messages d'erreur detailles, etc.)
    DEBUG: bool = True

    # Hote et port utilises pour lancer le serveur (python -m app.main).
    # 0.0.0.0 par defaut : necessaire pour etre joignable depuis l'exterieur
    # du conteneur sur une plateforme cloud (Render/Railway), et fonctionne
    # aussi bien en local. PORT est lu si la plateforme le fournit (variable
    # standard sur Render/Railway) ; sinon BACKEND_PORT (defaut 8000) est
    # utilise, pour ne pas casser le lancement local existant.
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    PORT: int | None = None

    # Chemin absolu vers le fichier .keras du modele, si l'on souhaite
    # surcharger l'emplacement par defaut (backend/app/ml/model_files/).
    MODEL_PATH: str | None = None

    # Origines autorisees pour le CORS, separees par des virgules
    # (ex: "https://mon-frontend.vercel.app,http://localhost:5173").
    # Defaut : uniquement le frontend Vite local.
    CORS_ORIGINS: str = "http://localhost:5173"

    # Connexion MySQL (valeurs lues depuis .env, jamais codees en dur)
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "visioninspectia"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""

    # JWT (valeurs lues depuis .env, jamais codees en dur)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def RUNTIME_PORT(self) -> int:
        """Port effectif d'ecoute : PORT (fourni par la plateforme cloud) si present, sinon BACKEND_PORT."""
        return self.PORT or self.BACKEND_PORT

    @property
    def CORS_ORIGINS_LIST(self) -> list[str]:
        """Liste des origines CORS autorisees, obtenue en decoupant CORS_ORIGINS sur les virgules."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def DATABASE_URL(self) -> str:
        """Construit automatiquement l'URL de connexion SQLAlchemy/PyMySQL."""
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


settings = Settings()
