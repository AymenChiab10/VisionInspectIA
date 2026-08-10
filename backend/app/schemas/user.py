"""
Schemas Pydantic lies a l'utilisateur (Partie authentification).

UserCreate  : donnees recues lors de l'inscription (POST /register).
UserLogin   : donnees recues lors de la connexion (POST /login).
UserResponse: donnees renvoyees au client (jamais le mot de passe).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# Note : l'email est type "str" et non "EmailStr". EmailStr necessiterait la
# dependance supplementaire "email-validator", non prevue dans la liste des
# bibliotheques autorisees pour cette partie. L'unicite de l'email reste
# garantie par la contrainte UNIQUE en base (voir models/user.py).


class UserCreate(BaseModel):
    """Donnees necessaires a la creation d'un compte."""

    first_name: str
    last_name: str
    email: str
    # bcrypt ignore silencieusement tout ce qui depasse 72 octets : on borne
    # explicitement la longueur plutot que de laisser un mot de passe se
    # faire tronquer sans que l'utilisateur en soit informe.
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    """Donnees necessaires a la connexion."""

    email: str
    password: str


class UserResponse(BaseModel):
    """Representation publique d'un utilisateur (sans le mot de passe)."""

    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    created_at: datetime

    # Permet de construire ce schema directement depuis un objet SQLAlchemy User.
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Donnees necessaires a la mise a jour du profil (PUT /users/me)."""

    first_name: str
    last_name: str
    email: str


class PasswordUpdate(BaseModel):
    """Donnees necessaires au changement de mot de passe."""

    current_password: str
    new_password: str = Field(min_length=6, max_length=72)
