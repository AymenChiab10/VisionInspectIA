"""
Logique metier de la generation de rapports PDF.

Recupere l'inspection demandee (en verifiant qu'elle appartient bien a
l'utilisateur connecte), puis delegue la construction du PDF a
app/utils/pdf_utils.py.
"""

from io import BytesIO

from sqlalchemy.orm import Session

from app.models.user import User
from app.services.history_service import get_inspection
from app.utils.pdf_utils import generate_pdf


def generate_report(db: Session, current_user: User, inspection_id: int) -> BytesIO:
    """
    Genere le rapport PDF d'une inspection appartenant a l'utilisateur connecte.

    Reutilise history_service.get_inspection(), qui leve deja une 404 si
    l'inspection est introuvable ou appartient a un autre utilisateur,
    evitant de dupliquer ce controle d'appartenance.
    """
    inspection = get_inspection(db, current_user, inspection_id)
    return generate_pdf(inspection, current_user)
