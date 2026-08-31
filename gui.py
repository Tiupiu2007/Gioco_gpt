import sys
from dotenv import load_dotenv
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QLineEdit, QPushButton, QLabel, QProgressBar, QMessageBox
from game import GameEngine, GameState, OllamaNarrator
from game.save import load_game, save_game

class TurnWorker(QThread):
    finished_turn = pyqtSignal(str)
    failed = pyqtSignal(str)
    def __init__(self, engine, action):
        super().__init__()
        self.engine, self.action = engine, action
    def run(self):
        try:
            self.finished_turn.emit(self.engine.act(self.action))
        except Exception as exc:
            self.failed.emit(str(exc))

class IsekaiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.state = load_game() or GameState()
        self.narrator = OllamaNarrator()
        self.engine = GameEngine(self.state, self.narrator)
        self.setWindowTitle("Gioco GPT — Isekai")
        self.resize(1100, 720)
        self._build_ui()
        self._show(self.engine.start())
        self._refresh_status()

    def _build_ui(self):
        root = QWidget(); self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        header = QHBoxLayout()
        self.status = QLabel(); header.addWidget(self.status); header.addStretch()
        save = QPushButton("Salva"); save.clicked.connect(lambda: save_game(self.state)); header.addWidget(save)
        layout.addLayout(header)
        self.story = QTextBrowser(); self.story.setOpenExternalLinks(False); layout.addWidget(self.story, 1)
        controls = QHBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText("Scrivi liberamente cosa fa il protagonista...")
        self.input.returnPressed.connect(self.send)
        self.send_button = QPushButton("Agisci"); self.send_button.clicked.connect(self.send)
        controls.addWidget(self.input, 1); controls.addWidget(self.send_button)
        layout.addLayout(controls)
        self.setStyleSheet('''QMainWindow { background:#101218; } QLabel { color:#ddd; font-size:15px; } QTextBrowser { background:#171922; color:#eee; border:1px solid #303340; padding:18px; font-size:16px; } QLineEdit { background:#171922; color:#fff; border:1px solid #444957; padding:12px; font-size:15px; } QPushButton { padding:10px 18px; }''')

    def _show(self, text):
        self.story.append(text.replace("\n", "<br>"))
        self.story.verticalScrollBar().setValue(self.story.verticalScrollBar().maximum())

    def _refresh_status(self):
        p, w = self.state.player, self.state.world
        self.status.setText(f"Giorno {w.day} · {w.hour:02d}:00 · {w.location}   |   {p.name}   |   HP {p.hp}/{p.max_hp}   |   Lv {p.level}")

    def send(self):
        action = self.input.text().strip()
        if not action: return
        self.input.clear(); self._show(f"<b>Tu:</b> {action}")
        self.input.setEnabled(False); self.send_button.setEnabled(False)
        self.worker = TurnWorker(self.engine, action)
        self.worker.finished_turn.connect(self._turn_done)
        self.worker.failed.connect(self._turn_failed)
        self.worker.start()

    def _turn_done(self, text):
        self._show(text); self._refresh_status(); self.input.setEnabled(True); self.send_button.setEnabled(True); self.input.setFocus()

    def _turn_failed(self, error):
        QMessageBox.warning(self, "Errore narratore", error)
        self.input.setEnabled(True); self.send_button.setEnabled(True); self.input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IsekaiWindow(); window.show()
    sys.exit(app.exec())
