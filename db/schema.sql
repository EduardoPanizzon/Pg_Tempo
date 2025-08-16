CREATE TABLE IF NOT EXISTS perfis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    detalhes TEXT
);

CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    perfil_id INTEGER NOT NULL,
    data DATE NOT NULL,
    hora_chegada TIME,
    habitos TEXT,
    FOREIGN KEY (perfil_id) REFERENCES perfis(id)
);
