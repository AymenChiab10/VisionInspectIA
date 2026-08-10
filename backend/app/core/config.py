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

    # Hote et port utilises pour lancer le serveur (python -m app.main)
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

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
    def DATABASE_URL(self) -> str:
        """Construit automatiquement l'URL de connexion SQLAlchemy/PyMySQL."""
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


settings = Settings()
