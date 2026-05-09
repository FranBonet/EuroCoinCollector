"""Endpoints para la gestión de la colección personal."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ColeccionRequest, ColeccionResponse, MonedaResponse
from .. import crud

router = APIRouter(tags=["Colección"])


@router.get("/coleccion", response_model=list[ColeccionResponse])
def listar_coleccion(
    pais: Optional[int] = Query(None, description="Filtrar por ID del país"),
    db: Session = Depends(get_db),
):
    """Devuelve todas las monedas de la colección con cantidad > 0."""
    return crud.obtener_coleccion_por_pais(db, pais)


@router.get("/coleccion/faltantes", response_model=list[MonedaResponse])
def listar_faltantes(
    pais: Optional[int] = Query(None, description="Filtrar por ID del país"),
    db: Session = Depends(get_db),
):
    """Devuelve las monedas del catálogo que NO están en la colección."""
    return crud.obtener_monedas_faltantes(db, pais)


@router.put("/coleccion/{id_moneda}", response_model=ColeccionResponse)
def actualizar_coleccion(id_moneda: int, datos: ColeccionRequest, db: Session = Depends(get_db)):
    """Actualiza o crea una entrada en la colección (upsert)."""
    return _upsert_coleccion(db, id_moneda, datos)


@router.delete("/coleccion/{id_moneda}", status_code=204)
def eliminar_de_coleccion(id_moneda: int, db: Session = Depends(get_db)):
    """Elimina una moneda de la colección."""
    return _eliminar_coleccion_validada(db, id_moneda)


def _validar_moneda_existe(db: Session, id_moneda: int) -> None:
    """Lanza 404 si la moneda no existe en el catálogo."""
    if not crud.buscar_moneda_por_id(db, id_moneda):
        raise HTTPException(status_code=404, detail="Moneda no encontrada en el catálogo")


def _upsert_coleccion(db: Session, id_moneda: int, datos: ColeccionRequest):
    """Crea o actualiza una entrada de colección."""
    _validar_moneda_existe(db, id_moneda)
    entrada = crud.buscar_entrada_coleccion(db, id_moneda)
    if entrada:
        crud.actualizar_campos_coleccion(entrada, datos.cantidad, datos.fecha, datos.notas)
        return crud.guardar_en_db(db, entrada)
    return crud.crear_entrada_coleccion(db, id_moneda, datos.cantidad, datos.fecha, datos.notas)


def _eliminar_coleccion_validada(db: Session, id_moneda: int) -> None:
    """Valida que existe y elimina la entrada de colección."""
    entrada = crud.buscar_entrada_coleccion(db, id_moneda)
    if not entrada:
        raise HTTPException(status_code=404, detail="La moneda no está en la colección")
    crud.eliminar_entrada_coleccion(db, entrada)
