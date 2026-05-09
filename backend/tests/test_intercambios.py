"""Tests para los endpoints de intercambios."""

import pytest


class TestListarIntercambios:
    """Tests para GET /intercambios."""

    def test_intercambios_vacios(self, client):
        """Devuelve lista vacía si no hay intercambios."""
        response = client.get("/intercambios")
        assert response.status_code == 200
        assert response.json() == []


class TestCrearIntercambio:
    """Tests para POST /intercambios."""

    def test_crear_intercambio(self, client, moneda_quijote):
        """Crea un nuevo intercambio."""
        response = client.post("/intercambios", json={
            "nombre_usuario": "TestUser",
            "id_moneda_ofrecida": moneda_quijote.id_moneda,
            "contacto": "test@email.com",
            "descripcion": "Moneda en buen estado",
        })
        assert response.status_code == 201
        assert response.json()["nombre_usuario"] == "TestUser"
        assert response.json()["estado"] == "activo"

    def test_crear_intercambio_moneda_no_existe(self, client):
        """Devuelve 404 si la moneda ofrecida no existe."""
        response = client.post("/intercambios", json={
            "nombre_usuario": "TestUser",
            "id_moneda_ofrecida": 9999,
            "contacto": "test@email.com",
        })
        assert response.status_code == 404


class TestCerrarIntercambio:
    """Tests para PATCH /intercambios/{id}/cerrar."""

    def test_cerrar_intercambio(self, client, moneda_quijote):
        """Cierra un intercambio activo."""
        crear = client.post("/intercambios", json={
            "nombre_usuario": "TestUser",
            "id_moneda_ofrecida": moneda_quijote.id_moneda,
            "contacto": "test@email.com",
        })
        id_inter = crear.json()["id_intercambio"]
        response = client.patch(f"/intercambios/{id_inter}/cerrar")
        assert response.status_code == 200
        assert response.json()["estado"] == "cerrado"


class TestEliminarIntercambio:
    """Tests para DELETE /intercambios/{id}."""

    def test_eliminar_intercambio(self, client, moneda_quijote):
        """Elimina un intercambio."""
        crear = client.post("/intercambios", json={
            "nombre_usuario": "TestUser",
            "id_moneda_ofrecida": moneda_quijote.id_moneda,
            "contacto": "test@email.com",
        })
        id_inter = crear.json()["id_intercambio"]
        response = client.delete(f"/intercambios/{id_inter}")
        assert response.status_code == 204

    def test_eliminar_intercambio_no_existe(self, client):
        """Devuelve 404 si el intercambio no existe."""
        response = client.delete("/intercambios/9999")
        assert response.status_code == 404
