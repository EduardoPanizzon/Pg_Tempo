from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDateEdit, QLabel
from PySide6.QtCore import QDate
from db.database import get_connection
from datetime import date

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Carregamentos")

        central = QWidget()
        layout = QVBoxLayout()

        # Data
        self.data_edit = QDateEdit()
        self.data_edit.setDate(QDate.currentDate())
        self.data_edit.dateChanged.connect(self.carregar_tabela)
        layout.addWidget(QLabel("Carregamento -"))
        layout.addWidget(self.data_edit)

        # Tabela
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Botão salvar
        btn_salvar = QPushButton("Salvar preenchimentos do dia")
        btn_salvar.clicked.connect(self.salvar_dados)
        layout.addWidget(btn_salvar)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self.carregar_tabela()

    def carregar_tabela(self):
        conn = get_connection()
        perfis = conn.execute("SELECT id, motorista, placa, tipo_carro, ajudante FROM perfis").fetchall()

        self.table.setRowCount(len(perfis))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Motorista", "Placa", "Tipo", "Ajudante",
                                              "Destino", "Hora Chegada", "Adiantamento", "Manifesto"])

        data_str = self.data_edit.date().toString("yyyy-MM-dd")

        for i, p in enumerate(perfis):
            # Dados fixos
            self.table.setItem(i, 0, QTableWidgetItem(p[1]))
            self.table.setItem(i, 1, QTableWidgetItem(p[2]))
            self.table.setItem(i, 2, QTableWidgetItem(p[3]))
            self.table.setItem(i, 3, QTableWidgetItem(p[4]))

            # Dados preenchíveis (carregar se já existirem)
            registro = conn.execute(
                "SELECT destino, hora_chegada, adiantamento, manifesto FROM registros WHERE perfil_id=? AND data=?",
                (p[0], data_str)).fetchone()

            for j in range(4, 8):
                valor = registro[j-4] if registro else ""
                self.table.setItem(i, j, QTableWidgetItem(valor))

        conn.close()

    def salvar_dados(self):
        conn = get_connection()
        data_str = self.data_edit.date().toString("yyyy-MM-dd")

        for i in range(self.table.rowCount()):
            motorista = self.table.item(i, 0).text()
            perfil_id = conn.execute("SELECT id FROM perfis WHERE motorista=?", (motorista,)).fetchone()[0]

            destino = self.table.item(i, 4).text() if self.table.item(i, 4) else ""
            hora = self.table.item(i, 5).text() if self.table.item(i, 5) else ""
            adiantamento = self.table.item(i, 6).text() if self.table.item(i, 6) else ""
            manifesto = self.table.item(i, 7).text() if self.table.item(i, 7) else ""

            # Inserir ou atualizar
            existe = conn.execute("SELECT id FROM registros WHERE perfil_id=? AND data=?",
                                  (perfil_id, data_str)).fetchone()
            if existe:
                conn.execute("UPDATE registros SET destino=?, hora_chegada=?, adiantamento=?, manifesto=? WHERE id=?",
                             (destino, hora, adiantamento, manifesto, existe[0]))
            else:
                conn.execute("INSERT INTO registros (perfil_id, data, destino, hora_chegada, adiantamento, manifesto) VALUES (?, ?, ?, ?, ?, ?)",
                             (perfil_id, data_str, destino, hora, adiantamento, manifesto))
        conn.commit()
        conn.close()
