import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NoAuthLayout from '../layouts/NoAuthLayout';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (username === 'admin' && password === 'test1234') {
            localStorage.setItem('token', 'dummy-token');
            navigate('/dashboard');
        } else {
            setError('Invalid credentials');
        }
    };

    return (
        <NoAuthLayout>
            <main className="flex min-h-screen flex-col items-center justify-center">
                <form onSubmit={handleLogin} className="space-y-4">
                    <h1>Login</h1>
                    {error && <div className="text-red-500">{error}</div>}
                    <div>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit">Login</button>
                </form>
            </main>
        </NoAuthLayout>
    );
}
