import React, { useState } from 'react';
import { Save, Trophy, Clock } from 'lucide-react';
import { Match } from '../types';

interface MatchCardProps {
  match: Match;
  onScoreUpdate: (matchId: string, score1: number, score2: number) => void;
}

export default function MatchCard({ match, onScoreUpdate }: MatchCardProps) {
  const [score1, setScore1] = useState(match.score1?.toString() || '');
  const [score2, setScore2] = useState(match.score2?.toString() || '');
  const [isEditing, setIsEditing] = useState(!match.completed);

  const handleSave = () => {
    const s1 = parseInt(score1);
    const s2 = parseInt(score2);
    
    if (!isNaN(s1) && !isNaN(s2) && s1 >= 0 && s2 >= 0 && (s1 === 13 || s2 === 13)) {
      onScoreUpdate(match.id, s1, s2);
      setIsEditing(false);
    }
  };

  const canSave = () => {
    const s1 = parseInt(score1);
    const s2 = parseInt(score2);
    return !isNaN(s1) && !isNaN(s2) && s1 >= 0 && s2 >= 0 && (s1 === 13 || s2 === 13) && s1 !== s2;
  };

  const getWinner = () => {
    if (!match.completed || match.score1 === undefined || match.score2 === undefined) return null;
    return match.score1 > match.score2 ? match.team1 : match.team2;
  };

  const getTeamDisplayName = (team: any, isTeam1: boolean) => {
    const teamNumber = isTeam1 ? 1 : 2;
    return `Équipe ${teamNumber}`;
  };

  const winner = getWinner();

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${
      match.completed 
        ? 'border-green-500 bg-green-50' 
        : 'border-amber-500 bg-amber-50'
    }`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {match.completed ? (
            <Trophy className="text-green-600" size={20} />
          ) : (
            <Clock className="text-amber-600" size={20} />
          )}
          <span className="text-sm font-medium text-gray-600">
            {match.completed ? 'Match terminé' : 'En cours'}
          </span>
        </div>
        <span className="text-sm text-gray-500">Round {match.round}</span>
      </div>

      <div className="space-y-4">
        {/* Équipe 1 */}
        <div className={`flex items-center justify-between p-3 rounded-lg ${
          winner?.id === match.team1.id ? 'bg-green-100 border border-green-300' : 'bg-gray-100'
        }`}>
          <div>
            <h3 className="font-semibold text-gray-800">{getTeamDisplayName(match.team1, true)}</h3>
            <p className="text-sm text-gray-600">{match.team1.players.join(' • ')}</p>
          </div>
          
          {isEditing ? (
            <input
              type="number"
              value={score1}
              onChange={(e) => setScore1(e.target.value)}
              min="0"
              max="13"
              className="w-16 px-2 py-1 text-center border rounded focus:ring-2 focus:ring-amber-500"
              placeholder="0"
            />
          ) : (
            <div className={`text-2xl font-bold ${
              winner?.id === match.team1.id ? 'text-green-600' : 'text-gray-700'
            }`}>
              {match.score1 ?? '-'}
            </div>
          )}
        </div>

        {/* VS */}
        <div className="text-center text-gray-400 font-bold">VS</div>

        {/* Équipe 2 */}
        <div className={`flex items-center justify-between p-3 rounded-lg ${
          winner?.id === match.team2.id ? 'bg-green-100 border border-green-300' : 'bg-gray-100'
        }`}>
          <div>
            <h3 className="font-semibold text-gray-800">{getTeamDisplayName(match.team2, false)}</h3>
            <p className="text-sm text-gray-600">{match.team2.players.join(' • ')}</p>
          </div>
          
          {isEditing ? (
            <input
              type="number"
              value={score2}
              onChange={(e) => setScore2(e.target.value)}
              min="0"
              max="13"
              className="w-16 px-2 py-1 text-center border rounded focus:ring-2 focus:ring-amber-500"
              placeholder="0"
            />
          ) : (
            <div className={`text-2xl font-bold ${
              winner?.id === match.team2.id ? 'text-green-600' : 'text-gray-700'
            }`}>
              {match.score2 ?? '-'}
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      {isEditing && (
        <div className="mt-4 pt-4 border-t">
          <button
            onClick={handleSave}
            disabled={!canSave()}
            className="w-full bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            <Save size={18} />
            Enregistrer le score
          </button>
          
          {!canSave() && (score1 || score2) && (
            <p className="text-sm text-red-600 mt-2 text-center">
              Un match de pétanque se joue en 13 points. Une équipe doit atteindre 13 points pour gagner.
            </p>
          )}
        </div>
      )}

      {match.completed && (
        <div className="mt-4 pt-4 border-t">
          <button
            onClick={() => setIsEditing(true)}
            className="text-sm text-amber-600 hover:text-amber-700 font-medium"
          >
            Modifier le score
          </button>
        </div>
      )}
    </div>
  );
}