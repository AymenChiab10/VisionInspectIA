"""
Initialisation de la base de donnees.

Cree les tables si elles n'existent pas encore, a partir des modeles
declares dans app/db/base.py. N'insere aucune donnee, ne cree aucun
utilisateur administrateur.
"""

from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    """Cree les tables manquantes en base a partir des modeles SQLAlchemy."""
    Base.metadata.create_all(bind=engine)
