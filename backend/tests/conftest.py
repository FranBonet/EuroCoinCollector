"""Configuración compartida para los tests — fixtures y test database."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app
from backend.models import Pais, Moneda


# ── Motor SQLite en memoria para tests ────────────────────────

engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las destruye después."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def db_session():
    """Proporciona una sesión de base de datos limpia para cada test."""
    session = SessionTest()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """Proporciona un cliente HTTP de test con la DB inyectada."""
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def pais_espana(db_session) -> Pais:
    """Crea y devuelve un país España de prueba."""
    pais = Pais(nombre="España", codigo_iso="ES")
    db_session.add(pais)
    db_session.commit()
    db_session.refresh(pais)
    return pais


@pytest.fixture()
def pais_alemania(db_session) -> Pais:
    """Crea y devuelve un país Alemania de prueba."""
    pais = Pais(nombre="Alemania", codigo_iso="DE")
    db_session.add(pais)
    db_session.commit()
    db_session.refresh(pais)
    return pais


@pytest.fixture()
def moneda_quijote(db_session, pais_espana) -> Moneda:
    """Crea y devuelve una moneda Don Quijote de prueba."""
    moneda = Moneda(
        id_pais=pais_espana.id_pais,
        nombre="Don Quijote — IV Centenario",
        anyo=2005,
        tipo="conmemorativa",
        precio_mercado=6.00,
    )
    db_session.add(moneda)
    db_session.commit()
    db_session.refresh(moneda)
    return moneda


@pytest.fixture()
def moneda_comun_espana(db_session, pais_espana) -> Moneda:
    """Crea y devuelve una moneda común española de prueba."""
    moneda = Moneda(
        id_pais=pais_espana.id_pais,
        nombre="Rey Felipe VI — diseño común",
        anyo=2015,
        tipo="comun",
        precio_mercado=2.50,
    )
    db_session.add(moneda)
    db_session.commit()
    db_session.refresh(moneda)
    return moneda
