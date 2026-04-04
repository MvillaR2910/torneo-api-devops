def crear_integracion(client):
    return client.post("/api/v2/integracion/", json={
        "contenido": {
            "metadata": {
                "source": "google-cloud-soporte",
                "version": "v2"
            },
            "payload": {
                "ticket": {
                    "id": 1,
                    "asunto": "incidente"
                },
                "solicitante": {
                    "id": 2,
                    "nombre": "juan"
                },
                "comentario": {
                    "id": 3,
                    "mensaje": "requiere revision"
                }
            }
        }
    })


def test_crear_integracion(client):
    r = crear_integracion(client)
    assert r.status_code == 200

    data = r.json()
    assert data["id"] >= 1
    assert "equipo" in data["contenido"]["payload"]
    assert "jugador" in data["contenido"]["payload"]
    assert "partido" in data["contenido"]["payload"]


def test_listar_integraciones(client):
    crear_integracion(client)

    r = client.get("/api/v2/integracion/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_integracion_por_id(client):
    r = crear_integracion(client)
    integracion_id = r.json()["id"]

    r2 = client.get(f"/api/v2/integracion/{integracion_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == integracion_id


def test_actualizar_integracion_con_put(client):
    r = crear_integracion(client)
    integracion_id = r.json()["id"]

    r2 = client.put(f"/api/v2/integracion/{integracion_id}", json={
        "contenido": {
            "metadata": {
                "source": "put-update",
                "version": "v2"
            },
            "payload": {
                "ticket": {
                    "id": 99,
                    "asunto": "actualizado"
                }
            }
        }
    })

    assert r2.status_code == 200
    assert r2.json()["contenido"]["metadata"]["source"] == "put-update"
    assert r2.json()["contenido"]["payload"]["ticket"]["id"] == 99


def test_actualizar_integracion_con_patch(client):
    r = crear_integracion(client)
    integracion_id = r.json()["id"]

    r2 = client.patch(f"/api/v2/integracion/{integracion_id}", json={
        "contenido": {
            "metadata": {
                "source": "patch-update"
            }
        }
    })

    assert r2.status_code == 200
    assert r2.json()["contenido"]["metadata"]["source"] == "patch-update"


def test_integracion_no_encontrada(client):
    r = client.get("/api/v2/integracion/999")
    assert r.status_code == 404