import { Link } from 'react-router-dom';

export default function Settings() {
    return (
        <main>
            <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
                ← Back to Dashboard
            </Link>
            <h1>Settings</h1>
            {/* Settings interface will go here */}
        </main>
    );
} 