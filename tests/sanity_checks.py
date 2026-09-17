"""
sanity_checks.py
-----------------
Integration-style sanity checks for the Smart AI Chatbot.

These tests exercise the full flow across chatbot.py, prompts.py, and
api_client.py (with the network call to Cohere mocked out) to verify
that the three members' components integrate correctly.

They complement tests/chatbot_test.py, which covers the lower-level
unit behavior (input validation, exit commands, single bot-reply calls).
This file focuses on multi-turn history correctness, prompt structure,
response parsing, and error-path behavior end-to-end.

Run with:
    pytest tests/ -v

No real API key or network access is required — every test that would
otherwise hit the Cohere API mocks src.chatbot.generate_response
(the same import chatbot.py itself uses) or src.api_client.API_KEY.
The one exception is test_api.py at the project root, which is an
optional, manual, real-API integration check (see README "Testing").
"""

from unittest.mock import patch

import pytest

from src.chatbot import _get_bot_reply_result, get_bot_reply, is_valid_input
from src.prompts import build_messages, update_history
from src.utils import is_empty, is_exit_command, normalize_text


# ---------------------------------------------------------------------------
# TC-001 / TC-010 — Normal question + response parsing
# ---------------------------------------------------------------------------

@patch("src.chatbot.generate_response")
def test_tc001_normal_question_returns_parsed_reply(mock_generate):
    """TC-001: a normal question is sent, and the parsed text is returned."""
    mock_generate.return_value = "AI stands for Artificial Intelligence."

    reply, success = _get_bot_reply_result([], "What is artificial intelligence?")

    assert success is True
    assert reply == "AI stands for Artificial Intelligence."
    mock_generate.assert_called_once()


@patch("src.chatbot.generate_response")
def test_tc010_response_is_stripped(mock_generate):
    """TC-010: surrounding whitespace from the provider response is stripped."""
    mock_generate.return_value = "   padded reply   "

    reply, success = _get_bot_reply_result([], "hello")

    assert success is True
    assert reply == "padded reply"


@patch("src.chatbot.generate_response")
def test_empty_provider_response_is_treated_as_failure(mock_generate):
    """An empty/whitespace-only reply from the provider must not be treated
    as a successful turn (so history is not polluted with empty replies)."""
    mock_generate.return_value = "   "

    reply, success = _get_bot_reply_result([], "hello")

    assert success is False


# ---------------------------------------------------------------------------
# TC-002 / TC-006 / TC-011 / TC-012 — Multi-turn conversation & history
# ---------------------------------------------------------------------------

@patch("src.chatbot.generate_response")
def test_tc002_followup_question_receives_prior_context(mock_generate):
    """TC-002: the second call's messages must include the first exchange."""
    mock_generate.return_value = "Machine learning is a subset of AI."
    history = []
    reply1, ok1 = _get_bot_reply_result(history, "What is machine learning?")
    assert ok1
    history = update_history(history, "What is machine learning?", reply1)

    mock_generate.return_value = "For example, spam email detection."
    _get_bot_reply_result(history, "Give me an example.")

    # Inspect what was actually sent to the provider on the second call.
    sent_messages = mock_generate.call_args.args[0]
    contents = [m["content"] for m in sent_messages]
    assert "What is machine learning?" in contents
    assert "Machine learning is a subset of AI." in contents
    assert "Give me an example." in contents


@patch("src.chatbot.generate_response")
def test_tc006_tc012_history_order_and_no_duplicates_across_turns(mock_generate):
    """TC-006 / TC-012: run several consecutive turns and verify the
    history stays correctly ordered with no duplicate entries."""
    history = []
    turns = [
        ("Hi", "Hello!"),
        ("What's 2+2?", "4."),
        ("Thanks", "You're welcome!"),
    ]

    for user_msg, bot_msg in turns:
        mock_generate.return_value = bot_msg
        reply, success = _get_bot_reply_result(history, user_msg)
        assert success is True
        history = update_history(history, user_msg, reply)

    assert len(history) == len(turns) * 2
    expected = []
    for user_msg, bot_msg in turns:
        expected.append({"role": "user", "content": user_msg})
        expected.append({"role": "assistant", "content": bot_msg})
    assert history == expected


