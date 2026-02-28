def crear_equipo(client):
    r = client.post("/equipos/", json={
        "nombre": "nacional",
        "ciudad": "medellin",
        "entrenador": "x"
    })
    return r.json()["id"]


def crear_jugador(client, equipo_id: int):
    return client.post("/jugadores/", json={
        "equipo_id": equipo_id,
        "nombre": "juan perez",
        "posicion": "delantero",
        "numero": 9
    })


def test_crear_jugador(client):
    equipo_id = crear_equipo(client)
    r = crear_jugador(client, equipo_id)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] >= 1
    assert data["equipo_id"] == equipo_id


def test_listar_jugadores(client):
    equipo_id = crear_equipo(client)
    crear_jugador(client, equipo_id)

    r = client.get("/jugadores/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_jugador_por_id(client):
    equipo_id = crear_equipo(client)
    r = crear_jugador(client, equipo_id)
    jugador_id = r.json()["id"]

    r2 = client.get(f"/jugadores/{jugador_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == jugador_id


def test_actualizar_jugador(client):
    equipo_id = crear_equipo(client)
    r = crear_jugador(client, equipo_id)
    jugador_id = r.json()["id"]

    r2 = client.put(f"/jugadores/{jugador_id}", json={
        "equipo_id": equipo_id,
        "nombre": "carlos",
        "posicion": "defensa",
        "numero": 3
    })
    assert r2.status_code == 200
    assert r2.json()["nombre"] == "carlos"
    assert r2.json()["numero"] == 3


def test_eliminar_jugador(client):
    equipo_id = crear_equipo(client)
    r = crear_jugador(client, equipo_id)
    jugador_id = r.json()["id"]

    r2 = client.delete(f"/jugadores/{jugador_id}")
    assert r2.status_code == 200

    r3 = client.get(f"/jugadores/{jugador_id}")
    assert r3.status_code == 404


def test_jugador_no_encontrado(client):
    r = client.get("/jugadores/999")
    assert r.status_code == 404