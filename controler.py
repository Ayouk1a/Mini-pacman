import random
from PyQt6.QtCore import QTimer

123

class Entite:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ControleurPacman:
    def __init__(self, largeur, hauteur, nb_fantomes):
        self.largeur = largeur
        self.hauteur = hauteur
        self.nb_fantomes = nb_fantomes
        self.fantomes = []
        self.pacman = None
        self.minuteur = QTimer()
        self.scene = None

        self.minuteur.timeout.connect(self.etape_suivante)

    def demarrer(self):
        self.fantomes = [Entite(random.randint(0, self.largeur - 1), random.randint(0, self.hauteur - 1)) 
                         for _ in range(self.nb_fantomes)]
        self.pacman = Entite(random.randint(0, self.largeur - 1), random.randint(0, self.hauteur - 1))

        self.minuteur.start(500)
        print("Jeu démarré avec:")
        print(f"Pacman en ({self.pacman.x}, {self.pacman.y})")
        for i, fantome in enumerate(self.fantomes):
            print(f"Fantôme {i+1} en ({fantome.x}, {fantome.y})")

    def arreter(self):
        self.minuteur.stop()
        print("Jeu arrêté")
        if self.scene:
            self.scene.afficher_message_gagne()

    def deplacer_pacman(self, dx, dy):
        nouveau_x = (self.pacman.x + dx) % self.largeur
        nouveau_y = (self.pacman.y + dy) % self.hauteur
        self.pacman.x, self.pacman.y = nouveau_x, nouveau_y

        # Vérifier si Pacman mange un fantôme
        self.fantomes = [fantome for fantome in self.fantomes if not (fantome.x == self.pacman.x and fantome.y == self.pacman.y)]

        # Vérifier la victoire
        if not self.fantomes:
            print("Tous les fantômes ont été mangés ! Arrêt du jeu.")
            self.arreter()
            return

        if self.scene:
            self.scene.rafraichir(self.fantomes, self.pacman)

    def etape_suivante(self):
        # Déplacement aléatoire des fantômes
        for fantome in self.fantomes:
            fantome.x = (fantome.x + random.choice([-1, 0, 1])) % self.largeur
            fantome.y = (fantome.y + random.choice([-1, 0, 1])) % self.hauteur

        # Actualiser la scène
        if self.scene:
            self.scene.rafraichir(self.fantomes, self.pacman)

        print("Étape suivante terminée. Pacman:", (self.pacman.x, self.pacman.y))
        for i, fantome in enumerate(self.fantomes):
            print(f"Fantôme {i+1} en ({fantome.x}, {fantome.y})")
