"""
Schemas Pydantic lies au token JWT (Partie authentification).

Token     : reponse renvoyee au client apres un login reussi.
TokenData : contenu decode du JWT, utilise en interne (api/deps.py).
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Reponse renvoyee par POST /login."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Donnees extraites du JWT decode."""

    email: str | None = None
