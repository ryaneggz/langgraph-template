import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Model, listModels } from '@/services/modelService';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useChatContext } from '@/context/ChatContext';
import { SiAnthropic, SiOpenai } from 'react-icons/si';
import { FaPlus } from 'react-icons/fa';
import { Button } from "@/components/ui/button";

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [models, setModels] = useState<Model[]>([]);
  const currentModel = searchParams.get('model') || '';
  const { setPayload, setMessages } = useChatContext();

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await listModels();
        setModels(response.models);
        
        // Set default model if none selected
        if (!currentModel && response.models.length > 0) {
          setSearchParams({ model: response.models[0].id });
        }
      } catch (error) {
        console.error('Failed to fetch models:', error);
      }
    };

    fetchModels();
  }, []);

  useEffect(() => {
    if (currentModel) {
      setPayload((prev: any) => ({ ...prev, model: currentModel }));
    }
  }, [currentModel, setPayload]);

  const handleModelChange = (modelId: string) => {
    setSearchParams({ model: modelId });
  };

  const handleNewChat = () => {
    setMessages([]);
    setPayload((prev: any) => ({ ...prev, threadId: '', query: '' }));
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <header className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <button 
                onClick={() => navigate(-1)}
                className="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors mr-4"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-5 w-5 mr-1" 
                  viewBox="0 0 20 20" 
                  fill="currentColor"
                >
                  <path 
                    fillRule="evenodd" 
                    d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" 
                    clipRule="evenodd" 
                  />
                </svg>
                Back
              </button>
              <h1 className="text-2xl font-bold text-foreground">Chat</h1>
            </div>
            
            <div className="flex items-center gap-2">
              <Select value={currentModel} onValueChange={handleModelChange}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="Select Model" />
                </SelectTrigger>
                <SelectContent>
                  {models
                    .filter(model => !model.metadata.embedding)
                    .map((model) => (
                      <SelectItem key={model.id} value={model.id}>
                        <div className="flex items-center gap-2">
                          {model.provider === 'openai' && (
                            <SiOpenai className="h-4 w-4" />
                          )}
                          {model.provider === 'anthropic' && (
                            <SiAnthropic className="h-4 w-4" />
                          )}
                          {model.label}
                        </div>
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>

              <Button
                variant="outline"
                size="icon"
                onClick={handleNewChat}
                className="h-9 w-9"
                title="New Chat"
              >
                <FaPlus className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {children}
    </div>
  );
}
