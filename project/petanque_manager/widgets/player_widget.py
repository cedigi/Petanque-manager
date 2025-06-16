#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget pour la gestion des joueurs individuels (pour la mêlée)
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QMessageBox, QLabel, QFrame, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class PlayerWidget(QWidget):
    """Widget pour gérer les joueurs individuels"""
    
    players_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.players = []
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre
        title = QLabel("Gestion des Joueurs")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Zone d'ajout de joueur
        self.setup_add_player_section(layout)
        
        # Liste des joueurs
        self.setup_players_list(layout)
        
    def setup_add_player_section(self, parent_layout):
        """Configuration de la section d'ajout de joueur"""
        group_box = QGroupBox("Ajouter un joueur")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)
        
        # Formulaire d'ajout
        form_layout = QFormLayout()
        
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Nom du joueur")
        self.player_name_input.returnPressed.connect(self.add_player)
        form_layout.addRow("Nom:", self.player_name_input)
        
        group_layout.addLayout(form_layout)
        
        # Bouton d'ajout
        self.add_player_btn = QPushButton("Ajouter le joueur")
        self.add_player_btn.clicked.connect(self.add_player)
        group_layout.addWidget(self.add_player_btn)
        
        parent_layout.addWidget(group_box)
        
    def setup_players_list(self, parent_layout):
        """Configuration de la liste des joueurs"""
        # Label
        label = QLabel("Joueurs inscrits")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(label)
        
        # Liste
        self.players_list = QListWidget()
        self.players_list.setAlternatingRowColors(True)
        parent_layout.addWidget(self.players_list)
        
        # Bouton de suppression
        self.remove_player_btn = QPushButton("Supprimer le joueur sélectionné")
        self.remove_player_btn.clicked.connect(self.remove_selected_player)
        self.remove_player_btn.setEnabled(False)
        self.remove_player_btn.setStyleSheet("background-color: #dc3545; color: white;")
        parent_layout.addWidget(self.remove_player_btn)
        
        # Connexion des signaux
        self.players_list.itemSelectionChanged.connect(self.on_selection_changed)
        
    def add_player(self):
        """Ajouter un nouveau joueur"""
        name = self.player_name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un nom de joueur")
            return
            
        if name in self.players:
            QMessageBox.warning(self, "Erreur", "Ce joueur est déjà inscrit")
            return
            
        # Ajouter le joueur
        self.players.append(name)
        
        # Vider le champ
        self.player_name_input.clear()
        
        # Rafraîchir l'affichage
        self.refresh_players_list()
        self.players_changed.emit()
        
    def remove_selected_player(self):
        """Supprimer le joueur sélectionné"""
        current_item = self.players_list.currentItem()
        if not current_item:
            return
            
        player_name = current_item.text()
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer {player_name} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.players.remove(player_name)
            self.refresh_players_list()
            self.players_changed.emit()
            
    def on_selection_changed(self):
        """Appelé quand la sélection change"""
        has_selection = self.players_list.currentItem() is not None
        self.remove_player_btn.setEnabled(has_selection)
        
    def refresh_players_list(self):
        """Rafraîchir la liste des joueurs"""
        self.players_list.clear()
        
        for player in self.players:
            item = QListWidgetItem(player)
            self.players_list.addItem(item)
            
    def get_players(self):
        """Obtenir la liste des joueurs"""
        return self.players.copy()
        
    def clear_players(self):
        """Vider la liste des joueurs"""
        self.players.clear()
        self.refresh_players_list()
        self.players_changed.emit()