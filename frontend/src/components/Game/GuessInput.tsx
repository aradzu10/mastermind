import { useGameStore } from '../../store/gameStore';

export default function GuessInput() {
  const { currentGuess, setCurrentGuess, makeGuess, game, loading } = useGameStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentGuess.length === 4 && !game?.won) {
      makeGuess(currentGuess);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentGuess(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4 items-center">
      <input
        type="text"
        value={currentGuess}
        onChange={handleChange}
        placeholder="Enter 4 digits"
        maxLength={4}
        pattern="[0-9]{4}"
        className="px-4 py-2 text-2xl tracking-widest border-2 border-gray-300 rounded-lg
                   focus:outline-none focus:border-blue-500 text-center w-48
                   disabled:bg-gray-100 disabled:cursor-not-allowed"
        disabled={loading || game?.won || !game}
      />
      <button
        type="submit"
        disabled={currentGuess.length !== 4 || loading || game?.won || !game}
        className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold
                   hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                   transition-colors"
      >
        {loading ? 'Submitting...' : 'Guess'}
      </button>
    </form>
  );
}
