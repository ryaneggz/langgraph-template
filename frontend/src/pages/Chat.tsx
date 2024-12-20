import ChatLayout from '../layouts/ChatLayout';
import { Link } from 'react-router-dom';

export default function Chat() {
    return (
        <ChatLayout>
            <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
                ← Back to Dashboard
            </Link>

            <div className="chat-history">
                <div className="message ai-message">
                    Hello! How can I help you today?
                </div>
                <div className="message user-message">
                    Can you help me with a coding problem?
                </div>
                <div className="message ai-message">
                    Of course! Please describe the problem you're facing and I'll do my best to assist you.
                </div>
            </div>

            <div className="input-container">
                <textarea 
                    className="message-input" 
                    placeholder="Type your message here..."
                    rows={1}
                ></textarea>
                <button className="send-button">Send</button>
            </div>
        </ChatLayout>
    );
} 