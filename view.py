from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QSpinBox, QPushButton, QGraphicsView, QGraphicsScene, QLabel
)
from PyQt6.QtGui import QBrush, QPen, QColor, QKeyEvent, QFont
from PyQt6.QtCore import Qt, QTimer
from controler import ControleurPacman

class ScenePacman(QGraphicsScene):
    def __init__(self, largeur, hauteur, taille_case, parent=None):
        super().__init__(parent)
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.setSceneRect(0, 0, largeur * taille_case, hauteur * taille_case)
        self.afficher_victoire = False

    def rafraichir(self, fantomes, pacman):
        self.clear()
        self.addRect(0, 0, self.largeur * self.taille_case, self.hauteur * self.taille_case, 
                     QPen(QColor("#666666")), QBrush(QColor("#888888")))

        for x in range(self.largeur):
            for y in range(self.hauteur):
                self.addRect(
                    x * self.taille_case,
                    y * self.taille_case,
                    self.taille_case,
                    self.taille_case,
                    QPen(QColor("#AAAAAA"))
                )

        for fantome in fantomes:
            self.addEllipse(
                fantome.x * self.taille_case,
                fantome.y * self.taille_case,
                self.taille_case,
                self.taille_case,
                QPen(QColor("#770000")),
                QBrush(QColor("#FF5555"))
            )

        if pacman:
            self.addEllipse(
                pacman.x * self.taille_case,
                pacman.y * self.taille_case,
                self.taille_case,
                self.taille_case,
                QPen(QColor("#555500")),
                QBrush(QColor("#FFFF55"))
            )

        if self.afficher_victoire:
            texte = self.addText("GAGNÉ !", QFont("Arial", 30, QFont.Weight.Bold))
            texte.setDefaultTextColor(QColor("#FFFF55"))
            texte.setPos(
                (self.largeur * self.taille_case) / 2 - texte.boundingRect().width() / 2,
                (self.hauteur * self.taille_case) / 2 - texte.boundingRect().height() / 2
            )

    def afficher_message_gagne(self):
        self.afficher_victoire = True
        self.rafraichir([], None)

class ParametresPacman(QWidget):
    def __init__(self):
        super().__init__()

        self.controleur = None
        self.scene = None
        self.taille_case = 25  # Taille par défaut d'une case (modifiable)
        self.temps_ecoule = 0  # Temps écoulé en secondes
        self.minuteur = QTimer()  # Timer pour incrémenter le temps

        # Définir une couleur de fond grise pour la fenêtre
        self.setStyleSheet("background-color: #CCCCCC; color: black;")

        disposition_principale = QVBoxLayout(self)

        self.largeur_grille_spinbox = QSpinBox()
        self.largeur_grille_spinbox.setRange(5, 50)
        self.largeur_grille_spinbox.setValue(20)

        self.hauteur_grille_spinbox = QSpinBox()
        self.hauteur_grille_spinbox.setRange(5, 50)
        self.hauteur_grille_spinbox.setValue(20)

        self.nb_fantomes_spinbox = QSpinBox()
        self.nb_fantomes_spinbox.setRange(1, 20)
        self.nb_fantomes_spinbox.setValue(3)

        disposition_formulaire = QFormLayout()
        disposition_formulaire.addRow("Largeur de la grille:", self.largeur_grille_spinbox)
        disposition_formulaire.addRow("Hauteur de la grille:", self.hauteur_grille_spinbox)
        disposition_formulaire.addRow("Nombre de fantômes:", self.nb_fantomes_spinbox)

        disposition_principale.addLayout(disposition_formulaire)

        # Ajouter un label pour afficher le temps écoulé
        self.label_timer = QLabel("Temps écoulé : 0s")
        self.label_timer.setFont(QFont("Arial", 14))
        disposition_principale.addWidget(self.label_timer)

        self.bouton_demarrer = QPushButton("DÉMARRER")
        self.bouton_demarrer.clicked.connect(self.demarrer_jeu)

        self.bouton_arreter = QPushButton("ARRÊTER")
        self.bouton_arreter.setEnabled(False)
        self.bouton_arreter.clicked.connect(self.arreter_jeu)

        disposition_boutons = QHBoxLayout()
        disposition_boutons.addWidget(self.bouton_demarrer)
        disposition_boutons.addWidget(self.bouton_arreter)

        disposition_principale.addLayout(disposition_boutons)

        self.vue_graphique = QGraphicsView()
        disposition_principale.addWidget(self.vue_graphique)

        self.setLayout(disposition_principale)

        # Connecter le timer à une méthode pour mettre à jour le temps
        self.minuteur.timeout.connect(self.incrementer_temps)

    def demarrer_jeu(self):
        largeur = self.largeur_grille_spinbox.value()
        hauteur = self.hauteur_grille_spinbox.value()
        nb_fantomes = self.nb_fantomes_spinbox.value()

        self.controleur = ControleurPacman(largeur, hauteur, nb_fantomes)

        # Taille dynamique de la scène en fonction de la grille
        self.scene = ScenePacman(largeur, hauteur, self.taille_case)
        self.vue_graphique.setScene(self.scene)
        self.controleur.scene = self.scene

        # Adapter la taille de la vue graphique pour inclure la scène
        self.vue_graphique.setFixedSize(largeur * self.taille_case + 2, hauteur * self.taille_case + 2)

        # Adapter la taille de la fenêtre principale
        self.setFixedSize(self.vue_graphique.width() + 50, self.vue_graphique.height() + 200)

        self.controleur.demarrer()

        # Réinitialiser le temps et démarrer le minuteur
        self.temps_ecoule = 0
        self.label_timer.setText("Temps écoulé : 0s")
        self.minuteur.start(1000)  # Mettre à jour chaque seconde

        self.bouton_demarrer.setEnabled(False)
        self.bouton_arreter.setEnabled(True)

    def arreter_jeu(self):
        if self.controleur:
            self.controleur.arreter()
        if self.scene:
            self.scene.clear()

        # Arrêter le minuteur
        self.minuteur.stop()

        self.bouton_demarrer.setEnabled(True)
        self.bouton_arreter.setEnabled(False)

    def incrementer_temps(self):
        self.temps_ecoule += 1
        self.label_timer.setText(f"Temps écoulé : {self.temps_ecoule}s")

    def keyPressEvent(self, evenement: QKeyEvent):
        if self.controleur:
            if evenement.key() == Qt.Key.Key_Z:  
                self.controleur.deplacer_pacman(0, -1)
            elif evenement.key() == Qt.Key.Key_S:  
                self.controleur.deplacer_pacman(0, 1)
            elif evenement.key() == Qt.Key.Key_Q:  
                self.controleur.deplacer_pacman(-1, 0)
            elif evenement.key() == Qt.Key.Key_D:  
                self.controleur.deplacer_pacman(1, 0)
