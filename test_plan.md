# Test Plan — Smart AI Chatbot

## 1. Objective

Verify that the Smart AI Chatbot meets its functional requirements —
input validation, conversation history, prompt construction, API
integration, response parsing, error handling, and clean exit — and
that the three members' components (API client, prompts/history,
chatbot logic) integrate correctly end to end.

## 2. Scope

In scope:
- Input validation (empty, whitespace, normal, exit commands)
- Conversation history construction, ordering, and reuse across turns
- Prompt construction (system prompt + history + new message)
- API client behavior: successful calls, missing key, invalid
  key/network failure, empty/unexpected responses
- Error handling and application stability across all of the above
- Integration between `src/chatbot.py`, `src/prompts.py`,
  `src/api_client.py`, `src/utils.py`, and both entry points
  (`main.py`, `app.py`)
- Credential handling and secret hygiene (`.env`, `.gitignore`,
  `.env.example`, source, tests, README)

Out of scope:
- Model quality/accuracy of Cohere's responses (not something this
  project controls or should test)
- Load/performance/stress testing
- UI/visual regression testing of the Streamlit front end
- Any provider other than Cohere
- RAG, fine-tuning, agents, vector databases, cloud deployment — not
  part of this project's requirements

## 3. Test Environment

- Python 3.12, virtual environment (`.venv`)
- Dependencies from `requirements.txt` (`cohere`, `python-dotenv`,
  `streamlit`, `pytest`)
- `pytest` for automated tests
- Automated tests mock `src.chatbot.generate_response` — they do not
  require a real `COHERE_API_KEY` or network access
- `test_api.py` (manual, optional) requires a real `COHERE_API_KEY`
  and outbound network access to the Cohere API

## 4. Test Categories

| Category | Description | Where |
|---|---|---|
| Unit — validation & exit | Input validation, exit-command detection | `tests/chatbot_test.py` |
| Unit — single reply | `get_bot_reply` happy path + one error path | `tests/chatbot_test.py` |
| Integration — history/prompt | Multi-turn history, prompt structure, response parsing | `tests/sanity_checks.py` |
| Integration — error handling | Missing key, invalid key/network failure, unexpected exceptions | `tests/sanity_checks.py` |
| Manual — end-to-end CLI | Running `main.py` with piped input | Performed during QA (see report) |
| Manual — real API | One live call to Cohere | `test_api.py` (optional, requires credentials) |
| Security review | Credential hygiene, `.gitignore`, git history scan | Performed during QA (see report) |

## 5. Test Cases

See `requirements_traceability.md` for the full TC-001 through TC-012
list mapped to requirements, implementation, and results.

## 6. Acceptance Criteria

- All automated tests in `tests/` pass (`pytest tests/ -v`).
- The terminal app (`main.py`) runs end to end without crashing for:
  normal input, empty input, whitespace input, and each exit command.
- No hardcoded credentials exist anywhere in the repository or its
  git history.
- `.env` is git-ignored and `.env.example` contains placeholders only.
- Every requirement in `requirements_traceability.md` is marked PASS
  or explicitly marked NOT VERIFIABLE with a stated reason — none are
  left unassessed.
