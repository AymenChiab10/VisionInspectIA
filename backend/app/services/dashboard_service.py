"""
Logique metier des statistiques du dashboard.

Toutes les statistiques sont calculees directement par une requete SQL
agregee (COUNT, SUM conditionnel, AVG) sur MySQL, jamais stockees ni
recalculees en memoire.
"""

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.models.user import User
from app.schemas.inspection import DashboardStatistics


def get_dashboard_statistics(db: Session, current_user: User) -> DashboardStatistics:
    """Calcule les statistiques agregees des inspections de l'utilisateur connecte."""

    result = (
        db.query(
            func.count(Inspection.id).label("total_inspections"),
            func.sum(case((Inspection.predicted_class == "good", 1), else_=0)).label("total_good"),
            func.sum(case((Inspection.predicted_class == "broken_large", 1), else_=0)).label("total_broken_large"),
            func.sum(case((Inspection.predicted_class == "broken_small", 1), else_=0)).label("total_broken_small"),
            func.sum(case((Inspection.predicted_class == "contamination", 1), else_=0)).label("total_contamination"),
            func.avg(Inspection.confidence).label("average_confidence"),
        )
        .filter(Inspection.user_id == current_user.id)
        .one()
    )

    # confidence est stockee en base sous forme de fraction (0-1) ; le
    # dashboard l'exprime en pourcentage, conformement au format attendu
    # (ex: 98.21) plutot qu'une fraction brute (0.9821).
    average_confidence_percent = (
        round(float(result.average_confidence) * 100, 2)
        if result.average_confidence is not None
        else 0.0
    )

    return DashboardStatistics(
        total_inspections=result.total_inspections or 0,
        total_good=result.total_good or 0,
        total_broken_large=result.total_broken_large or 0,
        total_broken_small=result.total_broken_small or 0,
        total_contamination=result.total_contamination or 0,
        average_confidence=average_confidence_percent,
    )
