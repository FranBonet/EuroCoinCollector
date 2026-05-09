"""Esquemas Pydantic para validación de datos en request/response."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


# ── País ──────────────────────────────────────────────────────

class PaisResponse(BaseModel):
    """Esquema de respuesta para un país."""
    model_config = ConfigDict(from_attributes=True)

    id_pais: int
    nombre: str
    codigo_iso: str


# ── Moneda ────────────────────────────────────────────────────

class MonedaResponse(BaseModel):
    """Esquema de respuesta para una moneda del catálogo."""
    model_config = ConfigDict(from_attributes=True)

    id_moneda: int
    id_pais: int
    nombre: str
    anyo: int
    imagen_url: Optional[str] = None
    tipo: str
    precio_mercado: Optional[Decimal] = None
    pais: Optional[PaisResponse] = None


# ── Colección ─────────────────────────────────────────────────

class ColeccionRequest(BaseModel):
    """Esquema de petición para actualizar la colección."""
    cantidad: int = 1
    fecha: Optional[date] = None
    notas: Optional[str] = None


class ColeccionResponse(BaseModel):
    """Esquema de respuesta para una entrada de la colección."""
    model_config = ConfigDict(from_attributes=True)

    id_coleccion: int
    id_moneda: int
    cantidad: int
    fecha: Optional[date] = None
    notas: Optional[str] = None
    moneda: Optional[MonedaResponse] = None


# ── Lista de Deseos ───────────────────────────────────────────

class ListaDeseosRequest(BaseModel):
    """Esquema de petición para añadir a la lista de deseos."""
    prioridad: Literal["alta", "media", "baja"] = "media"
    notas: Optional[str] = None


class ListaDeseosResponse(BaseModel):
    """Esquema de respuesta para un deseo."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_moneda: int
    prioridad: str
    notas: Optional[str] = None
    moneda: Optional[MonedaResponse] = None


# ── Estadísticas ──────────────────────────────────────────────

class EstadisticasResponse(BaseModel):
    """Esquema de respuesta para las estadísticas de la colección."""
    total_catalogo: int
    total_poseidas: int
    total_cantidad: int
    porcentaje_completado: float
    valor_estimado: Decimal


# ── Intercambio ───────────────────────────────────────────────

class IntercambioRequest(BaseModel):
    """Esquema de petición para publicar un intercambio."""
    nombre_usuario: str
    id_moneda_ofrecida: int
    id_moneda_buscada: Optional[int] = None
    descripcion: Optional[str] = None
    contacto: str


class IntercambioResponse(BaseModel):
    """Esquema de respuesta para un intercambio."""
    model_config = ConfigDict(from_attributes=True)

    id_intercambio: int
    nombre_usuario: str
    id_moneda_ofrecida: int
    id_moneda_buscada: Optional[int] = None
    descripcion: Optional[str] = None
    contacto: str
    fecha_publicacion: datetime
    estado: str
    moneda_ofrecida: Optional[MonedaResponse] = None
    moneda_buscada: Optional[MonedaResponse] = None
