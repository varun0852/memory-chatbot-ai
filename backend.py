import logging

import google.generativeai as genai

from config import GOOGLE_API_KEY, MODEL_NAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)



class ChatBot:

    """
        ChatBot manages all communication with the Google Gemini model.

        Responsibilities:
        - Configure Gemini
        - Convert Streamlit chat history
        - Generate AI responses
    """


    def __init__(self, api_key: str | None = None):

        """
        Initialize the chatbot.

        If an API key is passed from the frontend,
        use it. Otherwise, use the key from config.py.
        """

        self.api_key = api_key or GOOGLE_API_KEY

        if not self.api_key:
            raise ValueError(
                "Google API Key not found. "
                "Add it to .env or enter it in the sidebar."
            )

        self.model = self._configure_model()

        logger.info("ChatBot initialized successfully.")


    def _configure_model(self):
        """
        Configure the Gemini model and return it.
        """

        genai.configure(api_key=self.api_key)

        logger.info("Configuring Gemini model...")

        model = genai.GenerativeModel(MODEL_NAME)

        logger.info(f"Loaded model: {MODEL_NAME}")

        return model
    

    def _prepare_history(
        self,
        history: list[dict]
    ) -> list[dict]:
        """
        Convert Streamlit chat history into the format
        expected by the Gemini API.
        """

        conversation = []

        for message in history:
            role = "user" if message["role"] == "user" else "model"

            conversation.append(
                {
                    "role": role,
                    "parts": [message["content"]],
                }
            )

        return conversation
    

    def chat(
        self,
        user_message: str,
        history: list[dict]
    ) -> str:
        """
        Generate a response from Gemini using the
        previous conversation history.
        """

        conversation = self._prepare_history(history)

        chat = self.model.start_chat(history=conversation)

        logger.info("Sending request to Gemini...")

        response = chat.send_message(user_message)

        logger.info("Response received successfully.")

        return response.text