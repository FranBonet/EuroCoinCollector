"""Endpoints para países."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PaisResponse
from .. import crud

router = APIRouter(tags=["Países"])


@router.get("/paises", response_model=list[PaisResponse])
def listar_paises(db: Session = Depends(get_db)):
    """Devuelve la lista de todos los países emisores."""
    return crud.obtener_todos_paises(db)
