from groq import (
    Groq, 
    AuthenticationError,
    APIConnectionError as GroqAPIConnectionError,
    APITimeoutError as GroqAPITimeoutError,
    RateLimitError as GroqRateLimitError,
    APIResponseValidationError,)

from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, SYSTEM_PROMPT, MAX_RETRIES, RETRY_DELAY, REQUEST_TIMEOUT

import time

from utils.logger import logger

from backend.exceptions import InvalidAPIKeyError, APIConnectionError, APITimeoutError, RateLimitError, ResponseError



class ChatBot:

    """
        ChatBot manages all communication with the LLM provider.

        Responsibilities:
        - Configure LLM client
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
            logger.error("No API key is provided.")

            raise InvalidAPIKeyError(
                "API key not found. " 
                "Add it to .env or enter it in the sidebar"
            )

        self.client = self._configure_client()

        logger.info("ChatBot initialized successfully.")


    def _configure_client(self):
        """
        Configure the LLM client and return it.
        """

        logger.info("Configuring LLM client...")

        client = Groq(
            api_key=self.api_key,
            timeout=REQUEST_TIMEOUT
        )

        logger.info(f"Loaded model: {MODEL_NAME}")

        return client
    
    def _build_messages(
    self,
    history: list[dict],
    ) -> list[dict]:
        """
        Build the conversation history in the format
        expected by the LLM.
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
        Generate a response from LLM using
        the previous conversation history.
        """

        messages = self._build_messages(history)


        logger.info("Sending request to LLM...")

        for attempt in range(1, MAX_RETRIES +1):

            try:

                logger.info(
                    f"Sending request to LLM (Attempt {attempt}/{MAX_RETRIES})..."
                )

                response = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=TEMPERATURE,
                )

                logger.info("Response received successfully.")

                return response.choices[0].message.content
            
            except GroqAPIConnectionError as e:

                logger.warning(
                    f"Connection attempt {attempt}/{MAX_RETRIES} failed: {e}"
                )

                if attempt == MAX_RETRIES:

                    logger.exception(
                        "Failed to connect to AI service. after all retry attempts."
                    )

                    raise APIConnectionError(
                        "Unable to connect to the AI service. Please check your internet connection and try again."
                    ) from e

                logger.info(
                    f"Retrying in {RETRY_DELAY} seconds..."
                )

                time.sleep(RETRY_DELAY)

            except GroqAPITimeoutError as e:

                logger.warning(
                    f"Timeout on attempt {attempt}/{MAX_RETRIES}: {e}"
                )

                if attempt == MAX_RETRIES:

                    logger.exception(
                        "LLM request timed out after all retry attempts."
                    )

                    raise APITimeoutError(
                        "The request timed out. Please try again."
                    ) from e

                logger.info(
                    f"Retrying in {RETRY_DELAY} seconds..."
                )

                time.sleep(RETRY_DELAY)

            
            except AuthenticationError as e:

                logger.exception("Authentication failed.")

                raise InvalidAPIKeyError(
                    "The provided API key is invalid."
                ) from e
            
            
            
            except GroqRateLimitError as e:

                logger.exception("API rate limit exceeded")

                raise RateLimitError(
                    "Rate limit exceed. Please try again in a few moments."
                ) from e
            
            
            except APIResponseValidationError as e:

                logger.exception("Invalid response from LLM.")

                raise ResponseError(
                    "The AI returned an invalid response."
                ) from e
            
            
            except Exception as e:

                logger.exception("Unexpected chatbot error.")

                raise ResponseError(
                    "An unexpected error occurred while generating a response."
                ) from e
            