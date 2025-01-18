import { ScrollArea } from "@/components/ui/scroll-area";
import { useChatContext } from "@/context/ChatContext";
import { formatDistanceToNow } from "date-fns";
import { Button } from "@/components/ui/button";
import { truncateFrom } from "@/lib/utils/format";
import { Plus } from "lucide-react";
import { SettingsPopover } from "../popovers/SettingsPopover";

interface ThreadHistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ThreadHistoryDrawer({ isOpen, onClose }: ThreadHistoryDrawerProps) {
  const { history, setMessages, setPayload } = useChatContext();

  const handleThreadClick = (threadId: string, messages: any[]) => {
    setMessages(messages);
    setPayload((prev: any) => ({ ...prev, threadId }));
    onClose(); // Close drawer after selection on mobile
  };

  return (
    <>
      {/* Overlay for mobile - only shows when drawer is open */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 md:hidden" 
          onClick={onClose}
        />
      )}
      
      <div className={`
        absolute md:relative w-[300px] border-r border-border flex flex-col h-[calc(100vh-0px)]
        ${isOpen ? 'flex' : 'hidden md:flex'}
        bg-background z-40
      `}>
          <div className="p-4 border-b border-border">
              <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleThreadClick("", [])}
              >
                  <Plus className="mr-2 h-4 w-4" />
                  New Chat
              </Button>
          </div>

          <ScrollArea className="flex-1">
              <div className="p-2 space-y-2">
                  {history?.threads?.map((thread: any) => (
                      <button
                          key={thread.thread_id}
                          onClick={() =>
                              handleThreadClick(
                                  thread.thread_id,
                                  thread.messages
                              )
                          }
                          className="w-full text-left p-3 rounded-lg hover:bg-accent transition-colors border border-border"
                      >
                          <div className="w-full">
                              <p className="text-sm font-medium line-clamp-2">
                                  {truncateFrom(thread.messages[1]?.content, 'end', "...", 100) || "New Chat"}
                              </p>
                              <p className="text-xs text-muted-foreground mt-1 truncate">
                                  {formatDistanceToNow(new Date(thread.ts), {
                                      addSuffix: true,
                                  })}
                              </p>
                          </div>
                      </button>
                  ))}
              </div>
          </ScrollArea>

            <div className="p-4 border-t border-border">
                <SettingsPopover />
            </div>
      </div>
    </>
  );
} 