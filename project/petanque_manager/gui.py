#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface graphique principale de Pétanque Manager
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QMenuBar, QAction, QStatusBar, 
                             QMessageBox, QDialog, QFormLayout, QLineEdit, 
                             QComboBox, QSpinBox, QPushButton, QDialogButtonBox,
                             QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from tournament import Tournament
from store import DatabaseManager
from widgets.team_widget import TeamWidget
from widgets.match_widget import MatchWidget
from widgets.standings_widget import StandingsWidget

class NewTournamentDialog(QDialog):
    """Dialog pour créer un nouveau tournoi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Tournoi")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QFormLayout()
        
        # Nom du tournoi
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nom du tournoi")
        layout.addRow("Nom du tournoi:", self.name_edit)
        
        # Type de tournoi
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "tête-à-tête",
            "doublette", 
            "triplette",
            "quadrette",
            "mêlée"
        ])
        layout.addRow("Type de tournoi:", self.type_combo)
        
        # Nombre de terrains
        self.terrain_spin = QSpinBox()
        self.terrain_spin.setMinimum(1)
        self.terrain_spin.setMaximum(20)
        self.terrain_spin.setValue(4)
        layout.addRow("Nombre de terrains:", self.terrain_spin)
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
    def get_tournament_data(self):
        """Retourne les données du tournoi"""
        return {
            'name': self.name_edit.text().strip(),
            'type': self.type_combo.currentText(),
            'terrain_count': self.terrain_spin.value()
        }

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self):
        super().__init__()
        self.tournament = None
        self.db_manager = DatabaseManager()
        self.dark_theme = False
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.apply_theme()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setWindowTitle("Pétanque Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Barre d'outils pour nouveau tournoi
        toolbar_layout = QHBoxLayout()
        
        self.new_tournament_btn = QPushButton("Nouveau Tournoi")
        self.new_tournament_btn.clicked.connect(self.new_tournament)
        toolbar_layout.addWidget(self.new_tournament_btn)
        
        self.tournament_label = QLabel("Aucun tournoi actif")
        self.tournament_label.setStyleSheet("font-weight: bold; color: #666;")
        toolbar_layout.addWidget(self.tournament_label)
        
        toolbar_layout.addStretch()
        main_layout.addLayout(toolbar_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Onglets
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Onglet Équipes/Joueurs
        self.team_widget = TeamWidget()
        self.tab_widget.addTab(self.team_widget, "Équipes/Joueurs")
        
        # Onglet Matchs
        self.match_widget = MatchWidget()
        self.tab_widget.addTab(self.match_widget, "Matchs")
        
        # Onglet Classement
        self.standings_widget = StandingsWidget()
        self.tab_widget.addTab(self.standings_widget, "Classement")
        
        # Connexions des signaux
        self.team_widget.teams_changed.connect(self.on_teams_changed)
        self.match_widget.match_completed.connect(self.on_match_completed)
        
    def setup_menu(self):
        """Configuration du menu"""
        menubar = self.menuBar()
        
        # Menu Affichage
        view_menu = menubar.addMenu("Affichage")
        
        theme_action = QAction("Thème sombre", self)
        theme_action.setCheckable(True)
        theme_action.setChecked(self.dark_theme)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Configuration de la barre de statut"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
        
    def new_tournament(self):
        """Créer un nouveau tournoi"""
        dialog = NewTournamentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_tournament_data()
            
            if not data['name']:
                QMessageBox.warning(self, "Erreur", "Le nom du tournoi est obligatoire")
                return
                
            # Créer le tournoi
            self.tournament = Tournament(
                name=data['name'],
                tournament_type=data['type'],
                terrain_count=data['terrain_count']
            )
            
            # Sauvegarder en base
            tournament_id = self.db_manager.create_tournament(
                data['name'], data['type'], data['terrain_count']
            )
            self.tournament.id = tournament_id
            
            # Mettre à jour l'interface
            self.tournament_label.setText(f"Tournoi: {data['name']} ({data['type']})")
            self.team_widget.set_tournament(self.tournament)
            self.match_widget.set_tournament(self.tournament)
            self.standings_widget.set_tournament(self.tournament)
            
            self.status_bar.showMessage(f"Nouveau tournoi créé: {data['name']}")
            
    def on_teams_changed(self):
        """Appelé quand les équipes changent"""
        if self.tournament:
            self.match_widget.refresh_teams()
            self.standings_widget.refresh_standings()
            
    def on_match_completed(self):
        """Appelé quand un match est terminé"""
        if self.tournament:
            self.standings_widget.refresh_standings()
            
    def toggle_theme(self, checked):
        """Basculer entre thème clair et sombre"""
        self.dark_theme = checked
        self.apply_theme()
        
    def apply_theme(self):
        """Appliquer le thème actuel"""
        style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        with open(style_path, "r") as f:
            style = f.read()
        if self.dark_theme:
            app_style = ".dark {\n" + style + "\n}"
        else:
            app_style = style
        QApplication.instance().setStyleSheet(app_style)
            
    def show_about(self):
        """Afficher la boîte de dialogue À propos"""
        QMessageBox.about(self, "À propos", 
                         "Pétanque Manager v1.0.0\n\n"
                         "Application de gestion de tournois de pétanque\n"
                         "Développée avec PyQt5")
        
    def closeEvent(self, event):
        """Événement de fermeture de l'application"""
        self.db_manager.close()
        event.accept()