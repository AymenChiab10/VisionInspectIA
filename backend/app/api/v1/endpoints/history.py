"""
Routes de l'historique des inspections.

Aucune logique metier ici : chaque route ne fait qu'appeler
app/services/history_service.py.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.inspection import InspectionResponse
from app.services import history_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module history est charge."""
    return {"module": "history", "status": "ready"}


@router.get("", response_model=list[InspectionResponse])
def read_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retourne l'historique complet des inspections de l'utilisateur connecte."""
    return history_service.get_user_history(db, current_user)


@router.get("/{inspection_id}", response_model=InspectionResponse)
def read_inspection(
    inspection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retourne le detail d'une inspection appartenant a l'utilisateur connecte."""
    return history_service.get_inspection(db, current_user, inspection_id)


@router.delete("/{inspection_id}")
def remove_inspection(
    inspection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Supprime une inspection (base + image) appartenant a l'utilisateur connecte."""
    return history_service.delete_inspection(db, current_user, inspection_id)