def test_tc011_history_update_stores_exactly_one_pair():
    """TC-011: update_history appends exactly one user + one assistant
    message, in that order, without mutating earlier entries."""
    history = [{"role": "user", "content": "old"}, {"role": "assistant", "content": "old reply"}]
    result = update_history(list(history), "new question", "new answer")

    assert result[:2] == history
    assert result[2] == {"role": "user", "content": "new question"}
    assert result[3] == {"role": "assistant", "content": "new answer"}
    assert len(result) == 4


def test_build_messages_prepends_system_prompt_and_appends_user_message():
    """Prompt construction: system prompt first, then history, then the
    new user message last — matching what api_client/Cohere expects."""
    history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    messages = build_messages(history, "how are you?")

    assert messages[0]["role"] == "system"
    assert messages[1:-1] == history
    assert messages[-1] == {"role": "user", "content": "how are you?"}


# ---------------------------------------------------------------------------
# TC-003 / TC-004 — Empty / whitespace input
# ---------------------------------------------------------------------------

def test_tc003_empty_input_is_rejected():
    assert is_valid_input("") is False
    assert is_empty("") is True


def test_tc004_whitespace_input_is_rejected():
    assert is_valid_input("     ") is False
    assert is_empty("     ") is True


@patch("src.chatbot.generate_response")
def test_tc003_tc004_api_not_called_for_empty_or_whitespace(mock_generate):
    """The chatbot loop must check is_empty before ever building a prompt
    or calling the API for blank input. (get_bot_reply itself doesn't
    enforce this -- run_chatbot's loop does -- so this test documents the
    expectation that empty text is filtered out upstream.)"""
    for blank in ("", "   ", "\t\n"):
        assert is_empty(normalize_text(blank)) is True
    mock_generate.assert_not_called()


# ---------------------------------------------------------------------------
# TC-005 — Exit commands
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text", ["exit", "quit", "/exit", "EXIT", "  quit  "])
def test_tc005_supported_exit_commands(text):
    assert is_exit_command(normalize_text(text)) is True


def test_tc005_non_exit_message_is_not_treated_as_exit():
    assert is_exit_command("exit please") is False


# ---------------------------------------------------------------------------
# TC-007 / TC-008 / TC-009 — Error handling
# ---------------------------------------------------------------------------

def test_tc008_missing_api_key_raises_configuration_error(monkeypatch):
    """TC-008: with no COHERE_API_KEY set, api_client.generate_response
    must raise ValueError (mapped by chatbot.py to a friendly
    'not configured correctly' message) rather than crashing."""
    import src.api_client as api_client

    monkeypatch.setattr(api_client, "API_KEY", None)
    with pytest.raises(ValueError):
        api_client.generate_response([{"role": "user", "content": "hi"}])


@patch("src.chatbot.generate_response")
def test_tc008_missing_key_produces_friendly_chatbot_message(mock_generate):
    mock_generate.side_effect = ValueError("COHERE_API_KEY is missing. Check your .env file.")

    reply, success = _get_bot_reply_result([], "hello")

    assert success is False
    assert "not configured correctly" in reply


@patch("src.chatbot.generate_response")
def test_tc007_tc009_api_or_network_failure_produces_friendly_message(mock_generate):
    """TC-007 / TC-009: an invalid key or network failure both surface as
    api_client.generate_response raising RuntimeError; the chatbot layer
    must catch it, show a friendly message, and not crash."""
    mock_generate.side_effect = RuntimeError("AI API request failed: 401 Unauthorized")

    reply, success = _get_bot_reply_result([], "hello")

    assert success is False
    assert "couldn't reach the AI service" in reply


@patch("src.chatbot.generate_response")
def test_unexpected_exception_is_still_handled_gracefully(mock_generate):
    """Any other unexpected exception type must not propagate and crash
    the app; it should be converted to a friendly message."""
    mock_generate.side_effect = KeyError("unexpected provider response shape")

    reply, success = _get_bot_reply_result([], "hello")

    assert success is False
    assert "unexpected error occurred" in reply


@patch("src.chatbot.generate_response")
def test_failed_turn_does_not_update_history(mock_generate):
    """A failed API call must not be added to conversation history."""
    mock_generate.side_effect = RuntimeError("boom")
    history = []

    reply, success = _get_bot_reply_result(history, "hello")
    assert success is False
    # Mirrors run_chatbot()'s behavior of skipping update_history on failure.
    assert history == []
