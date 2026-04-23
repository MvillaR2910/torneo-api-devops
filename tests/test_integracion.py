from unittest.mock import patch


def recibir_integracion(client, trace_id="trace-demo-001"):
    return client.post("/api/v2/integracion/recibir", json={
        "meta": {
            "antes": "helpdesk-api",
            "origen": "helpdesk-api",
            "siguiente": None
        },
        "trace_id": trace_id,
        "payload": {
            "soporte": {
                "solicitante": {
                    "id": 1,
                    "nombre": "Sebastian Ruiz"
                },
                "ticket": {
                    "id": 101,
                    "asunto": "incidente"
                }
            }
        }
    })


def body_completar(**kwargs):
    body = {
        "equipo": {
            "id": 1,
            "nombre": "Nacional",
            "ciudad": "Medellin",
            "entrenador": "Autuori"
        },
        "jugador": {
            "id": 1,
            "equipo_id": 1,
            "nombre": "Juan Perez",
            "posicion": "Delantero",
            "numero": 9
        },
        "partido": {
            "id": 1,
            "equipo_local_id": 1,
            "equipo_visitante_id": 2,
            "goles_local": 2,
            "goles_visitante": 1,
            "estado": "finalizado"
        }
    }
    body.update(kwargs)
    return body


def test_recibir_integracion_externa(client):
    r = recibir_integracion(client)
    assert r.status_code == 200

    data = r.json()
    assert data["id"] >= 1
    assert data["contenido"]["trace_id"] == "trace-demo-001"
    assert "soporte" in data["contenido"]["payload"]


def test_completar_integracion_por_id(client):
    r = recibir_integracion(client)
    integracion_id = r.json()["id"]

    r2 = client.post("/api/v2/integracion/completar", json=body_completar(integracion_id=integracion_id))
    assert r2.status_code == 200

    data = r2.json()
    assert data["id"] == integracion_id
    assert data["contenido"]["payload"]["soporte"]["ticket"]["id"] == 101
    assert data["contenido"]["payload"]["futbol"]["equipo"]["nombre"] == "Nacional"
    assert data["contenido"]["payload"]["futbol"]["jugador"]["numero"] == 9
    assert data["contenido"]["payload"]["futbol"]["partido"]["estado"] == "finalizado"


def test_completar_integracion_por_trace_id(client):
    recibir_integracion(client, trace_id="trace-demo-xyz")

    r = client.post("/api/v2/integracion/completar", json=body_completar(trace_id="trace-demo-xyz"))
    assert r.status_code == 200
    assert r.json()["contenido"]["trace_id"] == "trace-demo-xyz"
    assert r.json()["contenido"]["payload"]["futbol"]["equipo"]["id"] == 1


def test_completar_integracion_usa_la_ultima_si_no_mandan_filtro(client):
    recibir_integracion(client, trace_id="trace-1")
    r2 = recibir_integracion(client, trace_id="trace-2")
    ultima_id = r2.json()["id"]

    r3 = client.post("/api/v2/integracion/completar", json=body_completar())
    assert r3.status_code == 200
    assert r3.json()["id"] == ultima_id
    assert r3.json()["contenido"]["trace_id"] == "trace-2"


def test_completar_integracion_no_encontrada(client):
    r = client.post("/api/v2/integracion/completar", json=body_completar(trace_id="no-existe"))
    assert r.status_code == 404


def test_actualizar_integracion_en_destino(client):
    recibir_integracion(client, trace_id="trace-patch-001")
    client.post("/api/v2/integracion/completar", json=body_completar(trace_id="trace-patch-001"))

    class FakeResponse:
        status_code = 200

        @staticmethod
        def json():
            return {"ok": True}

    with patch("app.routers.integracion.requests.patch", return_value=FakeResponse()) as mock_patch:
        r = client.patch("/api/v2/integracion/actualizar-destino", json={
            "trace_id": "trace-patch-001",
            "url_destino": "http://otro-servicio/api/v2/integracion/123",
            "headers": {
                "Content-Type": "application/json"
            }
        })

    assert r.status_code == 200
    data = r.json()
    assert data["status_code_destino"] == 200
    assert data["body_enviado"]["trace_id"] == "trace-patch-001"
    assert data["body_enviado"]["payload"]["futbol"]["equipo"]["nombre"] == "Nacional"
    mock_patch.assert_called_once()
