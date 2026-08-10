"""
Module de securite de l'application.

Fournit les trois briques necessaires a une authentification JWT simple :
- hash_password() / verify_password() : hachage bcrypt des mots de passe ;
- create_access_token() : generation d'un JWT Bearer signe.

Pas de refresh token, pas d'OAuth2 complet : un JWT Bearer simple suffit
pour ce projet.
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexte de hachage : bcrypt uniquement, avec detection automatique
# des hashs a re-hacher si l'algorithme devient "deprecated" plus tard.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Retourne le hash bcrypt d'un mot de passe en clair."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifie qu'un mot de passe en clair correspond a son hash bcrypt."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Cree un JWT Bearer signe pour l'utilisateur identifie par `subject`
    (ici, l'email de l'utilisateur), avec une date d'expiration.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
