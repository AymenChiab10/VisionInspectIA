"""
Utilitaires pour la gestion des fichiers images uploades.
"""

import uuid
from pathlib import Path

from fastapi import HTTPException, status

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 Mo


def validate_image_file(filename: str, content: bytes) -> None:
    """
    Verifie que le fichier uploade est une image acceptee.

    - Extension autorisee : .jpg, .jpeg, .png
    - Taille maximale : 10 Mo

    Leve une HTTPException 400 si le fichier est invalide.
    """
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Format de fichier non autorise : '{extension}'. "
                "Formats acceptes : jpg, jpeg, png."
            ),
        )

    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fichier trop volumineux : la taille maximale autorisee est de 10 Mo.",
        )


def generate_unique_filename(original_filename: str) -> str:
    """Genere un nom de fichier unique, en conservant l'extension d'origine."""
    extension = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{extension}"
