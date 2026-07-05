from groq import (
    Groq, 
    AuthenticationError,
    APIConnectionError as GroqAPIConnectionError,
    APITimeoutError as GroqAPITimeoutError,
    RateLimitError as GroqRateLimitError,
    APIResponseValidationError,)

from collections.abc import Generator

from config import (
    GROQ_API_KEY,
    DEFAULT_MODEL,
    TEMPERATURE,
    SYSTEM_PROMPT,
    MAX_RETRIES,
    RETRY_DELAY,
    REQUEST_TIMEOUT,
)

import time

from utils.logger import logger

from backend.exceptions import InvalidAPIKeyError, APIConnectionError, APITimeoutError, RateLimitError, ResponseError

from models import ChatMessage



class ChatBot:

    """
        ChatBot manages all communication with the LLM provider.

        Responsibilities:
        - Configure LLM client
        - Build conversation messages
        - Send chat requests
        - Return AI responses
    """


    def __init__(
            self,
            api_key: str | None = None,
            model: str = DEFAULT_MODEL,
            ):

        """
        Initialize the chatbot.

        If an API key is passed from the frontend,
        use it. Otherwise, use the key from config.py.
        """

        self.api_key = api_key or GROQ_API_KEY

        self.model = model

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

        logger.info(f"Loaded model: {self.model}")

        return client
    

# prepares data
    def _build_messages( 
    self,
    history: list[ChatMessage],
    ) -> list[dict[str, str]]:
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
    

# manages retries/errors

    def _execute_request(
        self,
        messages: list[dict[str, str]],
        stream: bool,
    ):
        """
        Execute an LLM request with retry logic and
        centralized exception handling.
        """

        logger.info("Sending request to LLM...")

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                logger.info(
                    f"Sending request to LLM (Attempt {attempt}/{MAX_RETRIES})..."
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=TEMPERATURE,
                    stream=stream,
                )

                logger.info("Response received successfully.")

                return response

            except GroqAPIConnectionError as e:

                logger.warning(
                    f"Connection attempt {attempt}/{MAX_RETRIES} failed: {e}"
                )

                if attempt == MAX_RETRIES:

                    logger.exception(
                        "Failed to connect to AI service after all retry attempts."
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

                logger.exception("API rate limit exceeded.")

                raise RateLimitError(
                    "Rate limit exceeded. Please try again in a few moments."
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


# returns a complete response
    def chat(
    self,
    user_message: str,  # Reserved for future preprocessing, moderation, and analytics.
    history: list[ChatMessage]
    ) -> str:
        """
        Generate a response from LLM using
        the previous conversation history.
        """

        messages = self._build_messages(history)


        response = self._execute_request(
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content

 # yields streamed chunks   
    def stream_chat(
        self,
        user_message: str,
        history: list[ChatMessage],
    ) -> Generator[str, None, None]:
        """
        Stream a response from the LLM.
        """

        messages = self._build_messages(history)

        stream = self._execute_request(
            messages=messages,
            stream=True,
        )

        # for chunk in stream:
        #     delta = chunk.choices[0].delta.content

        #     if delta:
        #         yield delta

        for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                yield delta