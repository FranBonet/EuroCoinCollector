"""Endpoints para el tablón de intercambios de monedas."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import IntercambioRequest, IntercambioResponse
from .. import crud

router = APIRouter(tags=["Intercambios"])


@router.get("/intercambios", response_model=list[IntercambioResponse])
def listar_intercambios(db: Session = Depends(get_db)):
    """Devuelve todos los intercambios activos."""
    return crud.obtener_intercambios_activos(db)


@router.get("/intercambios/todos", response_model=list[IntercambioResponse])
def listar_todos_intercambios(db: Session = Depends(get_db)):
    """Devuelve todos los intercambios (activos y cerrados)."""
    return crud.obtener_todos_intercambios(db)


@router.post("/intercambios", response_model=IntercambioResponse, status_code=201)
def crear_intercambio(datos: IntercambioRequest, db: Session = Depends(get_db)):
    """Publica un nuevo intercambio en el tablón."""
    return _crear_intercambio_validado(db, datos)


@router.patch("/intercambios/{id_intercambio}/cerrar", response_model=IntercambioResponse)
def cerrar_intercambio(id_intercambio: int, db: Session = Depends(get_db)):
    """Marca un intercambio como cerrado."""
    return _cerrar_intercambio_validado(db, id_intercambio)


@router.delete("/intercambios/{id_intercambio}", status_code=204)
def eliminar_intercambio(id_intercambio: int, db: Session = Depends(get_db)):
    """Elimina un intercambio del tablón."""
    return _eliminar_intercambio_validado(db, id_intercambio)


def _validar_moneda_existe(db: Session, id_moneda: int) -> None:
    """Lanza 404 si la moneda no existe."""
    if not crud.buscar_moneda_por_id(db, id_moneda):
        raise HTTPException(status_code=404, detail="Moneda no encontrada")


def _crear_intercambio_validado(db: Session, datos: IntercambioRequest):
    """Valida y crea un nuevo intercambio."""
    _validar_moneda_existe(db, datos.id_moneda_ofrecida)
    if datos.id_moneda_buscada:
        _validar_moneda_existe(db, datos.id_moneda_buscada)
    return crud.crear_intercambio(
        db, datos.nombre_usuario, datos.id_moneda_ofrecida,
        datos.id_moneda_buscada, datos.descripcion, datos.contacto,
    )


def _cerrar_intercambio_validado(db: Session, id_intercambio: int):
    """Valida y cierra un intercambio."""
    intercambio = crud.buscar_intercambio_por_id(db, id_intercambio)
    if not intercambio:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    crud.cerrar_intercambio(intercambio)
    return crud.guardar_en_db(db, intercambio)


def _eliminar_intercambio_validado(db: Session, id_intercambio: int) -> None:
    """Valida y elimina un intercambio."""
    intercambio = crud.buscar_intercambio_por_id(db, id_intercambio)
    if not intercambio:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    crud.eliminar_intercambio(db, intercambio)
