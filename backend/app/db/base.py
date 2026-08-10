"""
Point d'import centralise de la Base declarative et de tous les modeles.

Ce module doit etre importe (directement ou indirectement) avant tout appel
a Base.metadata.create_all() ou par Alembic, afin que SQLAlchemy connaisse
l'ensemble des tables declarees dans app/models/.
"""

from app.db.session import Base  # noqa: F401

# Import de tous les modeles pour qu'ils s'enregistrent dans Base.metadata.
from app.models.user import User  # noqa: F401
from app.models.inspection import Inspection  # noqa: F401
