"""Tests para los endpoints /monedas."""


def test_listar_monedas_vacio(client):
    """Devuelve lista vacía cuando no hay monedas."""
    response = client.get("/monedas")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_monedas_con_datos(client, moneda_quijote):
    """Devuelve las monedas del catálogo."""
    response = client.get("/monedas")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filtrar_por_tipo_conmemorativa(client, moneda_quijote, moneda_comun_espana):
    """Filtra monedas conmemorativas correctamente."""
    response = client.get("/monedas?tipo=conmemorativa")
    assert len(response.json()) == 1
    assert response.json()[0]["tipo"] == "conmemorativa"


def test_filtrar_por_tipo_comun(client, moneda_quijote, moneda_comun_espana):
    """Filtra monedas comunes correctamente."""
    response = client.get("/monedas?tipo=comun")
    assert len(response.json()) == 1
    assert response.json()[0]["tipo"] == "comun"


def test_filtrar_por_anyo(client, moneda_quijote, moneda_comun_espana):
    """Filtra monedas por año correctamente."""
    response = client.get("/monedas?anyo=2005")
    assert len(response.json()) == 1
    assert response.json()[0]["anyo"] == 2005


def test_filtrar_por_pais(client, moneda_quijote, pais_espana):
    """Filtra monedas por país correctamente."""
    response = client.get(f"/monedas?pais={pais_espana.id_pais}")
    assert len(response.json()) == 1


def test_obtener_moneda_existente(client, moneda_quijote):
    """Devuelve una moneda por su ID."""
    response = client.get(f"/monedas/{moneda_quijote.id_moneda}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Don Quijote — IV Centenario"


def test_obtener_moneda_no_existente(client):
    """Devuelve 404 cuando la moneda no existe."""
    response = client.get("/monedas/9999")
    assert response.status_code == 404


def test_moneda_incluye_datos_pais(client, moneda_quijote):
    """La moneda incluye la información del país."""
    response = client.get(f"/monedas/{moneda_quijote.id_moneda}")
    assert response.json()["pais"]["nombre"] == "España"
