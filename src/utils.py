"""
utils.py
--------
General utility functions for the Smart AI Chatbot.
"""


def normalize_text(text: str) -> str:
    """
    Remove unnecessary whitespace from user input.

    Args:
        text: Raw user input.

    Returns:
        Normalized user input.
    """
    return " ".join(text.strip().split())


def is_empty(text: str) -> bool:
    """
    Check whether the given text is empty or contains only whitespace.

    Args:
        text: User input.

    Returns:
        True if the input is empty, otherwise False.
    """
    return not bool(text.strip())


def is_exit_command(
    text: str,
    exit_commands: set[str] | None = None
) -> bool:
    """
    Check whether the user entered a supported exit command.

    Args:
        text: User input.
        exit_commands: Supported exit commands.

    Returns:
        bool: True if the input is an exit command.
    """
    if exit_commands is None:
        exit_commands = {"exit", "quit", "/exit"}

    return text.lower().strip() in exit_commands