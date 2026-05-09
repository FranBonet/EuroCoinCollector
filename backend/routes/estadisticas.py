"""Endpoint para estadísticas de la colección."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import EstadisticasResponse
from .. import crud

router = APIRouter(tags=["Estadísticas"])


@router.get("/estadisticas", response_model=EstadisticasResponse)
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Devuelve las estadísticas completas de la colección."""
    return _construir_estadisticas(db)


def _construir_estadisticas(db) -> dict:
    """Calcula y devuelve todas las estadísticas."""
    total = crud.contar_total_catalogo(db)
    poseidas = crud.contar_monedas_poseidas(db)
    return {
        "total_catalogo": total,
        "total_poseidas": poseidas,
        "total_cantidad": crud.sumar_total_cantidad(db),
        "porcentaje_completado": crud.calcular_porcentaje(poseidas, total),
        "valor_estimado": crud.calcular_valor_estimado(db),
    }
