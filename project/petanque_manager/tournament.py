#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logique métier pour la gestion des tournois de pétanque
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Player:
    """Représente un joueur"""
    id: int
    name: str
    
@dataclass
class Team:
    """Représente une équipe"""
    id: int
    number: int
    players: List[Player] = field(default_factory=list)
    
    def get_display_name(self) -> str:
        """Retourne le nom d'affichage de l'équipe"""
        return f"Équipe {self.number}"
        
    def get_players_names(self) -> str:
        """Retourne les noms des joueurs séparés par des virgules"""
        return ", ".join([p.name for p in self.players])

@dataclass
class Match:
    """Représente un match"""
    id: int
    round_number: int
    team1: Team
    team2: Team
    score1: Optional[int] = None
    score2: Optional[int] = None
    terrain: Optional[int] = None
    completed: bool = False
    is_bye: bool = False
    
    def get_winner(self) -> Optional[Team]:
        """Retourne l'équipe gagnante"""
        if not self.completed or self.score1 is None or self.score2 is None:
            return None
        return self.team1 if self.score1 > self.score2 else self.team2
        
    def get_loser(self) -> Optional[Team]:
        """Retourne l'équipe perdante"""
        if not self.completed or self.score1 is None or self.score2 is None:
            return None
        return self.team2 if self.score1 > self.score2 else self.team1

@dataclass
class TeamStats:
    """Statistiques d'une équipe"""
    team: Team
    wins: int = 0
    losses: int = 0
    points_for: int = 0
    points_against: int = 0
    
    @property
    def points_difference(self) -> int:
        """Différence de points"""
        return self.points_for - self.points_against
        
    @property
    def win_rate(self) -> float:
        """Taux de victoire"""
        total = self.wins + self.losses
        return self.wins / total if total > 0 else 0.0

