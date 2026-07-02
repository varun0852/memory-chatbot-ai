from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, SYSTEM_PROMPT

from utils.logger import logger



class ChatBot:

    """
        ChatBot manages all communication with the Groq API.

        Responsibilities:
        - Configure Groq client
        - Build conversation messages
        - Send chat requests
        - Return AI responses
    """


    def __init__(self, api_key: str | None = None):

        """
        Initialize the chatbot.

        If an API key is passed from the frontend,
        use it. Otherwise, use the key from config.py.
        """

        self.api_key = api_key or GROQ_API_KEY

        if not self.api_key:
            raise ValueError(
            "Groq API Key not found. "
            "Add it to .env or enter it in the sidebar."
        )

        self.client = self._configure_model()

        logger.info("ChatBot initialized successfully.")


    def _configure_model(self) -> Groq:
        """
        Configure the Groq client and return it.
        """

        logger.info("Configuring Groq client...")

        client = Groq(api_key=self.api_key)

        logger.info(f"Loaded model: {MODEL_NAME}")

        return client
    
    def _build_messages(
    self,
    history: list[dict],
    ) -> list[dict]:
        """
        Build the conversation history in the format
        expected by the Groq API.
        """

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        for message in history:
            messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

        return messages
    

    def chat(
    self,
    user_message: str,
    history: list[dict]
    ) -> str:
        """
        Generate a response from Groq using
        the previous conversation history.
        """

        messages = self._build_messages(history)


        logger.info("Sending request to Groq...")

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
        )

        logger.info("Response received successfully.")

        return response.choices[0].message.content