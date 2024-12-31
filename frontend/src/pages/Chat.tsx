import ChatLayout from '../layouts/ChatLayout';
import { useChatContext } from '../context/ChatContext';
import MarkdownCard from '../components/cards/MarkdownCard';
import { Button } from '@/components/ui/button';
import { ThreadHistoryDrawer } from '@/components/drawers/ThreadHistoryDrawer';
import { useEffect, useRef } from 'react';
import ChatNav from '@/components/nav/ChatNav';

export default function Chat() {
    const { messages, payload, handleQuery, setPayload, useGetHistoryEffect } = useChatContext();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]); // Scroll when messages change

    useGetHistoryEffect();

    return (
        <ChatLayout>
            <div className="flex min-h-[calc(100vh-0px)] max-h-[calc(100vh-0px)] relative">
                <ThreadHistoryDrawer />
                
                <div className="flex-1 flex flex-col overflow-hidden">
                    <ChatNav />
                    <div className="flex-1 overflow-y-auto p-3 min-h-0">
                        <div className="space-y-4 max-w-4xl mx-auto pb-4">
                            {messages?.map((message: {role: string, content: string, type: string}, index: number) => {
                                if (message.role === 'user' || message.role === 'human' || message.type === 'human') {
                                    return (
                                        <div key={index} className="flex justify-end">
                                            <div className="max-w-[80%] md:max-w-[70%] bg-primary text-primary-foreground p-3 rounded-lg rounded-br-sm">
                                                <MarkdownCard content={message.content} />
                                            </div>
                                        </div>
                                    )
                                } else {
                                    return (
                                        <div key={index} className="flex justify-start">
                                            <div className="max-w-[90%] md:max-w-[80%] bg-muted text-muted-foreground p-3 rounded-lg rounded-bl-sm">
                                                <MarkdownCard content={message.content} />
                                            </div>
                                        </div>
                                    )
                                }
                            })}
                            <div ref={messagesEndRef} /> {/* Invisible element to scroll to */}
                        </div>
                    </div>

                    <div className="sticky bottom-0 bg-background border-t border-border">
                        <div className="flex gap-3 p-3">
                            <textarea 
                                className="flex-1 resize-none min-h-[44px] max-h-[200px] p-3 bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
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
                            />
                            <Button onClick={handleQuery}>
                                Send
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </ChatLayout>
    );
} 