def crear_equipo(client, nombre: str):
    r = client.post("/equipos/", json={
        "nombre": nombre,
        "ciudad": "x",
        "entrenador": "y"
    })
    return r.json()["id"]


def crear_partido(client, local_id: int, visitante_id: int, payload_extra=None):
    payload = {
        "fecha": "2026-02-28T12:00:00",
        "equipo_local_id": local_id,
        "equipo_visitante_id": visitante_id,
        "goles_local": None,
        "goles_visitante": None,
        "estado": "programado"
    }
    if payload_extra:
        payload.update(payload_extra)
    return client.post("/partidos/", json=payload)


def test_crear_partido(client):
    local_id = crear_equipo(client, "equipo a")
    visitante_id = crear_equipo(client, "equipo b")

    r = crear_partido(client, local_id, visitante_id)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] >= 1
    assert data["equipo_local_id"] == local_id
    assert data["equipo_visitante_id"] == visitante_id
    assert data["goles_local"] is None
    assert data["estado"] == "programado"


def test_listar_partidos(client):
    local_id = crear_equipo(client, "equipo a")
    visitante_id = crear_equipo(client, "equipo b")
    crear_partido(client, local_id, visitante_id)

    r = client.get("/partidos/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_partido_por_id(client):
    local_id = crear_equipo(client, "equipo a")
    visitante_id = crear_equipo(client, "equipo b")

    r = crear_partido(client, local_id, visitante_id)
    partido_id = r.json()["id"]

    r2 = client.get(f"/partidos/{partido_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == partido_id


def test_actualizar_partido(client):
    local_id = crear_equipo(client, "equipo a")
    visitante_id = crear_equipo(client, "equipo b")

    r = crear_partido(client, local_id, visitante_id)
    partido_id = r.json()["id"]

    r2 = client.put(f"/partidos/{partido_id}", json={
        "fecha": "2026-03-01T18:30:00",
        "equipo_local_id": local_id,
        "equipo_visitante_id": visitante_id,
        "goles_local": 2,
        "goles_visitante": 1,
        "estado": "jugado"
    })
    assert r2.status_code == 200
    assert r2.json()["estado"] == "jugado"
    assert r2.json()["goles_local"] == 2
    assert r2.json()["goles_visitante"] == 1


def test_eliminar_partido(client):
    local_id = crear_equipo(client, "equipo a")
    visitante_id = crear_equipo(client, "equipo b")

    r = crear_partido(client, local_id, visitante_id)
    partido_id = r.json()["id"]

    r2 = client.delete(f"/partidos/{partido_id}")
    assert r2.status_code == 200

    r3 = client.get(f"/partidos/{partido_id}")
    assert r3.status_code == 404


def test_partido_no_encontrado(client):
    r = client.get("/partidos/999")
    assert r.status_code == 404


def test_no_permitir_mismo_equipo_local_y_visitante(client):
    equipo_id = crear_equipo(client, "equipo unico")

    r = crear_partido(client, equipo_id, equipo_id)
    assert r.status_code == 400