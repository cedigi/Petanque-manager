#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de base de données SQLite pour Pétanque Manager
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class DatabaseManager:
    """Gestionnaire de base de données SQLite"""
    
    def __init__(self, db_path: str = "petanque.db"):
        self.db_path = db_path
        self.connection = None
        self.init_database()
        
    def init_database(self):
        """Initialiser la base de données et créer les tables"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        
        cursor = self.connection.cursor()
        
        # Table des tournois
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                terrain_count INTEGER NOT NULL,
                current_round INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL
            )
        """)
        
        # Table des équipes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id) ON DELETE CASCADE
            )
        """)
        
        # Table des joueurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                position INTEGER DEFAULT 1,
                FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        """)
        
        # Table des matchs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                round_number INTEGER NOT NULL,
                team1_id INTEGER NOT NULL,
                team2_id INTEGER NOT NULL,
                score1 INTEGER NULL,
                score2 INTEGER NULL,
                terrain INTEGER NULL,
                completed BOOLEAN DEFAULT FALSE,
                is_bye BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id) ON DELETE CASCADE,
                FOREIGN KEY (team1_id) REFERENCES teams (id) ON DELETE CASCADE,
                FOREIGN KEY (team2_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        """)
        
        self.connection.commit()
        
    def create_tournament(self, name: str, tournament_type: str, terrain_count: int) -> int:
        """Créer un nouveau tournoi"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO tournaments (name, type, terrain_count)
            VALUES (?, ?, ?)
        """, (name, tournament_type, terrain_count))
        
        tournament_id = cursor.lastrowid
        self.connection.commit()
        return tournament_id
        
    def get_tournament(self, tournament_id: int) -> Optional[Dict]:
        """Récupérer un tournoi par son ID"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM tournaments WHERE id = ?
        """, (tournament_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def get_all_tournaments(self) -> List[Dict]:
        """Récupérer tous les tournois"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM tournaments ORDER BY created_at DESC
        """)
        
        return [dict(row) for row in cursor.fetchall()]
        
    def create_team(self, tournament_id: int, number: int, players: List[str]) -> int:
        """Créer une nouvelle équipe"""
        cursor = self.connection.cursor()
        
        # Créer l'équipe
        cursor.execute("""
            INSERT INTO teams (tournament_id, number)
            VALUES (?, ?)
        """, (tournament_id, number))
        
        team_id = cursor.lastrowid
        
        # Ajouter les joueurs
        for i, player_name in enumerate(players, 1):
            cursor.execute("""
                INSERT INTO players (team_id, name, position)
                VALUES (?, ?, ?)
            """, (team_id, player_name, i))
            
        self.connection.commit()
        return team_id
        
    def get_teams_by_tournament(self, tournament_id: int) -> List[Dict]:
        """Récupérer toutes les équipes d'un tournoi"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT t.*, GROUP_CONCAT(p.name, ', ') as players
            FROM teams t
            LEFT JOIN players p ON t.id = p.team_id
            WHERE t.tournament_id = ?
            GROUP BY t.id
            ORDER BY t.number
        """, (tournament_id,))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def delete_team(self, team_id: int):
        """Supprimer une équipe"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
        self.connection.commit()
        
    def create_match(self, tournament_id: int, round_number: int, team1_id: int, 
                    team2_id: int, is_bye: bool = False) -> int:
        """Créer un nouveau match"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO matches (tournament_id, round_number, team1_id, team2_id, is_bye)
            VALUES (?, ?, ?, ?, ?)
        """, (tournament_id, round_number, team1_id, team2_id, is_bye))
        
        match_id = cursor.lastrowid
        self.connection.commit()
        return match_id
        
    def update_match_score(self, match_id: int, score1: int, score2: int, 
                          terrain: Optional[int] = None):
        """Mettre à jour le score d'un match"""
        cursor = self.connection.cursor()
        
        if terrain is not None:
            cursor.execute("""
                UPDATE matches 
                SET score1 = ?, score2 = ?, terrain = ?, completed = TRUE, completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (score1, score2, terrain, match_id))
        else:
            cursor.execute("""
                UPDATE matches 
                SET score1 = ?, score2 = ?, completed = TRUE, completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (score1, score2, match_id))
            
        self.connection.commit()
        
    def get_matches_by_tournament(self, tournament_id: int) -> List[Dict]:
        """Récupérer tous les matchs d'un tournoi"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT m.*, 
                   t1.number as team1_number, t2.number as team2_number,
                   GROUP_CONCAT(DISTINCT p1.name) as team1_players,
                   GROUP_CONCAT(DISTINCT p2.name) as team2_players
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.id
            JOIN teams t2 ON m.team2_id = t2.id
            LEFT JOIN players p1 ON t1.id = p1.team_id
            LEFT JOIN players p2 ON t2.id = p2.team_id
            WHERE m.tournament_id = ?
            GROUP BY m.id
            ORDER BY m.round_number, m.id
        """, (tournament_id,))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def get_matches_by_round(self, tournament_id: int, round_number: int) -> List[Dict]:
        """Récupérer les matchs d'un tour spécifique"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT m.*, 
                   t1.number as team1_number, t2.number as team2_number,
                   GROUP_CONCAT(DISTINCT p1.name) as team1_players,
                   GROUP_CONCAT(DISTINCT p2.name) as team2_players
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.id
            JOIN teams t2 ON m.team2_id = t2.id
            LEFT JOIN players p1 ON t1.id = p1.team_id
            LEFT JOIN players p2 ON t2.id = p2.team_id
            WHERE m.tournament_id = ? AND m.round_number = ?
            GROUP BY m.id
            ORDER BY m.id
        """, (tournament_id, round_number))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def update_tournament_round(self, tournament_id: int, round_number: int):
        """Mettre à jour le tour actuel du tournoi"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE tournaments SET current_round = ? WHERE id = ?
        """, (round_number, tournament_id))
        self.connection.commit()
        
    def complete_tournament(self, tournament_id: int):
        """Marquer un tournoi comme terminé"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE tournaments SET completed_at = CURRENT_TIMESTAMP WHERE id = ?
        """, (tournament_id,))
        self.connection.commit()
        
    def get_team_stats(self, tournament_id: int) -> List[Dict]:
        """Calculer les statistiques des équipes"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT 
                t.id,
                t.number,
                GROUP_CONCAT(p.name, ', ') as players,
                COUNT(CASE WHEN (m1.team1_id = t.id AND m1.score1 > m1.score2) OR 
                                (m1.team2_id = t.id AND m1.score2 > m1.score1) 
                           THEN 1 END) as wins,
                COUNT(CASE WHEN (m1.team1_id = t.id AND m1.score1 < m1.score2) OR 
                                (m1.team2_id = t.id AND m1.score2 < m1.score1) 
                           THEN 1 END) as losses,
                COALESCE(SUM(CASE WHEN m1.team1_id = t.id THEN m1.score1 
                                  WHEN m1.team2_id = t.id THEN m1.score2 
                                  ELSE 0 END), 0) as points_for,
                COALESCE(SUM(CASE WHEN m1.team1_id = t.id THEN m1.score2 
                                  WHEN m1.team2_id = t.id THEN m1.score1 
                                  ELSE 0 END), 0) as points_against
            FROM teams t
            LEFT JOIN players p ON t.id = p.team_id
            LEFT JOIN matches m1 ON (t.id = m1.team1_id OR t.id = m1.team2_id) AND m1.completed = TRUE
            WHERE t.tournament_id = ?
            GROUP BY t.id, t.number
            ORDER BY wins DESC, (points_for - points_against) DESC, points_for DESC
        """, (tournament_id,))
        
        return [dict(row) for row in cursor.fetchall()]
        
    def close(self):
        """Fermer la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            
    def __del__(self):
        """Destructeur pour s'assurer que la connexion est fermée"""
        self.close()