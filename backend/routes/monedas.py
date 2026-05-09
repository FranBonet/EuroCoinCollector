"""Endpoints para el catálogo de monedas."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import MonedaResponse
from .. import crud

router = APIRouter(tags=["Monedas"])


@router.get("/monedas", response_model=list[MonedaResponse])
def listar_monedas(
    tipo: Optional[str] = Query(None, description="comun o conmemorativa"),
    pais: Optional[int] = Query(None, description="ID del país"),
    anyo: Optional[int] = Query(None, description="Año de emisión"),
    db: Session = Depends(get_db),
):
    """Devuelve el catálogo de monedas con filtros opcionales."""
    return crud.buscar_monedas(db, tipo, pais, anyo)


@router.get("/monedas/{id_moneda}", response_model=MonedaResponse)
def obtener_moneda(id_moneda: int, db: Session = Depends(get_db)):
    """Devuelve una moneda por su ID o lanza 404."""
    return _moneda_o_404(db, id_moneda)


def _moneda_o_404(db: Session, id_moneda: int):
    """Busca una moneda y lanza 404 si no existe."""
    moneda = crud.buscar_moneda_por_id(db, id_moneda)
    if not moneda:
        raise HTTPException(status_code=404, detail="Moneda no encontrada")
    return moneda
