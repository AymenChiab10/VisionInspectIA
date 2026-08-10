"""
Schemas Pydantic lies aux inspections (Partie historique / dashboard).

InspectionResponse : representation publique d'une inspection.
DashboardStatistics : statistiques agregees sur les inspections de l'utilisateur.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InspectionResponse(BaseModel):
    """Representation publique d'une inspection (historique)."""

    id: int
    image_path: str
    predicted_class: str
    confidence: float
    created_at: datetime

    # Permet de construire ce schema directement depuis un objet SQLAlchemy Inspection.
    model_config = ConfigDict(from_attributes=True)


class DashboardStatistics(BaseModel):
    """Statistiques agregees sur les inspections de l'utilisateur connecte."""

    total_inspections: int
    total_good: int
    total_broken_large: int
    total_broken_small: int
    total_contamination: int
    average_confidence: float
