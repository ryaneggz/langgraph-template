import { Link } from 'react-router-dom';

export default function Chat() {
    return (
        <main>
            <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
                ← Back to Dashboard
            </Link>
            <h1>Chat</h1>
            {/* Chat interface will go here */}
        </main>
    );
} 