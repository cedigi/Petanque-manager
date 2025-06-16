import React from 'react';
import { Trophy, Medal, Award, TrendingUp } from 'lucide-react';
import { Tournament, TeamStats } from '../types';
import { getTeamRankings } from '../utils/tournamentLogic';
import MatchCard from './MatchCard';

interface TournamentViewProps {
  tournament: Tournament;
  onScoreUpdate: (matchId: string, score1: number, score2: number) => void;
  onNextRound: () => void;
  canAdvanceRound: boolean;
}

export default function TournamentView({ tournament, onScoreUpdate, onNextRound, canAdvanceRound }: TournamentViewProps) {
  const rankings = getTeamRankings(tournament.teams, tournament.matches);
  const currentRoundMatches = tournament.matches.filter(match => match.round === tournament.currentRound);
  const completedMatches = tournament.matches.filter(match => match.completed);

  const getRankIcon = (index: number) => {
    switch (index) {
      case 0: return <Trophy className="text-yellow-500" size={20} />;
      case 1: return <Medal className="text-gray-400" size={20} />;
      case 2: return <Award className="text-amber-600" size={20} />;
      default: return <TrendingUp className="text-gray-400" size={16} />;
    }
  };

  const getTeamDisplayName = (team: any, index: number) => {
    return `Équipe ${index + 1}`;
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Classement */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-lg p-6 sticky top-6">
            <div className="flex items-center gap-3 mb-6">
              <Trophy className="text-amber-600" size={24} />
              <h2 className="text-2xl font-bold text-gray-800">Classement</h2>
            </div>

            <div className="space-y-3">
              {rankings.map((stats: TeamStats, index: number) => (
                <div key={stats.team.id} className={`p-4 rounded-lg border ${
                  index === 0 ? 'bg-yellow-50 border-yellow-200' :
                  index === 1 ? 'bg-gray-50 border-gray-200' :
                  index === 2 ? 'bg-amber-50 border-amber-200' :
                  'bg-white border-gray-100'
                }`}>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getRankIcon(index)}
                      <span className="font-bold text-gray-800">#{index + 1}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-600">
                        {stats.wins}V - {stats.losses}D
                      </div>
                      <div className="text-xs text-gray-500">
                        {Math.round(stats.winRate * 100)}% victoires
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="font-semibold text-gray-800 mb-1">{getTeamDisplayName(stats.team, index)}</h3>
                  <p className="text-sm text-gray-600 mb-2">{stats.team.players.join(' • ')}</p>
                  
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Points: {stats.totalPointsFor} - {stats.totalPointsAgainst}</span>
                    <span className={`font-medium ${
                      stats.pointsDifference > 0 ? 'text-green-600' : 
                      stats.pointsDifference < 0 ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {stats.pointsDifference > 0 ? '+' : ''}{stats.pointsDifference}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* Statistiques du tournoi */}
            <div className="mt-6 pt-6 border-t">
              <h3 className="font-semibold text-gray-800 mb-3">Statistiques</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Type:</span>
                  <span className="font-medium">{tournament.type.name}</span>
                </div>
                <div className="flex justify-between">
                  <span>Round actuel:</span>
                  <span className="font-medium">{tournament.currentRound}</span>
                </div>
                <div className="flex justify-between">
                  <span>Matchs joués:</span>
                  <span className="font-medium">{completedMatches.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Équipes:</span>
                  <span className="font-medium">{tournament.teams.length}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Matchs */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              Round {tournament.currentRound}
            </h2>
            
            {canAdvanceRound && (
              <button
                onClick={onNextRound}
                className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors"
              >
                Round suivant
              </button>
            )}
          </div>

          {currentRoundMatches.length > 0 ? (
            <div className="space-y-6">
              {currentRoundMatches.map((match) => (
                <MatchCard
                  key={match.id}
                  match={match}
                  onScoreUpdate={onScoreUpdate}
                />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-lg p-8 text-center">
              <Trophy className="text-gray-400 mx-auto mb-4" size={48} />
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Tournoi terminé!</h3>
              <p className="text-gray-600">
                Félicitations à <strong>{getTeamDisplayName(rankings[0]?.team, 0)}</strong> pour la victoire!
              </p>
              <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
                <p className="text-sm text-gray-600">
                  Joueurs gagnants: <strong>{rankings[0]?.team.players.join(', ')}</strong>
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}