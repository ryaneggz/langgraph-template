import { Link } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout';

export default function Settings() {
    return (
        <AuthLayout>
            <main className="max-w-4xl mx-auto p-6">
                <div className="mb-8">
                    <Link 
                        to="/dashboard" 
                        className="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors"
                    >
                        <svg 
                            xmlns="http://www.w3.org/2000/svg" 
                            className="h-5 w-5 mr-2" 
                            viewBox="0 0 20 20" 
                            fill="currentColor"
                        >
                            <path 
                                fillRule="evenodd" 
                                d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" 
                                clipRule="evenodd" 
                            />
                        </svg>
                        Back to Dashboard
                    </Link>
                </div>

                <div className="bg-card text-card-foreground rounded-lg shadow-md p-6">
                    <h1 className="text-2xl font-bold text-foreground mb-6">Settings</h1>
                    
                    <div className="space-y-6">
                        {/* Profile Section */}
                        <section className="border-b border-border pb-6">
                            <h2 className="text-lg font-semibold text-foreground mb-4">Profile Settings</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-foreground mb-1">
                                        Display Name
                                    </label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 bg-background border border-input rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                                        placeholder="Your display name"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-foreground mb-1">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        className="w-full px-3 py-2 bg-background border border-input rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                                        placeholder="your.email@example.com"
                                    />
                                </div>
                            </div>
                        </section>

                        {/* Preferences Section */}
                        <section className="border-b border-border pb-6">
                            <h2 className="text-lg font-semibold text-foreground mb-4">Preferences</h2>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <label className="font-medium text-foreground">Email Notifications</label>
                                        <p className="text-sm text-muted-foreground">Receive email updates about your account</p>
                                    </div>
                                    <button 
                                        className="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-primary/50"
                                    >
                                        <span className="translate-x-0 inline-block h-5 w-5 transform rounded-full bg-background shadow transition duration-200 ease-in-out"></span>
                                    </button>
                                </div>
                            </div>
                        </section>

                        {/* Save Button */}
                        <div className="flex justify-end pt-4">
                            <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </AuthLayout>
    );
} 