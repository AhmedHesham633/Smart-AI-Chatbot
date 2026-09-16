"""
chatbot.py
----------
Core conversation logic for the Smart AI Chatbot.

Responsibilities:
- Read and normalize user input
- Validate user messages
- Handle exit commands
- Build conversation messages
- Communicate with the AI API
- Handle API errors safely
- Display assistant responses
- Maintain conversation history
"""

from typing import Dict, List

from src.api_client import generate_response
from src.prompts import build_messages, update_history
from src.utils import is_empty, is_exit_command, normalize_text


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXIT_COMMANDS = {"exit", "quit", "/exit"}


# ---------------------------------------------------------------------------
# Input / Output
# ---------------------------------------------------------------------------

def get_user_input() -> str:
    """
    Read and normalize one message from the user.

    Returns:
        str: Normalized user input.
    """
    return normalize_text(input("You: "))


def display_response(response: str) -> None:
    """Display the assistant's response."""
    print(f"Assistant: {response}\n")


def display_error(message: str) -> None:
    """
    Display a user-friendly error message.

    Args:
        message: Error message to display.
    """
    print(f"Assistant: {message}\n")


def is_valid_input(user_input: str) -> bool:
    """
    Check whether the user's input is valid and non-empty.

    Args:
        user_input: User's message.

    Returns:
        bool: True when the input contains text.
    """
    return not is_empty(user_input)


# ---------------------------------------------------------------------------
# AI Response
# ---------------------------------------------------------------------------

def _get_bot_reply_result(
    history: List[Dict[str, str]],
    user_input: str
) -> tuple[str, bool]:
    """
    Build the conversation context and request an AI response.

    Returns:
        tuple[str, bool]:
            The user-facing response and whether the API request succeeded.
    """
    try:
        messages = build_messages(history, user_input)
        reply = generate_response(messages)

        if not reply or not reply.strip():
            display_error(
                "Sorry, I received an empty response. "
                "Please try again."
            )
            return "", False

        return reply.strip(), True

    except ValueError as exc:
        print(f"[Configuration Error] {exc}")
        message = (
            "Sorry, the AI service is not configured correctly. "
            "Please check the API configuration."
        )
        display_error(message)
        return message, False

    except RuntimeError as exc:
        print(f"[API Error] {exc}")
        message = (
            "Sorry, I couldn't reach the AI service. "
            "Please check your connection and try again."
        )
        display_error(message)
        return message, False

    except Exception as exc:
        print(f"[Unexpected Error] {exc}")
        message = (
            "Sorry, an unexpected error occurred. "
            "Please try again."
        )
        display_error(message)
        return message, False


def get_bot_reply(
    history: List[Dict[str, str]],
    user_input: str
) -> str:
    """
    Build the conversation context and request an AI response.

    This public function preserves the simple string-based interface
    expected by the existing tests.
    """
    reply, _ = _get_bot_reply_result(history, user_input)
    return reply


# ---------------------------------------------------------------------------
# Main Conversation Loop
# ---------------------------------------------------------------------------

def run_chatbot() -> None:
    """
    Start and manage the chatbot conversation.

    The conversation continues until the user enters
    a supported exit command.
    """
    history: List[Dict[str, str]] = []

    print("=" * 55)
    print("              Smart AI Chatbot")
    print("=" * 55)
    print("Type 'exit', 'quit', or '/exit' to end the conversation.")
    print()

    while True:
        user_input = get_user_input()

        if is_exit_command(user_input, EXIT_COMMANDS):
            print("Assistant: Goodbye! 👋")
            break

        if is_empty(user_input):
            display_error("Please enter a message.")
            continue

        reply, success = _get_bot_reply_result(history, user_input)

        # Do not update history if the API request failed.
        if not success:
            continue

        display_response(reply)

        history = update_history(
            history,
            user_input,
            reply
        )


if __name__ == "__main__":
    run_chatbot()
