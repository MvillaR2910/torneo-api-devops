INSERT INTO equipo (nombre, ciudad, entrenador)
VALUES
    ('Atletico Nacional', 'Medellin', 'Javier Gandolfi'),
    ('Millonarios', 'Bogota', 'David Gonzalez')
ON CONFLICT DO NOTHING;

INSERT INTO jugador (equipo_id, nombre, posicion, numero)
VALUES
    (1, 'Alfredo Morelos', 'Delantero', 9),
    (2, 'Daniel Ruiz', 'Volante', 18)
ON CONFLICT DO NOTHING;

INSERT INTO partido (fecha, equipo_local_id, equipo_visitante_id, goles_local, goles_visitante, estado)
VALUES
    ('2026-04-28 20:00:00', 1, 2, 2, 1, 'finalizado')
ON CONFLICT DO NOTHING;

INSERT INTO integracion (contenido)
VALUES
    (
        '{
            "meta": {
                "antes": "helpdesk-api",
                "origen": "helpdesk-api",
                "siguiente": null
            },
            "trace_id": "trace-demo-sql-001",
            "payload": {
                "soporte": {
                    "ticket": {
                        "id": 101,
                        "asunto": "incidente"
                    }
                },
                "futbol": {
                    "equipo": {
                        "id": 1,
                        "nombre": "Atletico Nacional"
                    }
                }
            }
        }'
    )
ON CONFLICT DO NOTHING;

SELECT * FROM equipo;
SELECT * FROM jugador;
SELECT * FROM partido;
SELECT * FROM integracion;
