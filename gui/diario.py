from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
from db.database import get_connection
from datetime import date

class RegistroDiario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro Diário")
        layout = QVBoxLayout()

        self.perfil_select = QComboBox()
        layout.addWidget(QLabel("Perfil"))
        layout.addWidget(self.perfil_select)

        self.hora_input = QLineEdit()
        self.hora_input.setPlaceholderText("Hora de chegada (HH:MM)")
        layout.addWidget(self.hora_input)

        self.habitos_input = QLineEdit()
        self.habitos_input.setPlaceholderText("Hábitos")
        layout.addWidget(self.habitos_input)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar_registro)
        layout.addWidget(self.btn_salvar)

        self.setLayout(layout)
        self.carregar_perfis()

    def carregar_perfis(self):
        self.perfil_select.clear()
        conn = get_connection()
        for row in conn.execute("SELECT id, nome FROM perfis"):
            self.perfil_select.addItem(row[1], row[0])
        conn.close()

    def salvar_registro(self):
        perfil_id = self.perfil_select.currentData()
        hora = self.hora_input.text()
        habitos = self.habitos_input.text()

        conn = get_connection()
        conn.execute(
            "INSERT INTO registros (perfil_id, data, hora_chegada, habitos) VALUES (?, ?, ?, ?)",
            (perfil_id, date.today().isoformat(), hora, habitos)
        )
        conn.commit()
        conn.close()

        self.hora_input.clear()
        self.habitos_input.clear()
