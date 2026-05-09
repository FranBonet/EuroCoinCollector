"""Tests para los endpoints de colección."""

import pytest


class TestListarColeccion:
    """Tests para GET /coleccion."""

    def test_coleccion_vacia(self, client):
        """Devuelve lista vacía si no hay monedas en la colección."""
        response = client.get("/coleccion")
        assert response.status_code == 200
        assert response.json() == []

    def test_coleccion_con_monedas(self, client, moneda_quijote):
        """Devuelve las monedas añadidas a la colección."""
        client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 2})
        response = client.get("/coleccion")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_coleccion_filtrada_por_pais(self, client, moneda_quijote, pais_espana):
        """Filtra la colección por país."""
        client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 1})
        response = client.get(f"/coleccion?pais={pais_espana.id_pais}")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestActualizarColeccion:
    """Tests para PUT /coleccion/{id_moneda}."""

    def test_añadir_moneda_nueva(self, client, moneda_quijote):
        """Crea una nueva entrada en la colección."""
        response = client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 1})
        assert response.status_code == 200
        assert response.json()["cantidad"] == 1

    def test_moneda_no_existe(self, client):
        """Devuelve 404 si la moneda no existe."""
        response = client.put("/coleccion/9999", json={"cantidad": 1})
        assert response.status_code == 404


class TestEliminarColeccion:
    """Tests para DELETE /coleccion/{id_moneda}."""

    def test_eliminar_moneda_coleccion(self, client, moneda_quijote):
        """Elimina una moneda de la colección."""
        client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 1})
        response = client.delete(f"/coleccion/{moneda_quijote.id_moneda}")
        assert response.status_code == 204
        assert client.get("/coleccion").json() == []

    def test_eliminar_moneda_no_en_coleccion(self, client, moneda_quijote):
        """Devuelve 404 si la moneda no está en la colección."""
        response = client.delete(f"/coleccion/{moneda_quijote.id_moneda}")
        assert response.status_code == 404


class TestFaltantes:
    """Tests para GET /coleccion/faltantes."""

    def test_todas_faltan(self, client, moneda_quijote):
        """Si no hay nada en la colección, todas faltan."""
        response = client.get("/coleccion/faltantes")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_ninguna_falta(self, client, moneda_quijote):
        """Si se tienen todas, no falta ninguna."""
        client.put(f"/coleccion/{moneda_quijote.id_moneda}", json={"cantidad": 1})
        response = client.get("/coleccion/faltantes")
        assert response.status_code == 200
        assert len(response.json()) == 0
