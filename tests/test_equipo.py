def test_crear_y_listar_equipos(client):
    r = client.post("/equipos/", json={
        "nombre": "nacional",
        "ciudad": "medellin",
        "entrenador": "x"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["id"] >= 1
    assert data["nombre"] == "nacional"

    r2 = client.get("/equipos/")
    assert r2.status_code == 200
    lista = r2.json()
    assert len(lista) == 1