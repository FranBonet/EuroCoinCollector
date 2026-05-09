"""Tests para el endpoint /exportar/csv."""


def test_exportar_csv_vacio(client):
    """Devuelve un CSV con solo cabeceras cuando no hay datos."""
    response = client.get("/exportar/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]


def test_exportar_csv_con_datos(client, moneda_quijote):
    """Incluye la moneda en el CSV exportado."""
    response = client.get("/exportar/csv")
    assert "Don Quijote" in response.text


def test_exportar_csv_cabeceras(client):
    """El CSV contiene las cabeceras correctas."""
    response = client.get("/exportar/csv")
    assert "País" in response.text
    assert "Moneda" in response.text


def test_exportar_csv_content_disposition(client):
    """El CSV se descarga como archivo adjunto."""
    response = client.get("/exportar/csv")
    assert "attachment" in response.headers.get("content-disposition", "")
