import type { GuessRecord } from '../../types/game';

interface GuessHistoryProps {
  guesses: GuessRecord[];
  title?: string;
  isOpponent?: boolean;
}

export default function GuessHistory({ guesses, title = "Guess History", isOpponent = false }: GuessHistoryProps) {
  if (guesses.length === 0) {
    return (
      <div className="space-y-2">
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        <div className="text-gray-500 text-center py-8 bg-gray-50 rounded-lg">
          {"No guesses yet"}
        </div>
      </div>
    );
  }

  const colorScheme = isOpponent 
    ? { bg: 'bg-purple-50', exact: 'bg-green-100 text-green-800', wrongPos: 'bg-yellow-100 text-yellow-800' }
    : { bg: 'bg-indigo-50', exact: 'bg-green-100 text-green-800', wrongPos: 'bg-yellow-100 text-yellow-800' };

  return (
    <div className="space-y-2">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {guesses.map((guess, index) => (
          <div
            key={index}
            className={`flex items-center gap-4 p-3 ${colorScheme.bg} rounded-lg border ${isOpponent ? 'border-purple-200' : 'border-indigo-200'}`}
          >
            <span className="text-gray-500 font-mono w-8 text-sm">#{index + 1}</span>
            <span className="text-2xl font-mono tracking-widest font-bold">
              {guess.guess}
            </span>
            <div className="flex gap-2 ml-auto">
              <span className={`px-3 py-1 ${colorScheme.exact} rounded-full text-sm font-semibold flex items-center gap-1`}>
                🎯 {guess.exact}
              </span>
              <span className={`px-3 py-1 ${colorScheme.wrongPos} rounded-full text-sm font-semibold flex items-center gap-1`}>
                🔄 {guess.wrong_pos}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
