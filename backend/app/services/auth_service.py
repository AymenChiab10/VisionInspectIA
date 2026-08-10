"""
Logique metier de l'authentification.

Ce module concentre toute la logique (verification, hachage, acces base de
donnees, generation du JWT). Les routes (api/v1/endpoints/auth.py) ne font
qu'appeler ces fonctions.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin


def register_user(db: Session, user_data: UserCreate) -> User:
    """
    Cree un nouvel utilisateur.

    - Verifie que l'email n'est pas deja utilise.
    - Hash le mot de passe avant de l'enregistrer.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte existe deja avec cet email.",
        )

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, credentials: UserLogin) -> str:
    """
    Verifie les identifiants d'un utilisateur et retourne un JWT si valides.

    Leve une erreur 401 si l'email est inconnu ou si le mot de passe est
    incorrect (le message reste volontairement identique dans les deux cas,
    pour ne pas indiquer si un email existe en base).
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
        )

    return create_access_token(subject=user.email)
