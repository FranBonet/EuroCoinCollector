"""Conexión y gestión de sesiones de base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import get_database_url


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""
    pass


engine = create_engine(get_database_url())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Genera una sesión de base de datos y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
