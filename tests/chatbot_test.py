"""
test_chatbot.py
---------------
Unit tests for the Smart AI Chatbot conversation logic.
"""

from unittest.mock import patch

from src.chatbot import (
    is_valid_input,
    is_exit_command,
    get_bot_reply,
)


# ---------------------------------------------------------------------------
# Input Validation Tests
# ---------------------------------------------------------------------------

def test_valid_input():
    assert is_valid_input("Hello") is True


def test_empty_input():
    assert is_valid_input("") is False


def test_whitespace_input():
    assert is_valid_input("   ") is False


# ---------------------------------------------------------------------------
# Exit Command Tests
# ---------------------------------------------------------------------------

def test_exit_command():
    assert is_exit_command("exit") is True


def test_quit_command():
    assert is_exit_command("quit") is True


def test_slash_exit_command():
    assert is_exit_command("/exit") is True


def test_exit_command_is_case_insensitive():
    assert is_exit_command("EXIT") is True


def test_normal_message_is_not_exit():
    assert is_exit_command("hello") is False


# ---------------------------------------------------------------------------
# AI Response Tests
# ---------------------------------------------------------------------------

@patch("src.chatbot.generate_response")
def test_get_bot_reply(mock_generate_response):
    mock_generate_response.return_value = "Hello! How can I help you?"

    history = []

    reply = get_bot_reply(history, "Hello")

    assert reply == "Hello! How can I help you?"
    mock_generate_response.assert_called_once()


@patch("src.chatbot.generate_response")
def test_get_bot_reply_handles_api_error(mock_generate_response):
    mock_generate_response.side_effect = RuntimeError(
        "AI API request failed"
    )

    history = []

    reply = get_bot_reply(history, "Hello")

    assert "couldn't reach the AI service" in reply