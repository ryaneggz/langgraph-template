import { Link } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout';

export default function Dashboard() {

    return (
        <AuthLayout>
            <main className="max-w-6xl mx-auto p-6">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-foreground">Welcome to Your Dashboard</h1>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Link 
                        to="/chat" 
                        className="p-6 bg-card text-card-foreground rounded-lg shadow-md hover:shadow-lg transition-shadow border border-border"
                    >
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-primary/10 rounded-full">
                                <svg 
                                    xmlns="http://www.w3.org/2000/svg" 
                                    className="h-6 w-6 text-primary" 
                                    fill="none" 
                                    viewBox="0 0 24 24" 
                                    stroke="currentColor"
                                >
                                    <path 
                                        strokeLinecap="round" 
                                        strokeLinejoin="round" 
                                        strokeWidth={2} 
                                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" 
                                    />
                                </svg>
                            </div>
                            <div>
                                <h2 className="text-xl font-semibold text-foreground">Chat</h2>
                                <p className="text-muted-foreground">Start a conversation with our AI assistant</p>
                            </div>
                        </div>
                    </Link>

                    <Link 
                        to="/settings" 
                        className="p-6 bg-card text-card-foreground rounded-lg shadow-md hover:shadow-lg transition-shadow border border-border"
                    >
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-primary/10 rounded-full">
                                <svg 
                                    xmlns="http://www.w3.org/2000/svg" 
                                    className="h-6 w-6 text-primary" 
                                    fill="none" 
                                    viewBox="0 0 24 24" 
                                    stroke="currentColor"
                                >
                                    <path 
                                        strokeLinecap="round" 
                                        strokeLinejoin="round" 
                                        strokeWidth={2} 
                                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" 
                                    />
                                    <path 
                                        strokeLinecap="round" 
                                        strokeLinejoin="round" 
                                        strokeWidth={2} 
                                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" 
                                    />
                                </svg>
                            </div>
                            <div>
                                <h2 className="text-xl font-semibold text-foreground">Settings</h2>
                                <p className="text-muted-foreground">Configure your account preferences</p>
                            </div>
                        </div>
                    </Link>
                </div>
            </main>
        </AuthLayout>
    );
}