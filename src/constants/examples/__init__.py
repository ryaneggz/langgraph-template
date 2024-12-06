NEW_THREAD_QUERY_EXAMPLE = {
    "system": "You are a helpful assistant.",
    "query": "What is the capital of France?",
    "tools": [],
    "stream": False,
    "images": [],
    "visualize": False
}

NEW_THREAD_ANSWER_EXAMPLE = {
    "thread_id": "443250c4-b9ec-4dfc-96fd-0eb3ec6ccb44",
    "answer": {
        "content": "The capital of France is Paris.",
        "additional_kwargs": {},
        "response_metadata": {
            "id": "msg_01MBf5kez6rvPXKLiF5cquS6",
            "model": "claude-3-5-sonnet-20240620",
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": 20,
                "output_tokens": 10
            }
        },
        "type": "ai",
        "name": None,
        "id": "run-1a31cbe1-e361-424d-bad4-d106d0b32256-0",
        "example": False,
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": {
            "input_tokens": 20,
            "output_tokens": 10,
            "total_tokens": 30,
            "input_token_details": {}
        }
    }
}

EXISTING_THREAD_QUERY_EXAMPLE = {
    "query": "What about Germany?",
    "tools": [],
    "stream": False,
    "images": []
}

EXISTING_THREAD_ANSWER_EXAMPLE = {
    "thread_id": "443250c4-b9ec-4dfc-96fd-0eb3ec6ccb44",
    "answer": {
        "content": "The capital of Germany is Berlin.",
        "additional_kwargs": {},
        "response_metadata": {
        "id": "msg_01NRjVLzASk28A1JaNXj1TwV",
        "model": "claude-3-5-sonnet-20240620",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": 37,
            "output_tokens": 10
        }
        },
        "type": "ai",
        "name": None,
        "id": "run-6f5b5cc4-2b45-4486-8f92-ef14762039bc-0",
        "example": False,
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": {
        "input_tokens": 37,
        "output_tokens": 10,
        "total_tokens": 47,
        "input_token_details": {}
        }
    }
}

THREAD_HISTORY_EXAMPLE = {
    "thread_id": "443250c4-b9ec-4dfc-96fd-0eb3ec6ccb44",
    "messages": [
        {
            "content": "You are a helpful assistant.",
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "system",
            "name": None,
            "id": "8b6c3e63-a564-4738-8cd1-83f726efdd26"
        },
        {
            "content": "What is the capital of France?",
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "human",
            "name": None,
            "id": "e70c5a2f-9a67-40d5-bdcd-f703edd1febe",
            "example": False
        },
        {
            "content": "The capital of France is Paris.",
            "additional_kwargs": {},
            "response_metadata": {
                "id": "msg_01MBf5kez6rvPXKLiF5cquS6",
                "model": "claude-3-5-sonnet-20240620",
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_tokens": 20,
                    "output_tokens": 10
                }
            },
            "type": "ai",
            "name": None,
            "id": "run-1a31cbe1-e361-424d-bad4-d106d0b32256-0",
            "example": False,
            "tool_calls": [],
            "invalid_tool_calls": [],
            "usage_metadata": {
                "input_tokens": 20,
                "output_tokens": 10,
                "total_tokens": 30,
                "input_token_details": {}
            }
        },
        {
            "content": "What about Germany?",
            "additional_kwargs": {},
            "response_metadata": {},
            "type": "human",
            "name": None,
            "id": "2215e75a-d440-4f95-acd0-c4ae5ae034f1",
            "example": False
        },
        {
            "content": "The capital of Germany is Berlin.",
            "additional_kwargs": {},
            "response_metadata": {
                "id": "msg_01NRjVLzASk28A1JaNXj1TwV",
                "model": "claude-3-5-sonnet-20240620",
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_`tokens": 37,
                    "output_tokens": 10
                }
            },
            "type": "ai",
            "name": None,
            "id": "run-6f5b5cc4-2b45-4486-8f92-ef14762039bc-0",
            "example": False,
            "tool_calls": [],
            "invalid_tool_calls": [],
            "usage_metadata": {
                "input_tokens": 37,
                "output_tokens": 10,
                "total_tokens": 47,
                "input_token_details": {}
            }
        }
    ]
}