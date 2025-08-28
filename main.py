from PySide6.QtWidgets import QApplication
import sys
from db.database import init_db
from gui.main_window import MainWindow
from gui.cadastro import CadastroPerfis

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    cadastro = CadastroPerfis()
    cadastro.show()

    sys.exit(app.exec())
