import ChatLayout from '../layouts/ChatLayout';
import { useChatContext } from '../context/ChatContext';
import MarkdownCard from '../components/cards/MarkdownCard';

export default function Chat() {
    const { messages, payload, handleQuery, setPayload } = useChatContext();

    return (
        <ChatLayout>
            <div className="flex flex-col h-screen mx-0 pb-3"  style={{ maxHeight: 'calc(100vh - 65px)' }}>
                <div className="flex-1 overflow-y-auto space-y-4 p-3">
                    {messages?.map((message: {role: string, content: string}, index: number) => {
                        if (message.role === 'user' || message.role === 'human') {
                            return (
                                <div key={index} className="max-w-[80%] md:max-w-[50%] lg:max-w-[40%] bg-blue-600 text-white p-3 rounded-lg rounded-br-sm ml-auto">
                                    <MarkdownCard content={message.content} />
                                </div>
                            )
                        } else {
                            return (
                                <div key={index} className="max-w-[90%] bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-sm self-start">
                                    <MarkdownCard content={message.content} />
                                </div>
                            )
                        }
                    })}
                </div>

                <div className="flex gap-3 border-t border-gray-200 pt-4 px-3">
                    <textarea 
                        className="flex-1 resize-none min-h-[44px] max-h-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Type your message here..."
                        rows={1}
                        value={payload.query}
                        onChange={(e) => setPayload({ ...payload, query: e.target.value })}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleQuery();
                            }
                        }}
                    ></textarea>
                    <button 
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" 
                        onClick={handleQuery}
                    >
                        Send
                    </button>
                </div>
            </div>
        </ChatLayout>
    );
} 