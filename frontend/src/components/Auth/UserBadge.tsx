import { useAuthStore } from '../../store/authStore';
import { useNavigate } from 'react-router-dom';

export function UserBadge() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  return (
    <div className="flex items-center gap-4">
      <div className="text-right">
        <div className="font-medium text-gray-800">{user.display_name}</div>
        <div className="text-sm text-gray-500">
          {user.is_guest ? 'Guest' : 'User'} • ELO: {user.elo_rating}
        </div>
      </div>
      <button
        onClick={handleLogout}
        className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
      >
        Logout
      </button>
    </div>
  );
}
