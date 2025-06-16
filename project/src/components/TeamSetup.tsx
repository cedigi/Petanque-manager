import React, { useState } from 'react';
import { Plus, Users, Trash2, ArrowLeft } from 'lucide-react';
import { Team, TournamentType } from '../types';
import { generateId } from '../utils/tournamentLogic';

interface TeamSetupProps {
  tournamentType: TournamentType;
  teams: Team[];
  onTeamsChange: (teams: Team[]) => void;
  onStartTournament: () => void;
  onBack: () => void;
  canStart: boolean;
}

export default function TeamSetup({ 
  tournamentType, 
  teams, 
  onTeamsChange, 
  onStartTournament, 
  onBack,
  canStart 
}: TeamSetupProps) {
  const [newPlayers, setNewPlayers] = useState<string[]>(
    Array(tournamentType.playersPerTeam).fill('')
  );

  const addTeam = () => {
    if (newPlayers.some(p => p.trim())) {
      const team: Team = {
        id: generateId(),
        players: newPlayers.filter(p => p.trim()).map(p => p.trim()),
        createdAt: new Date()
      };
      onTeamsChange([...teams, team]);
      setNewPlayers(Array(tournamentType.playersPerTeam).fill(''));
    }
  };

  const removeTeam = (teamId: string) => {
    onTeamsChange(teams.filter(team => team.id !== teamId));
  };

  const updatePlayer = (index: number, value: string) => {
    const updated = [...newPlayers];
    updated[index] = value;
    setNewPlayers(updated);
  };

  const getTeamDisplayName = (team: Team, index: number) => {
    return `Équipe ${index + 1}`;
  };

  const getPlayerLabel = (index: number) => {
    if (tournamentType.playersPerTeam === 3) {
      const roles = ['Pointeur', 'Milieu', 'Tireur'];
      return roles[index] || `Joueur ${index + 1}`;
    }
    return `Joueur ${index + 1}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <button
              onClick={onBack}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft size={24} />
            </button>
            <Users className="text-amber-600" size={36} />
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Configuration des Équipes</h1>
              <p className="text-gray-600">Tournoi {tournamentType.name} - {tournamentType.description}</p>
            </div>
          </div>
        </div>
      </header>

      <main className="py-8">
        <div className="max-w-4xl mx-auto p-6">
          <div className="bg-white rounded-xl shadow-lg p-8">
            {/* Info du type de tournoi */}
            <div className="bg-amber-50 rounded-lg p-4 mb-8 border border-amber-200">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{tournamentType.icon}</span>
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{tournamentType.name}</h3>
                  <p className="text-gray-600">{tournamentType.description}</p>
                </div>
              </div>
            </div>

            {/* Formulaire d'ajout d'équipe */}
            <div className="bg-amber-50 rounded-lg p-6 mb-8">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Ajouter une équipe</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Joueurs de l'équipe
                  </label>
                  <div className="grid gap-3">
                    {newPlayers.map((player, index) => (
                      <input
                        key={index}
                        type="text"
                        value={player}
                        onChange={(e) => updatePlayer(index, e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                        placeholder={`${getPlayerLabel(index)} ${index < Math.min(2, tournamentType.playersPerTeam) ? '*' : ''}`}
                      />
                    ))}
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    * Champs obligatoires (minimum {Math.min(2, tournamentType.playersPerTeam)} joueur{Math.min(2, tournamentType.playersPerTeam) > 1 ? 's' : ''})
                  </p>
                </div>

                <button
                  onClick={addTeam}
                  disabled={!newPlayers.some(p => p.trim())}
                  className="w-full bg-amber-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-amber-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                >
                  <Plus size={20} />
                  Ajouter l'équipe
                </button>
              </div>
            </div>

            {/* Liste des équipes */}
            {teams.length > 0 && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  Équipes inscrites ({teams.length})
                </h3>
                
                <div className="grid gap-4">
                  {teams.map((team, index) => (
                    <div key={team.id} className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-gray-800">{getTeamDisplayName(team, index)}</h4>
                        <p className="text-sm text-gray-600">
                          {team.players.join(' • ')}
                        </p>
                      </div>
                      <button
                        onClick={() => removeTeam(team.id)}
                        className="text-red-500 hover:text-red-700 p-2 rounded-lg hover:bg-red-50 transition-colors"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Bouton de démarrage */}
            <div className="pt-6 border-t">
              <button
                onClick={onStartTournament}
                disabled={!canStart}
                className="w-full bg-green-600 text-white py-4 px-8 rounded-lg font-bold text-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {canStart 
                  ? `Commencer le tournoi (${teams.length} équipes)`
                  : 'Minimum 2 équipes requises'
                }
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
