from PySide6.QtWidgets import QApplication
import sys
from db.database import init_db
from gui.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
