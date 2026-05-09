"""Tests para los endpoints /lista_deseos."""


def test_listar_deseos_vacio(client):
    """Devuelve lista vacía cuando no hay deseos."""
    response = client.get("/lista_deseos")
    assert response.status_code == 200
    assert response.json() == []


def test_agregar_deseo(client, moneda_quijote):
    """Añade una moneda a la lista de deseos."""
    response = client.post(
        f"/lista_deseos/{moneda_quijote.id_moneda}",
        json={"prioridad": "alta", "notas": "La necesito"},
    )
    assert response.status_code == 201
    assert response.json()["prioridad"] == "alta"


def test_agregar_deseo_duplicado(client, moneda_quijote):
    """Devuelve 409 al intentar duplicar un deseo."""
    client.post(f"/lista_deseos/{moneda_quijote.id_moneda}", json={"prioridad": "media"})
    response = client.post(f"/lista_deseos/{moneda_quijote.id_moneda}", json={"prioridad": "alta"})
    assert response.status_code == 409


def test_eliminar_deseo(client, moneda_quijote):
    """Elimina una moneda de la lista de deseos."""
    client.post(f"/lista_deseos/{moneda_quijote.id_moneda}", json={"prioridad": "media"})
    response = client.delete(f"/lista_deseos/{moneda_quijote.id_moneda}")
    assert response.status_code == 204


def test_eliminar_deseo_no_existente(client):
    """Devuelve 404 al intentar eliminar un deseo inexistente."""
    response = client.delete("/lista_deseos/9999")
    assert response.status_code == 404


def test_deseo_moneda_no_existente(client):
    """Devuelve 404 al añadir deseo de moneda inexistente."""
    response = client.post("/lista_deseos/9999", json={"prioridad": "media"})
    assert response.status_code == 404


def test_listar_deseos_con_datos(client, moneda_quijote, moneda_comun_espana):
    """Muestra todos los deseos después de añadirlos."""
    client.post(f"/lista_deseos/{moneda_quijote.id_moneda}", json={"prioridad": "alta"})
    client.post(f"/lista_deseos/{moneda_comun_espana.id_moneda}", json={"prioridad": "baja"})
    response = client.get("/lista_deseos")
    assert len(response.json()) == 2
