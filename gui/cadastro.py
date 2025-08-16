from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget
from db.database import get_connection

class CadastroPerfis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Perfis")
        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        layout.addWidget(self.nome_input)

        self.idade_input = QLineEdit()
        self.idade_input.setPlaceholderText("Idade")
        layout.addWidget(self.idade_input)

        self.detalhes_input = QLineEdit()
        self.detalhes_input.setPlaceholderText("Detalhes")
        layout.addWidget(self.detalhes_input)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar_perfil)
        layout.addWidget(self.btn_salvar)

        self.lista = QListWidget()
        layout.addWidget(self.lista)

        self.setLayout(layout)
        self.carregar_perfis()

    def salvar_perfil(self):
        nome = self.nome_input.text()
        idade = self.idade_input.text()
        detalhes = self.detalhes_input.text()

        if nome.strip():
            conn = get_connection()
            conn.execute("INSERT INTO perfis (nome, idade, detalhes) VALUES (?, ?, ?)",
                         (nome, idade, detalhes))
            conn.commit()
            conn.close()
            self.carregar_perfis()
            self.nome_input.clear()
            self.idade_input.clear()
            self.detalhes_input.clear()

    def carregar_perfis(self):
        self.lista.clear()
        conn = get_connection()
        for row in conn.execute("SELECT id, nome, idade FROM perfis"):
            self.lista.addItem(f"{row[0]} - {row[1]} ({row[2]})")
        conn.close()
