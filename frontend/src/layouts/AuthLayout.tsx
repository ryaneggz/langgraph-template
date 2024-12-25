import { ColorModeButton } from '@/components/buttons/ColorModeButton';
import { Link, useNavigate } from 'react-router-dom';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('auth');
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Thread Agents</h1>
            <nav className="flex items-center space-x-4">
              <Link to="/dashboard" className="text-gray-600 hover:text-gray-900 transition-colors">
                Dashboard
              </Link>
              <Link to="/chat" className="text-gray-600 hover:text-gray-900 transition-colors">
                Chat
              </Link>
              <Link to="/settings" className="text-gray-600 hover:text-gray-900 transition-colors">
                Settings
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Logout
              </button>
              <ColorModeButton />
            </nav>
          </div>
        </div>
      </header>

      {children}

      <footer className="mt-auto bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-gray-500 text-sm">
            &copy; 2024 Thread Agents. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
