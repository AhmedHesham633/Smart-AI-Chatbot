# Acceptance Checklist — Smart AI Chatbot

## API
- [x] Real AI API is integrated (Cohere, `ClientV2.chat`).
- [x] Provider/model is documented (README: `command-a-03-2025`).
- [x] API response is parsed correctly (`response.message.content[0].text`).
- [x] API errors are handled (`ValueError` for missing key, `RuntimeError` for everything else).

## Input
- [x] Normal input works (TC-001).
- [x] Empty input is rejected (TC-003).
- [x] Whitespace input is rejected (TC-004).
- [x] Exit command works — `exit`, `quit`, `/exit`, case-insensitive (TC-005).

## Conversation
- [x] History is maintained (`prompts.update_history`).
- [x] Multi-turn conversation works, with prior context sent to the API (TC-002).
- [x] History order is correct — user then assistant, per turn (TC-006, TC-011).
- [x] No duplicate messages (TC-006, TC-012).

## Security
- [x] No hardcoded API key (verified by source grep).
- [x] `.env` is ignored (`.gitignore`).
- [x] `.env.example` exists with a placeholder value.
- [x] No credentials appear in documentation.
- [x] No credentials appear in tests. Git history was also checked and no
      credentials were found in any prior commit.

## Reliability
- [x] API failure handled (TC-009).
- [x] Missing credential handled (TC-008).
- [x] Invalid credential handled — same code path as API/network
      failure; see the note in `requirements_traceability.md` on the
      sandbox's network restrictions (TC-007).
- [x] Unexpected/other response errors handled (generic exception fallback test).

## Code Quality
- [x] Modular architecture (`chatbot.py` / `api_client.py` / `prompts.py` / `utils.py`).
- [x] Clear naming throughout.
- [x] No unnecessary duplication found.
- [x] No dead code found.
- [x] No unnecessary dependencies (all four `requirements.txt` entries are used: `cohere`, `python-dotenv`, `streamlit`, `pytest`).
- [x] Imports work correctly (`pytest tests/ -v` collects and runs cleanly).

## Reproducibility
- [x] `requirements.txt` installs cleanly in a fresh virtual environment (verified: `python -m venv .venv && pip install -r requirements.txt`).
- [x] Fresh environment can install dependencies.
- [x] README explains setup.
- [x] Application can be started from the documented command (`python main.py`, `streamlit run app.py`).

## Documentation
- [x] README complete.
- [x] Architecture explained.
- [x] Environment variables documented.
- [x] Run instructions documented.
- [x] Testing instructions documented.
- [x] Limitations documented.
