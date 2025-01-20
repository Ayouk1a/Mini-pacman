import sys
from PyQt6.QtWidgets import QApplication
from view import ParametresPacman

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ParametresPacman()
    fenetre.setWindowTitle("Mini-Pacman")
    fenetre.resize(600, 600)
    fenetre.show()
    sys.exit(app.exec())
