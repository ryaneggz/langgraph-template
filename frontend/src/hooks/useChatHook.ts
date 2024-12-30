import debug from 'debug';
import { SSE } from "sse.js";
import { useEffect, useRef, useState } from "react";
import { ThreadPayload } from '../entities';
import { TOKEN_NAME, VITE_API_URL } from '../config';
import apiClient from '@/lib/utils/apiClient';
debug.enable('hooks:*');
const logger = debug('hooks:useChatHook');

const initChatState = {
    response: null,
    responseRef: "",
    messages: [],
    payload: {
        threadId: '',
        images: [] as string[],
        query: '',
        system: 'You are a helpful assistant.',
        tools: [] as any[],
        visualize: false,
        model: ''
    },
    history: {
        threads: [],
        page: 1,
        per_page: 20,
        total: 0,
        next_page: '',
    }
}

export default function useChatHook() {
    const token = localStorage.getItem(TOKEN_NAME);
    const responseRef = useRef(initChatState.responseRef);
    const [response, setResponse] = useState<any>(initChatState.response);  
    const [messages, setMessages] = useState<any[]>(initChatState.messages);
    const [payload, setPayload] = useState(initChatState.payload);
    const [history, setHistory] = useState<any>(initChatState.history);


    const handleQuery = () => {
        queryThread(payload);
    }

    const queryThread = (payload: ThreadPayload) => {
        logger("Querying thread:", payload);
        const updatedMessages = [...messages, { role: 'user', content: payload.query }];
        setMessages(updatedMessages);
        setResponse("");
        responseRef.current = "";
        const source = new SSE(`${VITE_API_URL}/llm${payload.threadId ? `/${payload.threadId}` : ''}`, // TODO: Make this dynamic
            {
                headers: {
                    'Content-Type': 'application/json', 
                    'Accept': 'text/event-stream', // TODO: Make this dynamic
                    'Authorization': `Basic ${token}` // TODO: Make this dynamic
                },
                payload: JSON.stringify(payload),
                method: 'POST'
            }
        );

        source.addEventListener("error", (e: any) => {
            logger("Error received from server:", e);
            const errData = JSON.parse(e?.data);
            alert(errData?.detail);
            source.close();
            throw new Error(errData?.detail);
        });

        source.addEventListener("open", () => {
            const messagesWithAssistant = [...updatedMessages, { role: "assistant", content: "" }];
            setMessages(messagesWithAssistant);
        });

        source.addEventListener("message", (e: any) => {
            const data = JSON.parse(e.data);
            const message = data.content;
            logger("Message received:", message);
            responseRef.current += message;
            
            const finalMessages = [...messages, 
                { role: 'user', content: payload.query },
                { role: "assistant", content: responseRef.current }
            ];
            setPayload({ ...payload, query: '', threadId: data.thread_id });
            if (data.event === "end") {
                getHistory(1, history.per_page);
                source.close();
                logger("Thread ended");
                return;
            }
            setResponse(responseRef.current);
            setMessages(finalMessages);
        });
        source.stream();
        return true;
    };

    const getHistory = async (page: number = 1, perPage: number = 20) => {
        try {
            const res = await apiClient.get(`${VITE_API_URL}/threads?page=${page}&per_page=${perPage}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json', 
                    'Authorization': `Basic ${token}`
                },
                method: 'GET'
            });
            setHistory(res.data);
        } catch (error: any) {
            logger('Error listing threads:', error);
            throw new Error(error.response?.data?.detail || 'Failed to list threads');
        }
    }

    const useGetHistoryEffect = () => {
        useEffect(() => {
            getHistory();

            return () => {
                // Cleanup logic if needed
            };
        }, []);
    };

    return {
        ...initChatState,
        messages,
        setMessages,
        responseRef,
        response,
        setResponse,
        handleQuery,
        payload,
        setPayload,
        getHistory,
        history,
        setHistory,
        useGetHistoryEffect 
    }
}


