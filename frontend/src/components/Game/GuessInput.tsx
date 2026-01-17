import { useGameStore } from '../../store/gameStore';

interface GuessInputProps {
  disabled?: boolean;
}

export default function GuessInput({ disabled = false }: GuessInputProps) {
  const { currentGuess, setCurrentGuess, makeGuess, game, loading } = useGameStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentGuess.length === 4 && game?.winner_id === null && !disabled) {
      makeGuess(currentGuess);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentGuess(e.target.value);
  };

  const isDisabled = loading || game?.winner_id !== null || !game || disabled;

  return (
    <form onSubmit={handleSubmit} className="flex gap-4 items-center">
      <input
        type="text"
        value={currentGuess}
        onChange={handleChange}
        placeholder="Enter 4 digits"
        maxLength={4}
        pattern="[0-9]{4}"
        className="px-4 py-3 text-2xl tracking-widest border-2 border-indigo-300 rounded-lg
                   focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200
                   text-center w-full font-mono
                   disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
        disabled={isDisabled}
      />
      <button
        type="submit"
        disabled={currentGuess.length !== 4 || isDisabled}
        className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold
                   hover:shadow-lg disabled:bg-gray-300 disabled:cursor-not-allowed
                   transition-all hover:scale-105 whitespace-nowrap"
      >
        {loading ? 'Submitting...' : 'Guess'}
      </button>
    </form>
  );
}
