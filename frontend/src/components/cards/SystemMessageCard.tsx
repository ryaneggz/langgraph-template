import { useState } from "react"
import { ChevronDown, ChevronUp } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function SystemMessage({ content }: { content: string }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="flex flex-col gap-1 rounded-lg bg-[#1C1C1C] p-3">
      <div className="flex items-center justify-between">
        <div className="text-xs font-medium uppercase tracking-wider text-gray-400">SYSTEM</div>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 w-6 p-0 text-gray-400 hover:text-gray-200"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </Button>
      </div>
      <div className={`text-sm text-gray-200 ${!isExpanded ? "line-clamp-2" : ""}`}>
        <textarea
          className="w-full resize-none bg-transparent focus:outline-none"
          rows={isExpanded ? 6 : 2}
          defaultValue={content}
        />
      </div>
    </div>
  )
}
