from utils.pdf_exporter import export_as_pdf

history = []

for i in range(30):
    history.append(
        {
            "role": "user",
            "content": f"This is user message number {i + 1}. " * 3,
            "timestamp": "11:42:15",
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": f"This is assistant response number {i + 1}. " * 4,
            "timestamp": "11:42:20",
        }
    )

metadata = {
    "conversation_id": "TEST1234",
    "exported_on": "2026-07-02 18:10:00",
}

pdf = export_as_pdf(history, metadata)

with open("sample.pdf", "wb") as file:
    file.write(pdf)

print("sample.pdf created successfully!")