from utils.exporter import export_as_markdown

history = [
    {
        "role": "user",
        "content": "Hello!",
        "timestamp": "11:42:15",
    },
    {
        "role": "assistant",
        "content": "Hi! How can I help you?",
        "timestamp": "11:42:18",
    },
]
metadata = {
    "conversation_id": "TEST1234",
    "exported_on": "2026-07-02 17:15:42",
}
markdown = export_as_markdown(history, metadata)

with open("conversation.md", "w", encoding="utf-8") as file:
    file.write(markdown)

print("conversation.md created successfully!")
