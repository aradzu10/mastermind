import { useState } from 'react';
import type { GameMode } from '../../types/game';

interface GameModeSelectorProps {
  onStartGame: (mode: GameMode, playerSecret?: string) => void;
}

export function GameModeSelector({ onStartGame }: GameModeSelectorProps) {
  const [selectedMode, setSelectedMode] = useState<GameMode>('single');
  const [useCustomSecret, setUseCustomSecret] = useState(false);
  const [playerSecret, setPlayerSecret] = useState('');
  const [error, setError] = useState('');

  const handleStartGame = () => {
    if (selectedMode === 'ai' && useCustomSecret) {
      if (playerSecret.length !== 4 || !/^\d{4}$/.test(playerSecret)) {
        setError('Please enter a valid 4-digit code');
        return;
      }
      onStartGame(selectedMode, playerSecret);
    } else {
      onStartGame(selectedMode);
    }
  };

  const handleSecretChange = (value: string) => {
    if (value.length <= 4 && /^\d*$/.test(value)) {
      setPlayerSecret(value);
      setError('');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
        <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Mastermind
        </h1>
        <p className="text-center text-gray-600 mb-8">Choose your game mode</p>

        <div className="space-y-4 mb-6">
          {/* Single Player Mode */}
          <button
            onClick={() => {
              setSelectedMode('single');
              setUseCustomSecret(false);
            }}
            className={`w-full p-4 rounded-xl border-2 transition-all ${
              selectedMode === 'single'
                ? 'border-indigo-600 bg-indigo-50 shadow-md'
                : 'border-gray-200 hover:border-indigo-300'
            }`}
          >
            <div className="flex items-start">
              <div className="flex-1 text-left">
                <h3 className="font-bold text-lg text-gray-800">Single Player</h3>
                <p className="text-sm text-gray-600">Guess the computer's secret code</p>
              </div>
              <div className="text-3xl">🎯</div>
            </div>
          </button>

          {/* AI Opponent Mode */}
          <button
            onClick={() => {
              setSelectedMode('ai');
            }}
            className={`w-full p-4 rounded-xl border-2 transition-all ${
              selectedMode === 'ai'
                ? 'border-purple-600 bg-purple-50 shadow-md'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="flex items-start">
              <div className="flex-1 text-left">
                <h3 className="font-bold text-lg text-gray-800">vs AI Opponent</h3>
                <p className="text-sm text-gray-600">Race against an AI to crack codes</p>
              </div>
              <div className="text-3xl">🤖</div>
            </div>
          </button>

          {/* AI Secret Setter (only shown if AI mode selected) */}
          {selectedMode === 'ai' && (
            <div className="ml-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
              <label className="flex items-center space-x-2 mb-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={useCustomSecret}
                  onChange={(e) => {
                    setUseCustomSecret(e.target.checked);
                    setPlayerSecret('');
                    setError('');
                  }}
                  className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Set my own secret code
                </span>
              </label>

              {useCustomSecret && (
                <div>
                  <input
                    type="text"
                    value={playerSecret}
                    onChange={(e) => handleSecretChange(e.target.value)}
                    placeholder="Enter 4 digits"
                    maxLength={4}
                    className="w-full px-4 py-2 text-2xl text-center tracking-widest border-2 border-purple-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 font-mono"
                  />
                  {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
                  <p className="text-xs text-gray-500 mt-2">
                    AI will try to guess your code
                  </p>
                </div>
              )}

              {!useCustomSecret && (
                <p className="text-xs text-gray-500">
                  A random code will be generated for you
                </p>
              )}
            </div>
          )}

          {/* PvP Mode (Coming Soon) */}
          <button
            disabled
            className="w-full p-4 rounded-xl border-2 border-gray-200 bg-gray-50 opacity-60 cursor-not-allowed"
          >
            <div className="flex items-start">
              <div className="flex-1 text-left">
                <h3 className="font-bold text-lg text-gray-800">Player vs Player</h3>
                <p className="text-sm text-gray-600">Coming soon!</p>
              </div>
              <div className="text-3xl">👥</div>
            </div>
          </button>
        </div>

        {/* Start Game Button */}
        <button
          onClick={handleStartGame}
          className="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all hover:scale-105"
        >
          Start Game
        </button>

        {/* How to Play */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-semibold text-gray-800 mb-2">How to Play:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Guess the 4-digit secret code</li>
            <li>• 🎯 <span className="font-medium">Exact</span> = correct digit in correct position</li>
            <li>• 🔄 <span className="font-medium">Wrong Pos</span> = correct digit in wrong position</li>
            <li>• In AI mode, you both race to crack each other's code!</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
