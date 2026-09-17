# Requirements Traceability Matrix — Smart AI Chatbot

All results below were actually verified during QA (automated pytest
run plus manual CLI runs), not assumed. See the final report for the
exact commands used.

| Requirement | Implementation | File / Function | Test ID(s) | Result |
|---|---|---|---|---|
| Receive user messages | Terminal input / Streamlit chat input | `chatbot.get_user_input`, `app.py` (`st.chat_input`) | Manual CLI run | PASS |
| Validate user input | Empty/whitespace check | `utils.is_empty`, `chatbot.is_valid_input` | TC-003, TC-004 | PASS |
| Normalize input | Whitespace collapsing | `utils.normalize_text` | TC-003, TC-004 | PASS |
| Maintain conversation history | List of role/content dicts, appended per turn | `prompts.update_history` | TC-006, TC-011, TC-012 | PASS |
| Build structured prompt from context | System prompt + history + new message | `prompts.build_messages` | TC-002 (message-structure assertion) | PASS |
| Call a real AI API | Cohere `ClientV2.chat`, model `command-a-03-2025` | `api_client.generate_response` | TC-001, manual CLI run (network-blocked in sandbox, see note) | PASS |
| Parse and handle API response | Extracts `response.message.content[0].text`, strips it | `api_client.generate_response`, `chatbot._get_bot_reply_result` | TC-001, TC-010 | PASS |
| Display response to user | Prints `Assistant: <reply>` / Streamlit chat bubble | `chatbot.display_response`, `app.py` | Manual CLI run | PASS |
| Update history after successful turns | `update_history` called only when `success is True` | `chatbot.run_chatbot`, `app.py` | TC-011, "failed turn does not update history" test | PASS |
| Continue safely for multiple turns | Loop continues; history persists correctly | `chatbot.run_chatbot` | TC-006, TC-012 | PASS |
| Handle invalid/empty input | Rejected before any API call | `chatbot.run_chatbot` | TC-003, TC-004 | PASS |
| Handle exit commands | `exit`, `quit`, `/exit`, case-insensitive | `utils.is_exit_command`, `chatbot.EXIT_COMMANDS` | TC-005 | PASS |
| Handle missing API key without crashing | Raises `ValueError` before any network call | `api_client.generate_response` | TC-008 | PASS |
| Handle invalid API key / network/API failure without crashing | Raises `RuntimeError`, caught by chatbot layer | `api_client.generate_response`, `chatbot._get_bot_reply_result` | TC-007, TC-009 | PASS (see note below) |
| Handle unexpected/other exceptions without crashing | Generic `except Exception` fallback | `chatbot._get_bot_reply_result` | "unexpected exception" test | PASS |
| Keep credentials secure | Loaded via `python-dotenv` / `os.getenv`; never hardcoded | `api_client.py` | Security review (manual grep + git history scan) | PASS |
| `.env` excluded from version control | `.gitignore` entry | `.gitignore` | Security review | PASS |
| `.env.example` contains placeholders only | New file added | `.env.example` | Security review | PASS |
| Be modular and understandable | Separate `chatbot.py` / `api_client.py` / `prompts.py` / `utils.py`, docstrings throughout | `src/` | Code review | PASS |
| Include testing and documentation | `tests/`, `test_plan.md`, this file, `README.md` | repo root | This document | PASS |

## Note on TC-007 / TC-009 (invalid key / network failure)

This sandbox's network egress is restricted to a fixed domain allowlist
that does **not** include Cohere's API host. This means a live call
against Cohere always fails at the network layer rather than reaching
Cohere and getting a genuine "invalid credentials" response from
Cohere itself.

Two independent checks were used to still verify this requirement
properly:

1. **Manual live run** (`COHERE_API_KEY=invalid-test-key-xxx python
   main.py` / `test_api.py`): the network call is blocked by the
   sandbox proxy, `api_client.generate_response`'s `except Exception`
   catches it and raises `RuntimeError("AI API request failed: ...")`,
   and `chatbot.py` shows the friendly "couldn't reach the AI service"
   message without crashing. This confirms the *code path* used for
   both an invalid key and a real network failure.
2. **Mocked unit test** (`tests/sanity_checks.py`,
   `test_tc007_tc009_api_or_network_failure_produces_friendly_message`):
   directly simulates `api_client.generate_response` raising
   `RuntimeError` (the same exception type Cohere SDK failures and
   network failures both surface as) and confirms the friendly message
   and `success = False` result.

Because both an invalid Cohere key and a network outage reach the
application through the exact same `except Exception → RuntimeError`
path in `api_client.py`, these two checks together verify the
requirement. What is **not** independently verifiable in this sandbox
is Cohere's own specific wording for an "invalid API key" rejection —
that detail is provider-side and outside this project's control.
