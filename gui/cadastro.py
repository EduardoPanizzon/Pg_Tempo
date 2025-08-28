from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QHBoxLayout
from db.database import get_connection

class CadastroPerfis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Perfis")
        layout = QVBoxLayout()

        # Campos
        self.motorista_input = QLineEdit(); self.motorista_input.setPlaceholderText("Nome do motorista")
        self.placa_input = QLineEdit(); self.placa_input.setPlaceholderText("Placa")
        self.tipo_input = QLineEdit(); self.tipo_input.setPlaceholderText("Tipo de carro")
        self.ajudante_input = QLineEdit(); self.ajudante_input.setPlaceholderText("Nome do ajudante")

        layout.addWidget(self.motorista_input)
        layout.addWidget(self.placa_input)
        layout.addWidget(self.tipo_input)
        layout.addWidget(self.ajudante_input)

        self.btn_salvar = QPushButton("Salvar / Atualizar")
        self.btn_salvar.clicked.connect(self.salvar_perfil)
        layout.addWidget(self.btn_salvar)

        self.lista = QListWidget()
        self.lista.itemClicked.connect(self.carregar_perfil)
        layout.addWidget(self.lista)

        # Botão excluir
        self.btn_excluir = QPushButton("Excluir selecionado")
        self.btn_excluir.clicked.connect(self.excluir_perfil)
        layout.addWidget(self.btn_excluir)

        self.setLayout(layout)
        self.perfil_id = None
        self.carregar_lista()

    def carregar_lista(self):
        self.lista.clear()
        conn = get_connection()
        for row in conn.execute("SELECT id, motorista, placa, tipo_carro, ajudante FROM perfis"):
            self.lista.addItem(f"{row[0]} - {row[1]} | {row[2]} | {row[3]} | {row[4]}")
        conn.close()

    def salvar_perfil(self):
        motorista = self.motorista_input.text()
        placa = self.placa_input.text()
        tipo = self.tipo_input.text()
        ajudante = self.ajudante_input.text()

        conn = get_connection()
        if self.perfil_id:  # Atualizar
            conn.execute("UPDATE perfis SET motorista=?, placa=?, tipo_carro=?, ajudante=? WHERE id=?",
                         (motorista, placa, tipo, ajudante, self.perfil_id))
        else:  # Inserir
            conn.execute("INSERT INTO perfis (motorista, placa, tipo_carro, ajudante) VALUES (?, ?, ?, ?)",
                         (motorista, placa, tipo, ajudante))
        conn.commit()
        conn.close()
        self.carregar_lista()
        self.limpar_form()

    def carregar_perfil(self, item):
        parts = item.text().split(" - ")
        self.perfil_id = int(parts[0])
        conn = get_connection()
        row = conn.execute("SELECT motorista, placa, tipo_carro, ajudante FROM perfis WHERE id=?",
                           (self.perfil_id,)).fetchone()
        conn.close()
        self.motorista_input.setText(row[0])
        self.placa_input.setText(row[1])
        self.tipo_input.setText(row[2])
        self.ajudante_input.setText(row[3])

    def excluir_perfil(self):
        if not self.perfil_id:
            return
        conn = get_connection()
        conn.execute("DELETE FROM perfis WHERE id=?", (self.perfil_id,))
        conn.commit()
        conn.close()
        self.carregar_lista()
        self.limpar_form()

    def limpar_form(self):
        self.perfil_id = None
        self.motorista_input.clear()
        self.placa_input.clear()
        self.tipo_input.clear()
        self.ajudante_input.clear()
