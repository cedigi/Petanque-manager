export interface Team {
  id: string;
  players: string[];
  createdAt: Date;
}

export interface Match {
  id: string;
  team1: Team;
  team2: Team;
  score1?: number;
  score2?: number;
  terrain: number;
  round: number;
  completed: boolean;
  createdAt: Date;
  completedAt?: Date;
}

export interface Tournament {
  id: string;
  name: string;
  type: TournamentType;
  teams: Team[];
  matches: Match[];
  currentRound: number;
  status: 'setup' | 'active' | 'completed';
  createdAt: Date;
  completedAt?: Date;
}

export interface TeamStats {
  team: Team;
  matchesPlayed: number;
  wins: number;
  losses: number;
  totalPointsFor: number;
  totalPointsAgainst: number;
  pointsDifference: number;
  winRate: number;
}

export interface TournamentType {
  id: string;
  name: string;
  description: string;
  playersPerTeam: number;
  icon: string;
}

export const TOURNAMENT_TYPES: TournamentType[] = [
  {
    id: 'tete-a-tete',
    name: 'Tête à Tête',
    description: '1 joueur par équipe',
    playersPerTeam: 1,
    icon: '👤'
  },
  {
    id: 'doublette',
    name: 'Doublette',
    description: '2 joueurs par équipe',
    playersPerTeam: 2,
    icon: '👥'
  },
  {
    id: 'triplette',
    name: 'Triplette',
    description: '3 joueurs par équipe',
    playersPerTeam: 3,
    icon: '👥👤'
  },
  {
    id: 'quadrette',
    name: 'Quadrette',
    description: '4 joueurs par équipe',
    playersPerTeam: 4,
    icon: '👥👥'
  },
  {
    id: 'sextette',
    name: 'Sextette',
    description: '6 joueurs par équipe',
    playersPerTeam: 6,
    icon: '👥👥👥'
  },
  {
    id: 'poule-4-doublette',
    name: 'Poule de 4 en Doublette',
    description: '4 équipes de 2 joueurs en poule',
    playersPerTeam: 2,
    icon: '🔄👥'
  },
  {
    id: 'poule-4-triplette',
    name: 'Poule de 4 en Triplette',
    description: '4 équipes de 3 joueurs en poule',
    playersPerTeam: 3,
    icon: '🔄👥👤'
  }
];