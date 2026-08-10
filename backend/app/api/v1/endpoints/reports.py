"""
Routes de generation de rapports PDF.

Aucune logique metier ici : la route delegue entierement a
app/services/report_service.py et se contente de retourner le flux PDF.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services import report_service

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Endpoint de test confirmant que le module reports est charge."""
    return {"module": "reports", "status": "ready"}


@router.get("/{inspection_id}")
def download_report(
    inspection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Telecharge le rapport PDF d'une inspection appartenant a l'utilisateur connecte."""
    pdf_buffer = report_service.generate_report(db, current_user, inspection_id)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=inspection_{inspection_id}.pdf"
        },
    )
