"""
Routes de statistiques et de tableau de bord.

Aucune logique metier ici : la route ne fait qu'appeler
app/services/dashboard_service.py.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.inspection import DashboardStatistics
from app.services import dashboard_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module dashboard est charge."""
    return {"module": "dashboard", "status": "ready"}


@router.get("/statistics", response_model=DashboardStatistics)
def read_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retourne les statistiques agregees des inspections de l'utilisateur connecte."""
    return dashboard_service.get_dashboard_statistics(db, current_user)
