interface FreeGuessIndicatorProps {
  isOpponent?: boolean;
}

export default function FreeGuessIndicator({ isOpponent = false }: FreeGuessIndicatorProps) {
  const colorScheme = isOpponent
    ? 'bg-purple-100 text-purple-700 border-purple-300'
    : 'bg-indigo-100 text-indigo-700 border-indigo-300';

  return (
    <span className={`px-2 py-1 ${colorScheme} border rounded-full text-xs font-semibold flex items-center gap-1 whitespace-nowrap`}>
      🎁 Free Guess
    </span>
  );
}
