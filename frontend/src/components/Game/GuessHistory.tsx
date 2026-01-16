import type { GuessRecord } from '../../types/game';

interface GuessHistoryProps {
  guesses: GuessRecord[];
}

export default function GuessHistory({ guesses }: GuessHistoryProps) {
  if (guesses.length === 0) {
    return (
      <div className="text-gray-500 text-center py-8">
        No guesses yet. Start by entering a 4-digit number!
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <h3 className="text-lg font-semibold mb-4">Guess History</h3>
      <div className="space-y-2">
        {guesses.map((guess, index) => (
          <div
            key={index}
            className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg"
          >
            <span className="text-gray-500 font-mono w-8">#{index + 1}</span>
            <span className="text-2xl font-mono tracking-widest font-bold">
              {guess.guess}
            </span>
            <div className="flex gap-2 ml-auto">
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                {guess.exact} exact
              </span>
              <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold">
                {guess.wrong_pos} wrong pos
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
