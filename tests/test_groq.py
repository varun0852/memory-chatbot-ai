from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Explain Python in one sentence."
        }
    ]
)

print(response.choices[0].message.content)