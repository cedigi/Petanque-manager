#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget pour l'affichage du classement
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QFrame, QPushButton, QHBoxLayout,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from tournament import Tournament

class StandingsWidget(QWidget):
    """Widget pour afficher le classement"""
    
    def __init__(self):
        super().__init__()
        self.tournament = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre
        title = QLabel("Classement du Tournoi")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Boutons d'action
        self.setup_action_buttons(layout)
        
        # Tableau du classement
        self.setup_standings_table(layout)
        
    def setup_action_buttons(self, parent_layout):
        """Configuration des boutons d'action"""
        buttons_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_standings)
        buttons_layout.addWidget(self.refresh_btn)
        
        buttons_layout.addStretch()
        
        self.export_btn = QPushButton("Exporter")
        self.export_btn.clicked.connect(self.export_standings)
        self.export_btn.setEnabled(False)  # À implémenter plus tard
        buttons_layout.addWidget(self.export_btn)
        
        parent_layout.addLayout(buttons_layout)
        
    def setup_standings_table(self, parent_layout):
        """Configuration du tableau de classement"""
        # Label
        self.standings_label = QLabel("Classement non disponible")
        self.standings_label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(self.standings_label)
        
        # Tableau
        self.standings_table = QTableWidget()
        self.standings_table.setColumnCount(7)
        self.standings_table.setHorizontalHeaderLabels([
            "Position", "Équipe", "Joueurs", "Victoires", "Défaites", 
            "Points +/-", "Taux de victoire"
        ])
        
        # Configuration des colonnes
        header = self.standings_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        # Style du tableau
        self.standings_table.setAlternatingRowColors(True)
        self.standings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.standings_table.setSortingEnabled(False)  # Désactiver le tri manuel
        
        parent_layout.addWidget(self.standings_table)
        
    def set_tournament(self, tournament: Tournament):
        """Définir le tournoi actuel"""
        self.tournament = tournament
        self.refresh_standings()
        
    def refresh_standings(self):
        """Rafraîchir le classement"""
        if not self.tournament:
            self.standings_table.setRowCount(0)
            self.standings_label.setText("Aucun tournoi sélectionné")
            return
            
        if not self.tournament.teams:
            self.standings_table.setRowCount(0)
            self.standings_label.setText("Aucune équipe inscrite")
            return
            
        # Obtenir les statistiques
        stats_list = self.tournament.get_all_stats()
        
        if not stats_list:
            self.standings_table.setRowCount(0)
            self.standings_label.setText("Aucune statistique disponible")
            return
            
        self.standings_label.setText(f"Classement - {len(stats_list)} équipe(s)")
        self.standings_table.setRowCount(len(stats_list))
        
        for row, stats in enumerate(stats_list):
            # Position
            position_item = QTableWidgetItem(str(row + 1))
            position_item.setTextAlignment(Qt.AlignCenter)
            
            # Colorer les 3 premières positions
            if row == 0:  # 1ère place - Or
                position_item.setBackground(QColor(255, 215, 0))
            elif row == 1:  # 2ème place - Argent
                position_item.setBackground(QColor(192, 192, 192))
            elif row == 2:  # 3ème place - Bronze
                position_item.setBackground(QColor(205, 127, 50))
                
            self.standings_table.setItem(row, 0, position_item)
            
            # Équipe
            team_item = QTableWidgetItem(stats.team.get_display_name())
            team_item.setTextAlignment(Qt.AlignCenter)
            self.standings_table.setItem(row, 1, team_item)
            
            # Joueurs
            players_item = QTableWidgetItem(stats.team.get_players_names())
            self.standings_table.setItem(row, 2, players_item)
            
            # Victoires
            wins_item = QTableWidgetItem(str(stats.wins))
            wins_item.setTextAlignment(Qt.AlignCenter)
            self.standings_table.setItem(row, 3, wins_item)
            
            # Défaites
            losses_item = QTableWidgetItem(str(stats.losses))
            losses_item.setTextAlignment(Qt.AlignCenter)
            self.standings_table.setItem(row, 4, losses_item)
            
            # Différence de points
            diff_text = f"+{stats.points_difference}" if stats.points_difference > 0 else str(stats.points_difference)
            diff_item = QTableWidgetItem(diff_text)
            diff_item.setTextAlignment(Qt.AlignCenter)
            
            # Colorer selon la différence
            if stats.points_difference > 0:
                diff_item.setForeground(QColor(0, 128, 0))  # Vert
            elif stats.points_difference < 0:
                diff_item.setForeground(QColor(255, 0, 0))  # Rouge
                
            self.standings_table.setItem(row, 5, diff_item)
            
            # Taux de victoire
            win_rate_text = f"{stats.win_rate:.1%}"
            win_rate_item = QTableWidgetItem(win_rate_text)
            win_rate_item.setTextAlignment(Qt.AlignCenter)
            self.standings_table.setItem(row, 6, win_rate_item)
            
        # Ajuster la hauteur des lignes
        self.standings_table.resizeRowsToContents()
        
    def export_standings(self):
        """Exporter le classement (à implémenter)"""
        QMessageBox.information(self, "Information", "Fonctionnalité d'export à venir")
