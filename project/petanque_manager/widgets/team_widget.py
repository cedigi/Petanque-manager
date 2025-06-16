#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget pour la gestion des équipes et joueurs
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QLabel, QFrame, QGroupBox,
                             QSpinBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from tournament import Tournament, Team, Player

class TeamWidget(QWidget):
    """Widget pour gérer les équipes et joueurs"""
    
    teams_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.tournament = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre
        title = QLabel("Gestion des Équipes et Joueurs")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Zone d'ajout d'équipe
        self.setup_add_team_section(layout)
        
        # Tableau des équipes
        self.setup_teams_table(layout)
        
    def setup_add_team_section(self, parent_layout):
        """Configuration de la section d'ajout d'équipe"""
        group_box = QGroupBox("Ajouter une équipe")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)
        
        # Formulaire d'ajout
        form_layout = QFormLayout()
        
        # Champs pour les joueurs (adaptatif selon le type de tournoi)
        self.player_inputs = []
        for i in range(6):  # Maximum 6 joueurs pour sextette
            player_input = QLineEdit()
            player_input.setPlaceholderText(f"Joueur {i+1}")
            self.player_inputs.append(player_input)
            form_layout.addRow(f"Joueur {i+1}:", player_input)
            
        group_layout.addLayout(form_layout)
        
        # Bouton d'ajout
        self.add_team_btn = QPushButton("Ajouter l'équipe")
        self.add_team_btn.clicked.connect(self.add_team)
        self.add_team_btn.setEnabled(False)
        group_layout.addWidget(self.add_team_btn)
        
        parent_layout.addWidget(group_box)
        
    def setup_teams_table(self, parent_layout):
        """Configuration du tableau des équipes"""
        # Label
        label = QLabel("Équipes inscrites")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(label)
        
        # Tableau
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(4)
        self.teams_table.setHorizontalHeaderLabels([
            "N° Équipe", "Joueurs", "Actions", "Statut"
        ])
        
        # Configuration des colonnes
        header = self.teams_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Style du tableau
        self.teams_table.setAlternatingRowColors(True)
        self.teams_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        parent_layout.addWidget(self.teams_table)
        
    def set_tournament(self, tournament: Tournament):
        """Définir le tournoi actuel"""
        self.tournament = tournament
        self.update_ui_for_tournament_type()
        self.refresh_teams_table()
        
    def update_ui_for_tournament_type(self):
        """Mettre à jour l'interface selon le type de tournoi"""
        if not self.tournament:
            return
            
        # Déterminer le nombre de joueurs requis
        players_needed = {
            "tête-à-tête": 1,
            "doublette": 2,
            "triplette": 3,
            "quadrette": 4,
            "mêlée": 1,
            "sextette": 6
        }.get(self.tournament.tournament_type, 2)
        
        # Afficher/masquer les champs de joueurs
        for i, input_field in enumerate(self.player_inputs):
            if i < players_needed:
                input_field.show()
                input_field.parentWidget().show()
                # Marquer les champs obligatoires
                if i < min(2, players_needed):
                    input_field.setPlaceholderText(f"Joueur {i+1} *")
                else:
                    input_field.setPlaceholderText(f"Joueur {i+1}")
            else:
                input_field.hide()
                input_field.parentWidget().hide()
                
        # Activer le bouton d'ajout
        self.add_team_btn.setEnabled(True)
        
    def add_team(self):
        """Ajouter une nouvelle équipe"""
        if not self.tournament:
            QMessageBox.warning(self, "Erreur", "Aucun tournoi sélectionné")
            return
            
        # Récupérer les noms des joueurs
        players = []
        for input_field in self.player_inputs:
            if input_field.isVisible() and input_field.text().strip():
                players.append(input_field.text().strip())
                
        # Vérifier qu'on a au moins un joueur
        if not players:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir au moins un joueur")
            return
            
        # Ajouter l'équipe au tournoi
        team = self.tournament.add_team(players)
        
        # Vider les champs
        for input_field in self.player_inputs:
            input_field.clear()
            
        # Rafraîchir l'affichage
        self.refresh_teams_table()
        self.teams_changed.emit()
        
    def remove_team(self, team_id: int):
        """Supprimer une équipe"""
        reply = QMessageBox.question(
            self, "Confirmation", 
            "Êtes-vous sûr de vouloir supprimer cette équipe ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.tournament.remove_team(team_id)
            self.refresh_teams_table()
            self.teams_changed.emit()
            
    def refresh_teams_table(self):
        """Rafraîchir le tableau des équipes"""
        if not self.tournament:
            self.teams_table.setRowCount(0)
            return
            
        teams = self.tournament.teams
        self.teams_table.setRowCount(len(teams))
        
        for row, team in enumerate(teams):
            # Numéro d'équipe
            team_number_item = QTableWidgetItem(f"Équipe {team.number}")
            team_number_item.setTextAlignment(Qt.AlignCenter)
            self.teams_table.setItem(row, 0, team_number_item)
            
            # Joueurs
            players_text = team.get_players_names()
            players_item = QTableWidgetItem(players_text)
            self.teams_table.setItem(row, 1, players_item)
            
            # Bouton de suppression
            remove_btn = QPushButton("Supprimer")
            remove_btn.clicked.connect(lambda checked, tid=team.id: self.remove_team(tid))
            remove_btn.setStyleSheet("background-color: #dc3545; color: white;")
            self.teams_table.setCellWidget(row, 2, remove_btn)
            
            # Statut
            status_item = QTableWidgetItem("Inscrite")
            status_item.setTextAlignment(Qt.AlignCenter)
            self.teams_table.setItem(row, 3, status_item)
            
        # Ajuster la hauteur des lignes
        self.teams_table.resizeRowsToContents()