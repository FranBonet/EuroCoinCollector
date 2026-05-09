"""Tests para el endpoint /paises."""


def test_listar_paises_vacio(client):
    """Devuelve lista vacía cuando no hay países."""
    response = client.get("/paises")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_paises_con_datos(client, pais_espana, pais_alemania):
    """Devuelve la lista de países ordenados por nombre."""
    response = client.get("/paises")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_pais_tiene_campos_correctos(client, pais_espana):
    """Cada país tiene id_pais, nombre y codigo_iso."""
    response = client.get("/paises")
    pais = response.json()[0]
    assert "id_pais" in pais
    assert pais["nombre"] == "España"
    assert pais["codigo_iso"] == "ES"
