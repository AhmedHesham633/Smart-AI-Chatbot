SYSTEM_PROMPT = """
You are a helpful and friendly AI assistant.

Answer the user's questions clearly and accurately.

If you are unsure about something, say that you are unsure.
"""


def build_messages(history, user_message):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    return messages


def update_history(history, user_message, assistant_response):
    history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    return history
