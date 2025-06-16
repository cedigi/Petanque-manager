import React, { useState, useEffect } from 'react';
import { Tournament, Team } from '../types';
import { getTeamRankings } from '../utils/tournamentLogic';

interface TournamentViewProps {
  tournament: Tournament;
  onScoreUpdate: (matchId: string, score1: number, score2: number) => void;
  onNextRound: () => void;
  canAdvanceRound: boolean;
}

export default function TournamentView({ tournament, onScoreUpdate, onNextRound, canAdvanceRound }: TournamentViewProps) {
  const [activeTab, setActiveTab] = useState<'teams' | 'matches' | 'results'>('teams');
  const [scores, setScores] = useState<Record<string, { s1: string; s2: string }>>({});
  const rounds = Array.from(new Set(tournament.matches.map(m => m.round))).sort((a, b) => a - b);
  const [activeRound, setActiveRound] = useState<number>(rounds[0] || 1);

  useEffect(() => {
    if (rounds.length > 0) {
      setActiveRound(rounds[rounds.length - 1]);
    }
  }, [rounds]);

  const rankings = getTeamRankings(tournament.teams, tournament.matches);

  const teamNumber = (team: Team) => tournament.teams.findIndex(t => t.id === team.id) + 1;

  const handleChange = (id: string, field: 's1' | 's2', value: string) => {
    setScores(prev => ({ ...prev, [id]: { s1: prev[id]?.s1 || '', s2: prev[id]?.s2 || '', [field]: value } }));
  };

  const handleSave = (matchId: string) => {
    const entry = scores[matchId];
    if (!entry) return;
    const s1 = parseInt(entry.s1);
    const s2 = parseInt(entry.s2);
    if (!isNaN(s1) && !isNaN(s2) && (s1 === 13 || s2 === 13) && s1 !== s2) {
      onScoreUpdate(matchId, s1, s2);
      setScores(prev => ({ ...prev, [matchId]: { s1: '', s2: '' } }));
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-6 flex gap-2">
        <button onClick={() => setActiveTab('teams')} className={`px-4 py-2 rounded ${activeTab === 'teams' ? 'bg-orange-600 text-white' : 'bg-gray-200'}`}>Équipes</button>
        <button onClick={() => setActiveTab('matches')} className={`px-4 py-2 rounded ${activeTab === 'matches' ? 'bg-orange-600 text-white' : 'bg-gray-200'}`}>Matchs</button>
        <button onClick={() => setActiveTab('results')} className={`px-4 py-2 rounded ${activeTab === 'results' ? 'bg-orange-600 text-white' : 'bg-gray-200'}`}>Résultats</button>
      </div>

      {activeTab === 'teams' && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-gray-300 p-6 max-w-3xl mx-auto">
          <div className="text-right mb-2">
            <button onClick={handlePrint} className="bg-blue-600 text-white px-3 py-1 rounded">Imprimer</button>
          </div>
          <table className="w-full text-center border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="p-2 border border-gray-300">#</th>
                <th className="p-2 border border-gray-300">Joueurs</th>
              </tr>
            </thead>
            <tbody>
              {tournament.teams.map((team, index) => (
                <tr key={team.id}>
                  <td className="p-2 border border-gray-300">{index + 1}</td>
                  <td className="p-2 border border-gray-300">{team.players.join(' • ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'matches' && (
        <>
          <div className="mb-4 flex items-center gap-2">
            {rounds.map(r => (
              <button
                key={r}
                onClick={() => setActiveRound(r)}
                className={`px-3 py-1 rounded ${activeRound === r ? 'bg-orange-600 text-white' : 'bg-gray-200'}`}
              >
                Tour {r}
              </button>
            ))}
            <button onClick={handlePrint} className="ml-auto bg-blue-600 text-white px-3 py-1 rounded">Imprimer</button>
          </div>
          <div className="bg-white rounded-xl shadow-lg border-2 border-gray-300 p-6 max-w-5xl mx-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Tour {activeRound}</h2>
              {activeRound === tournament.currentRound && canAdvanceRound && (
                <button onClick={onNextRound} className="bg-blue-600 text-white px-4 py-1 rounded">Tour suivant</button>
              )}
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left border-collapse border border-gray-300">
                <thead>
                  <tr>
                    <th className="p-2 border border-gray-300">Éq.</th>
                    <th className="p-2 border border-gray-300">Joueurs</th>
                    <th className="p-2 border border-gray-300">Score</th>
                    <th className="p-2 border border-gray-300">Score</th>
                    <th className="p-2 border border-gray-300">Adversaires</th>
                    <th className="p-2 border border-gray-300">Éq.</th>
                    <th className="p-2 border border-gray-300">Terrain</th>
                    <th className="p-2 border border-gray-300"></th>
                  </tr>
                </thead>
                <tbody>
                  {tournament.matches.filter(m => m.round === activeRound).map(match => {
                    const entry = scores[match.id] || { s1: match.score1?.toString() || '', s2: match.score2?.toString() || '' };
                    const editable = !match.completed && !match.bye && activeRound === tournament.currentRound;
                    const isBye = match.bye || match.team2.players[0] === 'BYE';
                    return (
                      <tr key={match.id}>
                        <td className="p-2 border border-gray-300">{teamNumber(match.team1)}</td>
                        <td className="p-2 border border-gray-300">{match.team1.players.join(' • ')}</td>
                        <td className="p-2 border border-gray-300">
                          {editable ? (
                            <input type="number" value={entry.s1} onChange={e => handleChange(match.id, 's1', e.target.value)} className="w-16 p-1 border rounded" />
                          ) : (
                            match.score1 ?? '-'
                          )}
                        </td>
                        <td className="p-2 border border-gray-300">
                          {editable ? (
                            <input type="number" value={entry.s2} onChange={e => handleChange(match.id, 's2', e.target.value)} className="w-16 p-1 border rounded" />
                          ) : (
                            match.score2 ?? '-'
                          )}
                        </td>
                        <td className="p-2 border border-gray-300">{isBye ? 'BYE' : match.team2.players.join(' • ')}</td>
                        <td className="p-2 border border-gray-300">{isBye ? '-' : teamNumber(match.team2)}</td>
                        <td className="p-2 border border-gray-300">{match.terrain}</td>
                        <td className="p-2 border border-gray-300">
                          {editable && (Number(entry.s1) === 13 || Number(entry.s2) === 13) && Number(entry.s1) !== Number(entry.s2) && (
                            <button onClick={() => handleSave(match.id)} className="bg-blue-600 text-white px-2 py-1 rounded">OK</button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {activeTab === 'results' && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-gray-300 p-6 max-w-3xl mx-auto">
          <div className="text-right mb-2">
            <button onClick={handlePrint} className="bg-blue-600 text-white px-3 py-1 rounded">Imprimer</button>
          </div>
          <table className="w-full text-center border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="p-2 border border-gray-300">#</th>
                <th className="p-2 border border-gray-300">Joueurs</th>
                <th className="p-2 border border-gray-300">Victoires</th>
                <th className="p-2 border border-gray-300">Diff.</th>
              </tr>
            </thead>
            <tbody>
              {rankings.map((stats, index) => (
                <tr key={stats.team.id}>
                  <td className="p-2 border border-gray-300">{teamNumber(stats.team)}</td>
                  <td className="p-2 border border-gray-300">{stats.team.players.join(' • ')}</td>
                  <td className="p-2 border border-gray-300">{stats.wins}</td>
                  <td className="p-2 border border-gray-300">{stats.pointsDifference > 0 ? '+' : ''}{stats.pointsDifference}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
