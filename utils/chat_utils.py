from datetime import datetime

import uuid


def generate_session_id() -> str:
    """
    Generate a short unique identifier
    for the current chat session.
    """

    return str(uuid.uuid4())[:8].upper()



def get_chat_statistics(history: list[dict]) -> dict:
    """
    Calculate useful statistics for the current conversation.

    Returns:
        dict containing conversation metrics.
    """
    message_count = len(history)

    if message_count == 0:
        session_duration = "0 sec" 

    else:
        start_time = datetime.strptime(
            history[0]["timestamp"],
            "%H:%M:%S",
        )

        end_time = datetime.strptime(
            history[-1]["timestamp"],
            "%H:%M:%S",
        )

        duration = end_time - start_time

        seconds = int(duration.total_seconds())

        if seconds < 60:
            session_duration = f"{seconds} sec"
        
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60

            session_duration = f"{minutes} min {remaining_seconds} sec"

        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            session_duration = f"{hours} hr {minutes} min"

    user_messages = sum(
        1 for message in history
        if message["role"] == "user"
    )

    assistant_messages = sum(
        1 for message in history
        if message["role"] == "assistant"
    )


    return {
        "message_count": message_count,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "session_duration": session_duration
    }
