import { Link, useNavigate } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout';

export default function Dashboard() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <AuthLayout>
            <main>
                <div className="flex justify-between items-center">
                    <h1>Welcome to Your Dashboard</h1>
                    <button onClick={handleLogout}>Logout</button>
                </div>
                <nav>
                    <Link to="/chat">Chat</Link>
                    <Link to="/settings">Settings</Link>
                </nav>
            </main>
        </AuthLayout>
    );
}