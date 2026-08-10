"""
Routes d'authentification.

Aucune logique metier ici : chaque route ne fait qu'appeler
app/services/auth_service.py.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import auth_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module auth est charge."""
    return {"module": "auth", "status": "ready"}


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Cree un nouveau compte utilisateur."""
    return auth_service.register_user(db, user_data)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authentifie un utilisateur et retourne un JWT Bearer."""
    access_token = auth_service.authenticate_user(db, credentials)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Retourne les informations de l'utilisateur actuellement connecte."""
    return current_user


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)) -> dict:
    """
    Deconnexion simple : verifie que le JWT fourni est valide, puis confirme.

    Le backend ne stocke aucun JWT (pas de blacklist, pas de refresh token) :
    c'est au frontend de supprimer le token localement apres cet appel.
    """
    return {"message": "Logout successful"}
