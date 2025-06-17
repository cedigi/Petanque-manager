#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pétanque Manager - Application de gestion de tournois de pétanque
Point d'entrée principal de l'application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui import MainWindow

def main():
    """Point d'entrée principal de l'application"""
    # Configuration de l'application
    app = QApplication(sys.argv)
    app.setApplicationName("Pétanque Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Pétanque Manager")

    # Charger la feuille de style QSS
    style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
    with open(style_path, "r") as f:
        base_style = f.read()
    app.setStyleSheet(base_style)
    
    # Configuration pour les écrans haute résolution
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Création et affichage de la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Lancement de la boucle d'événements
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()