"""Tests para el endpoint /estadisticas."""


def test_estadisticas_sin_datos(client):
    """Devuelve estadísticas a cero cuando no hay monedas."""
    response = client.get("/estadisticas")
    assert response.status_code == 200
    assert response.json()["total_catalogo"] == 0
    assert response.json()["porcentaje_completado"] == 0.0


def test_estadisticas_con_monedas(client, moneda_quijote, moneda_comun_espana):
    """Cuenta correctamente el catálogo total."""
    response = client.get("/estadisticas")
    assert response.json()["total_catalogo"] == 2
    assert response.json()["total_poseidas"] == 0


def test_estadisticas_con_coleccion(client, moneda_quijote, moneda_comun_espana):
    """Calcula estadísticas con monedas en la colección."""
    client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 2})
    response = client.get("/estadisticas")
    datos = response.json()
    assert datos["total_poseidas"] == 1
    assert datos["total_cantidad"] == 2
    assert datos["porcentaje_completado"] == 50.0


def test_estadisticas_valor_estimado(client, moneda_quijote):
    """Calcula el valor estimado correctamente."""
    client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 3})
    response = client.get("/estadisticas")
    assert float(response.json()["valor_estimado"]) == 18.0
