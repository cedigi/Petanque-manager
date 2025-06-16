import { Team, Match, TeamStats } from '../types';

export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}

export function calculateTeamStats(team: Team, matches: Match[]): TeamStats {
  const teamMatches = matches.filter(
    match => match.completed && (match.team1.id === team.id || match.team2.id === team.id)
  );

  let wins = 0;
  let losses = 0;
  let totalPointsFor = 0;
  let totalPointsAgainst = 0;

  teamMatches.forEach(match => {
    const isTeam1 = match.team1.id === team.id;
    const teamScore = isTeam1 ? match.score1! : match.score2!;
    const opponentScore = isTeam1 ? match.score2! : match.score1!;

    totalPointsFor += teamScore;
    totalPointsAgainst += opponentScore;

    if (teamScore > opponentScore) {
      wins++;
    } else {
      losses++;
    }
  });

  return {
    team,
    matchesPlayed: teamMatches.length,
    wins,
    losses,
    totalPointsFor,
    totalPointsAgainst,
    pointsDifference: totalPointsFor - totalPointsAgainst,
    winRate: teamMatches.length > 0 ? wins / teamMatches.length : 0
  };
}

export function getTeamRankings(teams: Team[], matches: Match[]): TeamStats[] {
  const stats = teams.map(team => calculateTeamStats(team, matches));
  
  return stats.sort((a, b) => {
    // Trier par taux de victoire, puis par différence de points
    if (a.winRate !== b.winRate) {
      return b.winRate - a.winRate;
    }
    if (a.pointsDifference !== b.pointsDifference) {
      return b.pointsDifference - a.pointsDifference;
    }
    return b.totalPointsFor - a.totalPointsFor;
  });
}

export function generateNextMatches(teams: Team[], existingMatches: Match[], round: number): Match[] {
  const rankings = getTeamRankings(teams, existingMatches);
  const newMatches: Match[] = [];
  const availableTeams = [...rankings];

  // Éviter les rematches récents
  const getRecentOpponents = (teamId: string): string[] => {
    return existingMatches
      .filter(match => match.completed && (match.team1.id === teamId || match.team2.id === teamId))
      .slice(-2) // Derniers 2 matchs
      .map(match => match.team1.id === teamId ? match.team2.id : match.team1.id);
  };

  while (availableTeams.length >= 2) {
    const team1Stats = availableTeams.shift()!;
    const team1RecentOpponents = getRecentOpponents(team1Stats.team.id);
    
    // Trouver le meilleur adversaire possible
    let bestMatchIndex = -1;
    let bestScoreDifference = Infinity;

    for (let i = 0; i < availableTeams.length; i++) {
      const team2Stats = availableTeams[i];
      
      // Éviter les rematches récents
      if (team1RecentOpponents.includes(team2Stats.team.id)) {
        continue;
      }

      // Calculer la différence de performance
      const scoreDifference = Math.abs(team1Stats.pointsDifference - team2Stats.pointsDifference);
      
      if (scoreDifference < bestScoreDifference) {
        bestScoreDifference = scoreDifference;
        bestMatchIndex = i;
      }
    }

    // Si aucun adversaire optimal, prendre le premier disponible
    if (bestMatchIndex === -1 && availableTeams.length > 0) {
      bestMatchIndex = 0;
    }

    if (bestMatchIndex !== -1) {
      const team2Stats = availableTeams.splice(bestMatchIndex, 1)[0];
      
      newMatches.push({
        id: generateId(),
        team1: team1Stats.team,
        team2: team2Stats.team,
        round,
        completed: false,
        createdAt: new Date()
      });
    }
  }

  return newMatches;
}

export function canStartTournament(teams: Team[]): boolean {
  return teams.length >= 2 && teams.every(team => team.players.length > 0);
}

export function isRoundComplete(matches: Match[], round: number): boolean {
  const roundMatches = matches.filter(match => match.round === round);
  return roundMatches.length > 0 && roundMatches.every(match => match.completed);
}
