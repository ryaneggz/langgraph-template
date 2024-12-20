import ChatLayout from '../layouts/ChatLayout';
import { queryThread } from '../services/threadService';

const defaultThreadPayload = {
    images: [],
    query: 'What is the capital of Malaysia?',
    system: 'You are a helpful assistant.',
    tools: [],
    visualize: false
}

export default function Chat() {
    return (
        <ChatLayout>
            <div className="flex flex-col h-screen max-w-5xl mx-auto pb-3"  style={{ maxHeight: 'calc(100vh - 65px)' }}>
                <div className="flex-1 overflow-y-auto space-y-4 p-3">
                    <div className="max-w-[80%] bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-sm self-start">
                        Hello! How can I help you today?
                    </div>
                    <div className="max-w-[80%] bg-blue-600 text-white p-3 rounded-lg rounded-br-sm ml-auto">
                        Can you help me with a coding problem?
                    </div>
                    <div className="max-w-[80%] bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-sm self-start">
                        Of course! Please describe the problem you're facing and I'll do my best to assist you.
                    </div>
                </div>

                <div className="flex gap-3 border-t border-gray-200 pt-4 px-3">
                    <textarea 
                        className="flex-1 resize-none min-h-[44px] max-h-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Type your message here..."
                        rows={1}
                    ></textarea>
                    <button 
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" 
                        onClick={() => queryThread(defaultThreadPayload)}
                    >
                        Send
                    </button>
                </div>
            </div>
        </ChatLayout>
    );
} 