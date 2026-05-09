"""Endpoint para exportar la colección a CSV."""

import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud

router = APIRouter(tags=["Exportar"])

CSV_HEADERS = ["País", "Moneda", "Año", "Tipo", "Precio Mercado (€)", "Cantidad", "Notas"]


@router.get("/exportar/csv")
def exportar_csv(db: Session = Depends(get_db)):
    """Descarga la colección completa como archivo CSV."""
    return _generar_respuesta_csv(db)


def _generar_respuesta_csv(db: Session) -> StreamingResponse:
    """Genera la respuesta HTTP con el CSV adjunto."""
    return StreamingResponse(
        content=_crear_contenido_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=coleccion_euros.csv"},
    )


def _crear_contenido_csv(db: Session) -> io.StringIO:
    """Crea el contenido CSV con todas las monedas."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(CSV_HEADERS)
    _escribir_filas_csv(writer, crud.obtener_datos_exportacion(db))
    output.seek(0)
    return output


def _escribir_filas_csv(writer: csv.writer, monedas: list) -> None:
    """Escribe todas las filas de monedas en el CSV."""
    for moneda in monedas:
        writer.writerow(_moneda_a_fila_csv(moneda))


def _moneda_a_fila_csv(moneda) -> list:
    """Convierte una moneda a una fila CSV."""
    return [
        moneda.pais.nombre,
        moneda.nombre,
        moneda.anyo,
        moneda.tipo,
        moneda.precio_mercado or "",
        moneda.coleccion.cantidad if moneda.coleccion else 0,
        moneda.coleccion.notas if moneda.coleccion else "",
    ]
