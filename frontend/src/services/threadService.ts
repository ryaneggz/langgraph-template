import apiClient from '../utils/apiClient';
import { SSE } from "sse.js";

interface ThreadPayload {
  threadId?: string;
  images: string[];
  query: string;
  system: string;
  tools: any[];
  visualize: boolean;
}

export const queryThread = async (payload: ThreadPayload) => {
  const source = new SSE(`http://localhost:8000/llm${payload.threadId ? `/${payload.threadId}` : ''}`, // TODO: Make this dynamic
    {
      headers: {
        'Content-Type': 'application/json', 
        'Accept': 'text/event-stream', // TODO: Make this dynamic
        'Authorization': `Basic ${btoa("admin:test1234")}` // TODO: Make this dynamic
      },
      payload: JSON.stringify(payload),
      method: 'POST'
    }
  );
  source.addEventListener("error", (e: any) => {
    console.error("Error received from server:", e);
    const errData = JSON.parse(e?.data);
    alert(errData?.detail);
    source.close();
    throw new Error(errData?.detail);
  });
  source.addEventListener("message", (e: any) => {
    console.log(e.data);
  });
  source.stream();
};

export const findThread = async (threadId: string) => {
  const response = await apiClient.get(`/thread/${threadId}`);
  return response.data;
};