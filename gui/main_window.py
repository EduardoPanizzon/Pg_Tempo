from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from gui.cadastro import CadastroPerfis
from gui.diario import RegistroDiario
import pandas as pd
from db.database import get_connection
from datetime import date

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Registros")
        central = QWidget()
        layout = QVBoxLayout()

        btn_cadastro = QPushButton("Cadastro de Perfis")
        btn_cadastro.clicked.connect(self.abrir_cadastro)
        layout.addWidget(btn_cadastro)

        btn_diario = QPushButton("Registro Diário")
        btn_diario.clicked.connect(self.abrir_diario)
        layout.addWidget(btn_diario)

        btn_exportar = QPushButton("Exportar CSV (Hoje)")
        btn_exportar.clicked.connect(self.exportar_csv)
        layout.addWidget(btn_exportar)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def abrir_cadastro(self):
        self.cadastro_window = CadastroPerfis()
        self.cadastro_window.show()

    def abrir_diario(self):
        self.diario_window = RegistroDiario()
        self.diario_window.show()

    def exportar_csv(self):
        conn = get_connection()
        df = pd.read_sql_query(
            "SELECT r.data, p.nome, r.hora_chegada, r.habitos "
            "FROM registros r JOIN perfis p ON r.perfil_id = p.id "
            "WHERE r.data = ?",
            conn,
            params=(date.today().isoformat(),)
        )
        df.to_csv(f"registros_{date.today()}.csv", index=False)
        conn.close()
