#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget pour la gestion des matchs
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton, QLabel, 
                             QFrame, QSpinBox, QMessageBox, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from tournament import Tournament, Match

class MatchWidget(QWidget):
    """Widget pour gérer les matchs"""
    
    match_completed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.tournament = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre
        title = QLabel("Gestion des Matchs")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Zone de contrôle des tours
        self.setup_round_control(layout)
        
        # Tableau des matchs
        self.setup_matches_table(layout)
        
    def setup_round_control(self, parent_layout):
        """Configuration des contrôles de tour"""
        group_box = QGroupBox("Contrôle des Tours")
        group_layout = QHBoxLayout()
        group_box.setLayout(group_layout)
        
        # Sélecteur de tour
        group_layout.addWidget(QLabel("Tour:"))
        self.round_combo = QComboBox()
        self.round_combo.currentTextChanged.connect(self.on_round_changed)
        group_layout.addWidget(self.round_combo)
        
        group_layout.addStretch()
        
        # Boutons
        self.generate_first_round_btn = QPushButton("Générer 1er Tour")
        self.generate_first_round_btn.clicked.connect(self.generate_first_round)
        group_layout.addWidget(self.generate_first_round_btn)
        
        self.generate_next_round_btn = QPushButton("Générer Tour Suivant")
        self.generate_next_round_btn.clicked.connect(self.generate_next_round)
        self.generate_next_round_btn.setEnabled(False)
        group_layout.addWidget(self.generate_next_round_btn)
        
        parent_layout.addWidget(group_box)
        
    def setup_matches_table(self, parent_layout):
        """Configuration du tableau des matchs"""
        # Label
        self.matches_label = QLabel("Aucun match généré")
        self.matches_label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(self.matches_label)
        
        # Tableau
        self.matches_table = QTableWidget()
        self.matches_table.setColumnCount(7)
        self.matches_table.setHorizontalHeaderLabels([
            "Tour", "Équipe 1", "Score 1", "Score 2", "Équipe 2", "Terrain", "Statut"
        ])
        
        # Configuration des colonnes
        header = self.matches_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        # Style du tableau
        self.matches_table.setAlternatingRowColors(True)
        self.matches_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        parent_layout.addWidget(self.matches_table)
        
    def set_tournament(self, tournament: Tournament):
        """Définir le tournoi actuel"""
        self.tournament = tournament
        self.refresh_ui()
        
    def refresh_teams(self):
        """Rafraîchir après changement d'équipes"""
        self.refresh_ui()
        
    def refresh_ui(self):
        """Rafraîchir l'interface utilisateur"""
        if not self.tournament:
            self.matches_table.setRowCount(0)
            self.matches_label.setText("Aucun tournoi sélectionné")
            self.generate_first_round_btn.setEnabled(False)
            self.generate_next_round_btn.setEnabled(False)
            return
            
        # Vérifier si on peut générer le premier tour
        can_generate_first = len(self.tournament.teams) >= 2 and self.tournament.current_round == 0
        self.generate_first_round_btn.setEnabled(can_generate_first)
        
        # Vérifier si on peut générer le tour suivant
        can_generate_next = (self.tournament.current_round > 0 and 
                           self.tournament.is_round_complete(self.tournament.current_round))
        self.generate_next_round_btn.setEnabled(can_generate_next)
        
        # Mettre à jour le sélecteur de tour
        self.update_round_combo()
        
        # Rafraîchir le tableau des matchs
        self.refresh_matches_table()
        
    def update_round_combo(self):
        """Mettre à jour le sélecteur de tour"""
        self.round_combo.clear()
        
        if not self.tournament or self.tournament.current_round == 0:
            return
            
        for round_num in range(1, self.tournament.current_round + 1):
            self.round_combo.addItem(f"Tour {round_num}")
            
        # Sélectionner le dernier tour
        if self.round_combo.count() > 0:
            self.round_combo.setCurrentIndex(self.round_combo.count() - 1)
            
    def on_round_changed(self):
        """Appelé quand le tour sélectionné change"""
        self.refresh_matches_table()
        
    def generate_first_round(self):
        """Générer les matchs du premier tour"""
        if not self.tournament or len(self.tournament.teams) < 2:
            QMessageBox.warning(self, "Erreur", "Il faut au moins 2 équipes pour générer des matchs")
            return
            
        matches = self.tournament.generate_first_round_matches()
        
        if matches:
            QMessageBox.information(self, "Succès", f"{len(matches)} match(s) généré(s) pour le tour 1")
            self.refresh_ui()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de générer les matchs")
            
    def generate_next_round(self):
        """Générer les matchs du tour suivant"""
        if not self.tournament:
            return
            
        if not self.tournament.is_round_complete(self.tournament.current_round):
            QMessageBox.warning(self, "Erreur", "Le tour actuel n'est pas terminé")
            return
            
        matches = self.tournament.generate_next_round_matches()
        
        if matches:
            QMessageBox.information(self, "Succès", f"{len(matches)} match(s) généré(s) pour le tour {self.tournament.current_round}")
            self.refresh_ui()
        else:
            QMessageBox.information(self, "Information", "Aucun nouveau match à générer (tournoi terminé ?)")
            
    def refresh_matches_table(self):
        """Rafraîchir le tableau des matchs"""
        if not self.tournament:
            self.matches_table.setRowCount(0)
            self.matches_label.setText("Aucun tournoi sélectionné")
            return
            
        # Déterminer quel tour afficher
        current_round = 1
        if self.round_combo.currentText():
            try:
                current_round = int(self.round_combo.currentText().split()[-1])
            except:
                current_round = 1
                
        # Obtenir les matchs du tour sélectionné
        matches = self.tournament.get_matches_by_round(current_round)
        
        if not matches:
            self.matches_table.setRowCount(0)
            self.matches_label.setText(f"Aucun match pour le tour {current_round}")
            return
            
        self.matches_label.setText(f"Matchs du tour {current_round}")
        self.matches_table.setRowCount(len(matches))
        
        for row, match in enumerate(matches):
            # Tour
            round_item = QTableWidgetItem(str(match.round_number))
            round_item.setTextAlignment(Qt.AlignCenter)
            self.matches_table.setItem(row, 0, round_item)
            
            # Équipe 1
            team1_text = f"{match.team1.get_display_name()}\n{match.team1.get_players_names()}"
            team1_item = QTableWidgetItem(team1_text)
            self.matches_table.setItem(row, 1, team1_item)
            
            # Score 1
            if match.completed:
                score1_item = QTableWidgetItem(str(match.score1 or 0))
                score1_item.setTextAlignment(Qt.AlignCenter)
                self.matches_table.setItem(row, 2, score1_item)
            else:
                score1_spin = QSpinBox()
                score1_spin.setRange(0, 13)
                score1_spin.setValue(match.score1 or 0)
                score1_spin.valueChanged.connect(
                    lambda value, m=match, pos=1: self.on_score_changed(m, pos, value)
                )
                self.matches_table.setCellWidget(row, 2, score1_spin)
                
            # Score 2
            if match.completed:
                score2_item = QTableWidgetItem(str(match.score2 or 0))
                score2_item.setTextAlignment(Qt.AlignCenter)
                self.matches_table.setItem(row, 3, score2_item)
            else:
                score2_spin = QSpinBox()
                score2_spin.setRange(0, 13)
                score2_spin.setValue(match.score2 or 0)
                score2_spin.valueChanged.connect(
                    lambda value, m=match, pos=2: self.on_score_changed(m, pos, value)
                )
                self.matches_table.setCellWidget(row, 3, score2_spin)
                
            # Équipe 2
            team2_text = f"{match.team2.get_display_name()}\n{match.team2.get_players_names()}"
            team2_item = QTableWidgetItem(team2_text)
            self.matches_table.setItem(row, 4, team2_item)
            
            # Terrain
            if match.completed:
                terrain_item = QTableWidgetItem(str(match.terrain or ""))
                terrain_item.setTextAlignment(Qt.AlignCenter)
                self.matches_table.setItem(row, 5, terrain_item)
            else:
                terrain_spin = QSpinBox()
                terrain_spin.setRange(1, self.tournament.terrain_count)
                terrain_spin.setValue(match.terrain or 1)
                terrain_spin.valueChanged.connect(
                    lambda value, m=match: self.on_terrain_changed(m, value)
                )
                self.matches_table.setCellWidget(row, 5, terrain_spin)
                
            # Statut
            if match.completed:
                winner = match.get_winner()
                status_text = f"Terminé\nGagnant: {winner.get_display_name() if winner else 'Égalité'}"
                status_item = QTableWidgetItem(status_text)
                status_item.setTextAlignment(Qt.AlignCenter)
                self.matches_table.setItem(row, 6, status_item)
            else:
                validate_btn = QPushButton("Valider")
                validate_btn.clicked.connect(lambda checked, m=match: self.validate_match(m))
                validate_btn.setStyleSheet("background-color: #28a745; color: white;")
                self.matches_table.setCellWidget(row, 6, validate_btn)
                
        # Ajuster la hauteur des lignes
        self.matches_table.resizeRowsToContents()
        
    def on_score_changed(self, match: Match, position: int, value: int):
        """Appelé quand un score change"""
        if position == 1:
            match.score1 = value
        else:
            match.score2 = value
            
    def on_terrain_changed(self, match: Match, value: int):
        """Appelé quand le terrain change"""
        match.terrain = value
        
    def validate_match(self, match: Match):
        """Valider un match"""
        if match.score1 is None or match.score2 is None:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir les scores")
            return
            
        if match.score1 == match.score2:
            QMessageBox.warning(self, "Erreur", "Il ne peut pas y avoir d'égalité en pétanque")
            return
            
        if max(match.score1, match.score2) != 13:
            reply = QMessageBox.question(
                self, "Confirmation",
                "Un match de pétanque se joue normalement en 13 points.\n"
                "Voulez-vous vraiment valider ce score ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
                
        # Valider le match
        match.completed = True
        
        # Rafraîchir l'affichage
        self.refresh_matches_table()
        self.refresh_ui()
        self.match_completed.emit()
        
        QMessageBox.information(self, "Succès", "Match validé avec succès")