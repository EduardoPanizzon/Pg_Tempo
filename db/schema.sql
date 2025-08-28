CREATE TABLE IF NOT EXISTS perfis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    motorista TEXT NOT NULL,
    placa TEXT NOT NULL,
    tipo_carro TEXT,
    ajudante TEXT
);

CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    perfil_id INTEGER NOT NULL,
    data DATE NOT NULL,
    destino TEXT,
    hora_chegada TEXT,
    adiantamento TEXT,
    manifesto TEXT,
    FOREIGN KEY (perfil_id) REFERENCES perfis(id)
);
