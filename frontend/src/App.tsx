import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import GameBoard from './components/Game/GameBoard';
import { LoginPage } from './components/Auth/LoginPage';
import { ProtectedRoute } from './components/Auth/ProtectedRoute';
import { useAuthStore } from './store/authStore';

function App() {
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/game"
          element={
            <ProtectedRoute>
              <GameBoard />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/game" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
