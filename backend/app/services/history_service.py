"""
Logique metier de l'historique des inspections.

Ce module concentre toute la logique (acces base de donnees, controle
d'appartenance, suppression du fichier associe). Les routes
(api/v1/endpoints/history.py) ne font qu'appeler ces fonctions.
"""

from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.models.user import User

# backend/app/services/history_service.py -> backend/
BACKEND_ROOT = Path(__file__).resolve().parents[2]


def get_user_history(db: Session, current_user: User) -> list[Inspection]:
    """Retourne toutes les inspections de l'utilisateur connecte, du plus recent au plus ancien."""
    return (
        db.query(Inspection)
        .filter(Inspection.user_id == current_user.id)
        .order_by(Inspection.created_at.desc())
        .all()
    )


def get_inspection(db: Session, current_user: User, inspection_id: int) -> Inspection:
    """
    Retourne une inspection appartenant a l'utilisateur connecte.

    Leve une 404 si l'inspection n'existe pas ou appartient a un autre
    utilisateur (le message reste identique dans les deux cas, pour ne
    pas reveler l'existence d'inspections d'autrui).
    """
    inspection = (
        db.query(Inspection)
        .filter(Inspection.id == inspection_id, Inspection.user_id == current_user.id)
        .first()
    )

    if inspection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection introuvable.",
        )

    return inspection


def delete_inspection(db: Session, current_user: User, inspection_id: int) -> dict:
    """
    Supprime une inspection appartenant a l'utilisateur connecte : la ligne
    en base ainsi que l'image associee dans uploads/.
    """
    inspection = get_inspection(db, current_user, inspection_id)

    image_path = BACKEND_ROOT / inspection.image_path
    if image_path.exists():
        image_path.unlink()

    db.delete(inspection)
    db.commit()

    return {"message": "Inspection supprimee avec succes."}
