"""
Routes de gestion des utilisateurs.

Aucune logique metier ici : chaque route ne fait qu'appeler
app/services/user_service.py.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import PasswordUpdate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module users est charge."""
    return {"module": "users", "status": "ready"}


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Met a jour le profil (prenom, nom, email) de l'utilisateur connecte."""
    return user_service.update_profile(db, current_user, data)


@router.put("/me/password")
def update_password(
    data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change le mot de passe de l'utilisateur connecte."""
    return user_service.update_password(db, current_user, data)


@router.delete("/me")
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Supprime definitivement le compte de l'utilisateur connecte."""
    return user_service.delete_account(db, current_user)
