from enum import Enum

class ModelName(str, Enum):
    OPENAI_GPT_4O = "openai-gpt-4o"
    OPENAI_GPT_4O_MINI = "openai-gpt-4o-mini"
    OPENAI_REASONING_O1 = "openai-o1-preview"
    OPENAI_REASONING_O1_MINI = "openai-o1-mini"
    OPENAI_EMBEDDING_LARGE = "openai-text-embedding-3-large"
    ANTHROPIC_CLAUDE_3_5_SONNET = "anthropic-claude-3-5-sonnet-20240620"
    
    
MODEL_CONFIG = [
    {
        "id": ModelName.OPENAI_GPT_4O,
        "label": "GPT-4o",
        "provider": "openai",
        "metadata": {
            "system_message": True,
            "reasoning": False,
            "tool_calling": True,
            "multimodal": True,
            "embedding": False,
        }
    },
    {
        "id": ModelName.OPENAI_GPT_4O_MINI,
        "label": "GPT-4o Mini",
        "provider": "openai",
        "metadata": {
            "system_message": True,
            "reasoning": False,
            "tool_calling": True,
            "multimodal": True,
            "embedding": False,
        }
    },
    {
        "id": ModelName.OPENAI_REASONING_O1,
        "label": "o1",
        "provider": "openai",
        "metadata": {
            "system_message": False,
            "reasoning": True,
            "tool_calling": False,
            "multimodal": False,
            "embedding": False,
        }
    },
    {
        "id": ModelName.OPENAI_REASONING_O1_MINI,
        "label": "o1 Mini",
        "provider": "openai",
        "metadata": {
            "system_message": False,
            "reasoning": True,
            "tool_calling": False,
            "multimodal": False,
            "embedding": False,
        }
    },
    {
        "id": ModelName.OPENAI_EMBEDDING_LARGE,
        "label": "Text Embedding 3 Large",
        "provider": "openai",
        "metadata": {
            "system_message": False,
            "reasoning": False,
            "tool_calling": False,
            "multimodal": False,
            "embedding": True,
        }
    },
    {
        "id": ModelName.ANTHROPIC_CLAUDE_3_5_SONNET,
        "label": "Claude 3.5 Sonnet",
        "provider": "anthropic",
        "metadata": {
            "system_message": True,
            "reasoning": False,
            "tool_calling": True,
            "multimodal": True,
            "embedding": False,
        }
    }
]