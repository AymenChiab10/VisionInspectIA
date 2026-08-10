"""
Connexion SQLAlchemy a MySQL.

Definit le moteur (engine), la fabrique de sessions (SessionLocal), la
classe de base declarative (Base) ainsi que la dependance FastAPI get_db(),
utilisee pour ouvrir/fermer une session a chaque requete.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# pool_pre_ping evite les erreurs de connexion "perdue" (MySQL ferme les
# connexions inactives apres un certain temps).
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Fournit une session SQLAlchemy a une route, puis la ferme systematiquement."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
