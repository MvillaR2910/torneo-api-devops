def crear_equipo(client):
    return client.post("/api/v2/equipos/", json={
        "nombre": "nacional",
        "ciudad": "medellin",
        "entrenador": "x"
    })


def test_crear_equipo(client):
    r = crear_equipo(client)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] >= 1
    assert data["nombre"] == "nacional"


def test_listar_equipos(client):
    crear_equipo(client)
    r = client.get("/api/v2/equipos/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_equipo_por_id(client):
    r = crear_equipo(client)
    equipo_id = r.json()["id"]

    r2 = client.get(f"/api/v2/equipos/{equipo_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == equipo_id


def test_actualizar_equipo(client):
    r = crear_equipo(client)
    equipo_id = r.json()["id"]

    r2 = client.put(f"/api/v2/equipos/{equipo_id}", json={
        "nombre": "cali",
        "ciudad": "cali",
        "entrenador": "y"
    })

    assert r2.status_code == 200
    assert r2.json()["nombre"] == "cali"


def test_eliminar_equipo(client):
    r = crear_equipo(client)
    equipo_id = r.json()["id"]

    r2 = client.delete(f"/api/v2/equipos/{equipo_id}")
    assert r2.status_code == 200

    r3 = client.get(f"/api/v2/equipos/{equipo_id}")
    assert r3.status_code == 404


def test_equipo_no_encontrado(client):
    r = client.get("/api/v2/equipos/999")
    assert r.status_code == 404