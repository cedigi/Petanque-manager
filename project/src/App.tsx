import React, { useState, useEffect } from 'react';
import { Target, RotateCcw, Trophy } from 'lucide-react';
import { Tournament, Team, Match, TournamentType } from './types';
import { generateId, canStartTournament, generateNextMatches, isRoundComplete } from './utils/tournamentLogic';
import TournamentTypeSelector from './components/TournamentTypeSelector';
import TeamSetup from './components/TeamSetup';
import TournamentView from './components/TournamentView';

type AppState = 'type-selection' | 'team-setup' | 'tournament';

function App() {
  const [appState, setAppState] = useState<AppState>('type-selection');
  const [selectedType, setSelectedType] = useState<TournamentType | null>(null);
  const [tournament, setTournament] = useState<Tournament | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [darkMode, setDarkMode] = useState(false);

  // Sauvegarder l'état dans le localStorage
  useEffect(() => {
    const saved = localStorage.getItem('petanque-tournament');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        if (data.tournament) {
          setTournament({
            ...data.tournament,
            createdAt: new Date(data.tournament.createdAt),
            completedAt: data.tournament.completedAt ? new Date(data.tournament.completedAt) : undefined,
            teams: data.tournament.teams.map((team: any) => ({
              ...team,
              createdAt: new Date(team.createdAt)
            })),
            matches: data.tournament.matches.map((match: any) => ({
              ...match,
              createdAt: new Date(match.createdAt),
              terrain: match.terrain,
              bye: match.bye,
              completedAt: match.completedAt ? new Date(match.completedAt) : undefined
            }))
          });
          setAppState('tournament');
        } else if (data.teams && data.selectedType) {
          setTeams(data.teams.map((team: any) => ({
            ...team,
            createdAt: new Date(team.createdAt)
          })));
          setSelectedType(data.selectedType);
          setAppState('team-setup');
        }
      } catch (error) {
        console.error('Erreur lors du chargement:', error);
      }
    }
  }, []);

  useEffect(() => {
    const savedMode = localStorage.getItem('dark-mode');
    if (savedMode) {
      setDarkMode(JSON.parse(savedMode));
    }
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('dark-mode', JSON.stringify(darkMode));
  }, [darkMode]);

  useEffect(() => {
    if (appState === 'tournament' && tournament) {
      localStorage.setItem('petanque-tournament', JSON.stringify({ tournament }));
    } else if (appState === 'team-setup' && selectedType) {
      localStorage.setItem('petanque-tournament', JSON.stringify({ teams, selectedType }));
    }
  }, [tournament, teams, selectedType, appState]);

  const handleTypeSelect = (type: TournamentType) => {
    setSelectedType(type);
    setAppState('team-setup');
  };

  const DarkModeButton = () => (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="fixed top-4 right-4 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded"
    >
      {darkMode ? 'Mode clair' : 'Mode sombre'}
    </button>
  );

  const startTournament = () => {
    if (!canStartTournament(teams) || !selectedType) return;

    const initialMatches = generateNextMatches(teams, [], 1);
    
    const newTournament: Tournament = {
      id: generateId(),
      name: `Tournoi ${selectedType.name} du ${new Date().toLocaleDateString('fr-FR')}`,
      type: selectedType,
      teams,
      matches: initialMatches,
      currentRound: 1,
      status: 'active',
      createdAt: new Date()
    };

    setTournament(newTournament);
    setTeams([]);
    setAppState('tournament');
  };

  const updateScore = (matchId: string, score1: number, score2: number) => {
    if (!tournament) return;

    const updatedMatches = tournament.matches.map(match => {
      if (match.id === matchId) {
        return {
          ...match,
          score1,
          score2,
          completed: true,
          completedAt: new Date()
        };
      }
      return match;
    });

    setTournament({
      ...tournament,
      matches: updatedMatches
    });
  };

  const advanceToNextRound = () => {
    if (!tournament) return;

    const nextRound = tournament.currentRound + 1;
    const newMatches = generateNextMatches(tournament.teams, tournament.matches, nextRound);
    
    if (newMatches.length === 0) {
      // Tournoi terminé
      setTournament({
        ...tournament,
        status: 'completed',
        completedAt: new Date()
      });
      return;
    }

    setTournament({
      ...tournament,
      currentRound: nextRound,
      matches: [...tournament.matches, ...newMatches]
    });
  };

  const resetTournament = () => {
    setTournament(null);
    setTeams([]);
    setSelectedType(null);
    setAppState('type-selection');
    localStorage.removeItem('petanque-tournament');
  };

  const backToTypeSelection = () => {
    setTeams([]);
    setSelectedType(null);
    setAppState('type-selection');
    localStorage.removeItem('petanque-tournament');
  };

  const canAdvanceRound = tournament ? isRoundComplete(tournament.matches, tournament.currentRound) : false;

  if (appState === 'type-selection') {
    return (
      <>
        <DarkModeButton />
        <TournamentTypeSelector onTypeSelect={handleTypeSelect} />
      </>
    );
  }

  if (appState === 'team-setup' && selectedType) {
    return (
      <>
        <DarkModeButton />
        <TeamSetup
          tournamentType={selectedType}
          teams={teams}
          onTeamsChange={setTeams}
          onStartTournament={startTournament}
          onBack={backToTypeSelection}
          canStart={canStartTournament(teams)}
        />
      </>
    );
  }

  if (appState === 'tournament' && tournament) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-sky-100 dark:from-gray-800 dark:to-gray-900">
        <DarkModeButton />
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-lg">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Trophy className="text-orange-600" size={36} />
                <div>
                  <h1 className="text-2xl font-bold text-gray-800">{tournament.name}</h1>
                  <p className="text-gray-600">
                    {tournament.status === 'completed' ? 'Tournoi terminé' : 'Tournoi en cours'}
                  </p>
                </div>
              </div>
              
              <button
                onClick={resetTournament}
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <RotateCcw size={20} />
                Nouveau tournoi
              </button>
            </div>
          </div>
        </header>

        <main className="py-8">
          <TournamentView
            tournament={tournament}
            onScoreUpdate={updateScore}
            onNextRound={advanceToNextRound}
            canAdvanceRound={canAdvanceRound}
          />
        </main>
      </div>
    );
  }

  return null;
}

export default App;