class Tournament:
    """Classe principale pour gérer un tournoi"""
    
    def __init__(self, name: str, tournament_type: str, terrain_count: int):
        self.id: Optional[int] = None
        self.name = name
        self.tournament_type = tournament_type
        self.terrain_count = terrain_count
        self.teams: List[Team] = []
        self.matches: List[Match] = []
        self.current_round = 0
        self.created_at = datetime.now()
        
    def add_team(self, players: List[str]) -> Team:
        """Ajouter une équipe au tournoi"""
        team_number = len(self.teams) + 1
        team = Team(
            id=team_number,
            number=team_number,
            players=[Player(i, name) for i, name in enumerate(players, 1)]
        )
        self.teams.append(team)
        return team
        
    def remove_team(self, team_id: int):
        """Supprimer une équipe du tournoi"""
        self.teams = [t for t in self.teams if t.id != team_id]
        # Renuméroter les équipes
        for i, team in enumerate(self.teams, 1):
            team.number = i
            
    def get_team_stats(self, team: Team) -> TeamStats:
        """Calculer les statistiques d'une équipe"""
        stats = TeamStats(team)
        
        for match in self.matches:
            if not match.completed:
                continue
                
            if match.team1.id == team.id:
                stats.points_for += match.score1 or 0
                stats.points_against += match.score2 or 0
                if (match.score1 or 0) > (match.score2 or 0):
                    stats.wins += 1
                else:
                    stats.losses += 1
            elif match.team2.id == team.id:
                stats.points_for += match.score2 or 0
                stats.points_against += match.score1 or 0
                if (match.score2 or 0) > (match.score1 or 0):
                    stats.wins += 1
                else:
                    stats.losses += 1
                    
        return stats
        
    def get_all_stats(self) -> List[TeamStats]:
        """Obtenir les statistiques de toutes les équipes"""
        stats = [self.get_team_stats(team) for team in self.teams]
        # Trier par nombre de victoires, puis par différence de points
        stats.sort(key=lambda s: (-s.wins, -s.points_difference, -s.points_for))
        return stats
        
    def generate_first_round_matches(self) -> List[Match]:
        """Générer les matchs du premier tour avec appariement aléatoire"""
        if len(self.teams) < 2:
            return []
            
        self.current_round = 1
        matches = []
        available_teams = self.teams.copy()
        
        # Mélanger pour éviter que l'équipe 1 joue contre la 2, etc.
        random.shuffle(available_teams)
        
        match_id = len(self.matches) + 1
        
        # Créer les paires
        while len(available_teams) >= 2:
            team1 = available_teams.pop(0)
            team2 = available_teams.pop(0)
            
            match = Match(
                id=match_id,
                round_number=self.current_round,
                team1=team1,
                team2=team2
            )
            matches.append(match)
            match_id += 1
            
        # Gérer le BYE si nombre impair d'équipes
        if available_teams:
            bye_team = available_teams[0]
            bye_match = Match(
                id=match_id,
                round_number=self.current_round,
                team1=bye_team,
                team2=Team(0, 0, [Player(0, "BYE")]),  # Équipe fictive
                score1=13,
                score2=7,
                completed=True,
                is_bye=True
            )
            matches.append(bye_match)
            
        self.matches.extend(matches)
        return matches
        
    def generate_next_round_matches(self) -> List[Match]:
        """Générer les matchs du tour suivant"""
        if self.tournament_type == "quadrette":
            return self._generate_quadrette_matches()
        elif self.tournament_type == "mêlée":
            return self._generate_melee_matches()
        else:
            return self._generate_standard_matches()
            
    def _generate_standard_matches(self) -> List[Match]:
        """Générer les matchs pour les tournois standards (tête-à-tête, doublette, triplette)"""
        # Obtenir les statistiques actuelles
        stats = self.get_all_stats()
        
        # Grouper par nombre de victoires
        groups = {}
        for stat in stats:
            wins = stat.wins
            if wins not in groups:
                groups[wins] = []
            groups[wins].append(stat.team)
            
        matches = []
        match_id = len(self.matches) + 1
        self.current_round += 1
        
        # Apparier les équipes par groupe de victoires
        for win_count in sorted(groups.keys(), reverse=True):
            teams_in_group = groups[win_count].copy()
            random.shuffle(teams_in_group)  # Mélanger pour éviter les répétitions
            
            while len(teams_in_group) >= 2:
                team1 = teams_in_group.pop(0)
                team2 = teams_in_group.pop(0)
                
                match = Match(
                    id=match_id,
                    round_number=self.current_round,
                    team1=team1,
                    team2=team2
                )
                matches.append(match)
                match_id += 1
                
        self.matches.extend(matches)
        return matches
        
    def _generate_quadrette_matches(self) -> List[Match]:
        """Générer les matchs pour le tournoi quadrette (7 tours fixes)"""
        if self.current_round >= 7:
            return []
            
        # Patterns pour les 7 tours de quadrette
        patterns = [
            ([0, 1, 2], [3]),      # ABC vs D
            ([0, 1], [2, 3]),      # AB vs CD
            ([0, 1, 3], [2]),      # ABD vs C
            ([0, 2], [1, 3]),      # AC vs BD
            ([0, 2, 3], [1]),      # ACD vs B
            ([0, 3], [1, 2]),      # AD vs BC
            ([1, 2, 3], [0])       # BCD vs A
        ]
        
        if len(self.teams) != 4:
            return []
            
        self.current_round += 1
        pattern = patterns[self.current_round - 1]
        
        # Créer les sous-groupes
        group1_players = []
        group2_players = []
        
        for team_idx in pattern[0]:
            if team_idx < len(self.teams):
                group1_players.extend(self.teams[team_idx].players)
                
        for team_idx in pattern[1]:
            if team_idx < len(self.teams):
                group2_players.extend(self.teams[team_idx].players)
        
        # Créer des équipes temporaires pour ce match
        temp_team1 = Team(
            id=1000 + self.current_round * 10 + 1,
            number=1,
            players=group1_players
        )
        temp_team2 = Team(
            id=1000 + self.current_round * 10 + 2,
            number=2,
            players=group2_players
        )
        
        match = Match(
            id=len(self.matches) + 1,
            round_number=self.current_round,
            team1=temp_team1,
            team2=temp_team2
        )
        
        self.matches.append(match)
        return [match]
        
    def _generate_melee_matches(self) -> List[Match]:
        """Générer les matchs pour la mêlée (tirage aléatoire complet)"""
        if len(self.teams) < 2:
            return []
            
        self.current_round += 1
        matches = []
        available_teams = self.teams.copy()
        random.shuffle(available_teams)
        
        match_id = len(self.matches) + 1
        
        while len(available_teams) >= 2:
            team1 = available_teams.pop(0)
            team2 = available_teams.pop(0)
            
            match = Match(
                id=match_id,
                round_number=self.current_round,
                team1=team1,
                team2=team2
            )
            matches.append(match)
            match_id += 1
            
        # Gérer le BYE si nécessaire
        if available_teams:
            bye_team = available_teams[0]
            bye_match = Match(
                id=match_id,
                round_number=self.current_round,
                team1=bye_team,
                team2=Team(0, 0, [Player(0, "BYE")]),
                score1=13,
                score2=7,
                completed=True,
                is_bye=True
            )
            matches.append(bye_match)
            
        self.matches.extend(matches)
        return matches
        
    def update_match_score(self, match_id: int, score1: int, score2: int, terrain: Optional[int] = None):
        """Mettre à jour le score d'un match"""
        for match in self.matches:
            if match.id == match_id:
                match.score1 = score1
                match.score2 = score2
                match.completed = True
                if terrain is not None:
                    match.terrain = terrain
                break
                
    def get_matches_by_round(self, round_number: int) -> List[Match]:
        """Obtenir les matchs d'un tour spécifique"""
        return [m for m in self.matches if m.round_number == round_number]
        
    def is_round_complete(self, round_number: int) -> bool:
        """Vérifier si un tour est terminé"""
        round_matches = self.get_matches_by_round(round_number)
        return len(round_matches) > 0 and all(m.completed for m in round_matches)