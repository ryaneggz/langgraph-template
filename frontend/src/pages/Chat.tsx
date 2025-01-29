import ChatLayout from '../layouts/ChatLayout';
import { useChatContext } from '../context/ChatContext';
import MarkdownCard from '../components/cards/MarkdownCard';
import { Button } from '@/components/ui/button';
import { ThreadHistoryDrawer } from '@/components/drawers/ThreadHistoryDrawer';
import { useEffect, useRef, useState } from 'react';
import {ChatNav} from '@/components/nav/ChatNav';
import SystemMessageCard from '@/components/cards/SystemMessageCard';
import { ChatDrawer } from '@/components/drawers/ChatDrawer';

export default function Chat() {
    const { messages, payload, handleQuery, setPayload, useGetHistoryEffect } = useChatContext();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [isAssistantOpen, setIsAssistantOpen] = useState(true);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]); // Scroll when messages change

    useGetHistoryEffect();

    return (
        <ChatLayout>
            <div className={`
                flex min-h-[calc(100vh-0px)] max-h-[calc(100vh-0px)] relative
                transition-[padding-right] duration-200 ease-in-out
                ${isAssistantOpen ? 'pr-[320px]' : ''}
            `}>
                <ThreadHistoryDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} />
                
                <div className="flex-1 flex flex-col overflow-hidden">
                    <ChatNav 
                        onMenuClick={() => setIsDrawerOpen(!isDrawerOpen)}
                        onAssistantClick={() => setIsAssistantOpen(!isAssistantOpen)} 
                    />
                    <div className="flex-1 overflow-y-auto p-3 min-h-0">
                        <div className="space-y-4 max-w-4xl mx-auto pb-4">
                            {messages?.map((message: {role: string, content: string, type: string}, index: number) => {
                                if (message.role === 'user' || message.role === 'human' || message.type === 'human') {
                                    return (
                                        <div key={index} className="flex justify-end">
                                            <div className="max-w-[80%] md:max-w-[70%] bg-primary/90 text-primary-foreground p-3 rounded-lg rounded-br-sm">
                                                <MarkdownCard content={message.content} />
                                            </div>
                                        </div>
                                    )
                                } else if (message.role === 'system' || message.type === 'system') {
                                    return <SystemMessageCard content={message.content} />
                                } else {
                                    return (
                                        <div key={index} className="flex justify-start">
                                            <div className="max-w-[90%] md:max-w-[80%] bg-transparent text-foreground-500 p-3 rounded-lg rounded-bl-sm">
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
                            <Button onClick={handleQuery} disabled={payload.query.trim() === ''}>
                                Send
                            </Button>
                        </div>
                    </div>
                </div>

                <ChatDrawer isOpen={isAssistantOpen} onClose={() => setIsAssistantOpen(false)}>
                    <div className="space-y-4">
                        <div className="flex items-center space-x-2">
                            <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                                <span className="text-primary">AI</span>
                            </div>
                            <div>
                                <h3 className="font-medium">GPT-4</h3>
                                <p className="text-sm text-muted-foreground">Our most capable model</p>
                            </div>
                        </div>
                        
                        <div className="prose prose-sm dark:prose-invert">
                            <p>The current model can:</p>
                            <ul className="list-disc pl-4 space-y-1">
                                <li>Analyze complex problems</li>
                                <li>Generate creative content</li>
                                <li>Handle detailed conversations</li>
                                <li>Process and explain code</li>
                            </ul>
                        </div>
                    </div>
                </ChatDrawer>
            </div>
        </ChatLayout>
    );
} 