"""Definición de modelos ORM — tablas de la base de datos."""

from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Pais(Base):
    """Modelo ORM para la tabla pais."""

    __tablename__ = "pais"

    id_pais = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo_iso = Column(String(2), nullable=False, unique=True)

    monedas = relationship("Moneda", back_populates="pais")


class Moneda(Base):
    """Modelo ORM para la tabla moneda."""

    __tablename__ = "moneda"

    id_moneda = Column(Integer, primary_key=True, autoincrement=True)
    id_pais = Column(Integer, ForeignKey("pais.id_pais"), nullable=False)
    nombre = Column(String(255), nullable=False)
    anyo = Column(Integer, nullable=False)
    imagen_url = Column(String(512), nullable=True)
    tipo = Column(Enum("comun", "conmemorativa"), nullable=False, default="conmemorativa")
    precio_mercado = Column(DECIMAL(6, 2), nullable=True)

    pais = relationship("Pais", back_populates="monedas")
    coleccion = relationship("Coleccion", back_populates="moneda", uselist=False)
    deseo = relationship("ListaDeseos", back_populates="moneda", uselist=False)


class Coleccion(Base):
    """Modelo ORM para la tabla coleccion."""

    __tablename__ = "coleccion"

    id_coleccion = Column(Integer, primary_key=True, autoincrement=True)
    id_moneda = Column(Integer, ForeignKey("moneda.id_moneda"), nullable=False, unique=True)
    cantidad = Column(Integer, nullable=False, default=0)
    fecha = Column(Date, nullable=True)
    notas = Column(Text, nullable=True)

    moneda = relationship("Moneda", back_populates="coleccion")


class ListaDeseos(Base):
    """Modelo ORM para la tabla lista_deseos."""

    __tablename__ = "lista_deseos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_moneda = Column(Integer, ForeignKey("moneda.id_moneda"), nullable=False, unique=True)
    prioridad = Column(Enum("alta", "media", "baja"), nullable=False, default="media")
    notas = Column(Text, nullable=True)

    moneda = relationship("Moneda", back_populates="deseo")


class Intercambio(Base):
    """Modelo ORM para la tabla intercambio."""

    __tablename__ = "intercambio"

    id_intercambio = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(100), nullable=False)
    id_moneda_ofrecida = Column(Integer, ForeignKey("moneda.id_moneda"), nullable=False)
    id_moneda_buscada = Column(Integer, ForeignKey("moneda.id_moneda"), nullable=True)
    descripcion = Column(Text, nullable=True)
    contacto = Column(String(255), nullable=False)
    fecha_publicacion = Column(DateTime, nullable=False, server_default=func.now())
    estado = Column(Enum("activo", "cerrado"), nullable=False, default="activo")

    moneda_ofrecida = relationship("Moneda", foreign_keys=[id_moneda_ofrecida])
    moneda_buscada = relationship("Moneda", foreign_keys=[id_moneda_buscada])
