CREATE TABLE IF NOT EXISTS equipo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ciudad VARCHAR(255),
    entrenador VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS jugador (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    posicion VARCHAR(255),
    numero INTEGER,
    CONSTRAINT fk_jugador_equipo
        FOREIGN KEY (equipo_id)
        REFERENCES equipo (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partido (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL,
    equipo_local_id INTEGER NOT NULL,
    equipo_visitante_id INTEGER NOT NULL,
    goles_local INTEGER,
    goles_visitante INTEGER,
    estado VARCHAR(255) NOT NULL,
    CONSTRAINT fk_partido_equipo_local
        FOREIGN KEY (equipo_local_id)
        REFERENCES equipo (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_partido_equipo_visitante
        FOREIGN KEY (equipo_visitante_id)
        REFERENCES equipo (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS integracion (
    id SERIAL PRIMARY KEY,
    contenido JSON NOT NULL
);
