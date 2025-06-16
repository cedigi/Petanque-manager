import React from 'react';
import { Target, Users, ArrowRight } from 'lucide-react';
import { TournamentType, TOURNAMENT_TYPES } from '../types';

interface TournamentTypeSelectorProps {
  onTypeSelect: (type: TournamentType) => void;
}

export default function TournamentTypeSelector({ onTypeSelect }: TournamentTypeSelectorProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-sky-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <Target className="text-orange-600" size={36} />
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Gestionnaire de Tournois de Pétanque</h1>
              <p className="text-gray-600">Choisissez le type de tournoi à organiser</p>
            </div>
          </div>
        </div>
      </header>

      <main className="py-12">
        <div className="max-w-6xl mx-auto p-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Type de Tournoi</h2>
            <p className="text-xl text-gray-600">Sélectionnez la modalité de jeu pour votre tournoi</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {TOURNAMENT_TYPES.map((type) => (
              <div
                key={type.id}
                onClick={() => onTypeSelect(type)}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-2 border-2 border-transparent hover:border-orange-300 group"
              >
                <div className="p-8 text-center">
                  <div className="text-6xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    {type.icon}
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-800 mb-3 group-hover:text-orange-600 transition-colors">
                    {type.name}
                  </h3>
                  
                  <p className="text-gray-600 mb-6 text-lg">
                    {type.description}
                  </p>

                  <div className="flex items-center justify-center gap-2 text-orange-600 font-semibold group-hover:gap-4 transition-all">
                    <Users size={20} />
                    <span>{type.playersPerTeam} joueur{type.playersPerTeam > 1 ? 's' : ''}</span>
                    <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>

                <div className="bg-gradient-to-r from-orange-500 to-sky-500 h-2 rounded-b-xl transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>
              </div>
            ))}
          </div>

          <div className="mt-16 bg-white rounded-xl shadow-lg p-8">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Informations sur les Types de Tournois</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
                <div className="space-y-3">
                  <h4 className="font-semibold text-orange-600 text-lg">Tournois Classiques</h4>
                  <ul className="space-y-2 text-gray-600">
                    <li><strong>Tête à Tête:</strong> Jeu individuel, idéal pour les compétitions rapides</li>
                    <li><strong>Doublette:</strong> Format le plus populaire avec 2 joueurs par équipe</li>
                    <li><strong>Triplette:</strong> Format traditionnel avec pointeur, milieu et tireur</li>
                    <li><strong>Quadrette:</strong> Format pour grandes équipes</li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="font-semibold text-orange-600 text-lg">Formats Spéciaux</h4>
                  <ul className="space-y-2 text-gray-600">
                    <li><strong>Sextette:</strong> Format pour très grandes équipes</li>
                    <li><strong>Poules de 4:</strong> Système de poules avec matchs aller-retour</li>
                    <li>Chaque format adapte automatiquement le système de matchmaking</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}