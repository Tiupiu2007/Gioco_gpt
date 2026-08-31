import sys
from gui import IsekaiWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IsekaiWindow()
    window.show()
    sys.exit(app.exec())
