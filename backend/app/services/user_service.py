"""
Logique metier de la gestion du compte utilisateur (profil, mot de passe,
suppression). Les routes (api/v1/endpoints/users.py) ne font qu'appeler
ces fonctions.
"""

from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.inspection import Inspection
from app.models.user import User
from app.schemas.user import PasswordUpdate, UserUpdate

# backend/app/services/user_service.py -> backend/
BACKEND_ROOT = Path(__file__).resolve().parents[2]


def update_profile(db: Session, current_user: User, data: UserUpdate) -> User:
    """
    Met a jour prenom/nom/email de l'utilisateur connecte.

    Verifie que le nouvel email n'est pas deja utilise par un AUTRE
    utilisateur (l'unicite reste garantie par la contrainte UNIQUE en base).
    """
    if data.email != current_user.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un compte existe deja avec cet email.",
            )

    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    current_user.email = data.email

    db.commit()
    db.refresh(current_user)

    return current_user


def update_password(db: Session, current_user: User, data: PasswordUpdate) -> dict:
    """
    Change le mot de passe de l'utilisateur connecte, apres verification
    du mot de passe actuel.
    """
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect.",
        )

    current_user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully."}


def delete_account(db: Session, current_user: User) -> dict:
    """
    Supprime definitivement le compte de l'utilisateur connecte, ainsi que
    toutes ses inspections (base de donnees + images sur le disque).
    """
    inspections = db.query(Inspection).filter(Inspection.user_id == current_user.id).all()

    for inspection in inspections:
        image_path = BACKEND_ROOT / inspection.image_path
        if image_path.exists():
            image_path.unlink()
        db.delete(inspection)

    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully."}
