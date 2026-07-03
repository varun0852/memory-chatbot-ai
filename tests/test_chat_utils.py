from utils.chat_utils import get_chat_statistics

history = [
    {
        "role": "user",
        "content": "Hello!",
        "timestamp": "10:00:00",
    },
    {
        "role": "assistant",
        "content": "Hi! How can I help you?",
        "timestamp": "10:00:15",
    },
    {
        "role": "user",
        "content": "Explain Python.",
        "timestamp": "10:01:00",
    },
    {
        "role": "assistant",
        "content": "Python is a high-level programming language.",
        "timestamp": "10:02:30",
    },
]

stats = get_chat_statistics(history)

print(stats)