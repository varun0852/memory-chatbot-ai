import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from backend import ChatBot

bot = ChatBot()

history = []

response = bot.chat("Hello! Who are you?", history)

print(response)
