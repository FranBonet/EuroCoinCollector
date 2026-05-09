"""Endpoints para la lista de deseos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ListaDeseosRequest, ListaDeseosResponse
from .. import crud

router = APIRouter(tags=["Lista de Deseos"])


@router.get("/lista_deseos", response_model=list[ListaDeseosResponse])
def listar_deseos(db: Session = Depends(get_db)):
    """Devuelve toda la lista de deseos."""
    return crud.obtener_lista_deseos(db)


@router.post("/lista_deseos/{id_moneda}", response_model=ListaDeseosResponse, status_code=201)
def agregar_deseo(id_moneda: int, datos: ListaDeseosRequest, db: Session = Depends(get_db)):
    """Añade una moneda a la lista de deseos."""
    return _crear_deseo_validado(db, id_moneda, datos)


@router.delete("/lista_deseos/{id_moneda}", status_code=204)
def eliminar_deseo(id_moneda: int, db: Session = Depends(get_db)):
    """Elimina una moneda de la lista de deseos."""
    return _eliminar_deseo_validado(db, id_moneda)


def _validar_moneda_existe(db: Session, id_moneda: int) -> None:
    """Lanza 404 si la moneda no existe."""
    if not crud.buscar_moneda_por_id(db, id_moneda):
        raise HTTPException(status_code=404, detail="Moneda no encontrada")


def _validar_deseo_no_duplicado(db: Session, id_moneda: int) -> None:
    """Lanza 409 si la moneda ya está en la lista de deseos."""
    if crud.buscar_deseo_por_moneda(db, id_moneda):
        raise HTTPException(status_code=409, detail="La moneda ya está en la lista de deseos")


def _crear_deseo_validado(db: Session, id_moneda: int, datos: ListaDeseosRequest):
    """Valida y crea un nuevo deseo."""
    _validar_moneda_existe(db, id_moneda)
    _validar_deseo_no_duplicado(db, id_moneda)
    return crud.crear_deseo(db, id_moneda, datos.prioridad, datos.notas)


def _eliminar_deseo_validado(db: Session, id_moneda: int) -> None:
    """Valida que existe y elimina un deseo."""
    deseo = crud.buscar_deseo_por_moneda(db, id_moneda)
    if not deseo:
        raise HTTPException(status_code=404, detail="La moneda no está en la lista de deseos")
    crud.eliminar_deseo(db, deseo)
