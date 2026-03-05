# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
python -m streamlit run app.py

# Run all tests
pytest

# Run a single test
pytest tests/test_game_logic.py::test_winning_guess
```

## Project Purpose

This is an intentionally broken number-guessing game built with Streamlit, used as a learning exercise. Students must find and fix bugs, then refactor logic into `logic_utils.py`.

## Architecture

- **`app.py`** — Streamlit UI and session state management. Contains working implementations of all four logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`). This is the reference for what logic_utils.py should contain.
- **`logic_utils.py`** — Stub file where students must refactor the logic functions from `app.py`. All four functions currently raise `NotImplementedError`.
- **`tests/test_game_logic.py`** — Imports `check_guess` from `logic_utils` and tests it. Tests only check the first return value (outcome string), not the full `(outcome, message)` tuple that `app.py`'s version returns.

## Known Intentional Bugs (for student investigation)

1. **State bug** (`app.py:158-161`): On even-numbered attempts, `secret` is cast to `str`, causing type-mismatch comparisons in `check_guess` and making the game nearly unwinnable.
2. **Logic bug** (`app.py:37-40`): `check_guess` hints are inverted — "Go HIGHER" when guess is too high, "Go LOWER" when too low.
3. **Difficulty range bug** (`app.py:9`): Hard mode returns range `1–50` but the UI always displays `1–100`.
4. **Score bug** (`app.py:52`): Win score uses `attempt_number + 1` instead of `attempt_number`, miscounting attempts.
5. **New game bug** (`app.py:135`): "New Game" resets `attempts` to `0` instead of `1`, misaligning attempt counting.

## Test Contract

`tests/test_game_logic.py` expects `check_guess(guess, secret)` to return just the outcome string (`"Win"`, `"Too High"`, `"Too Low"`), not the `(outcome, message)` tuple. When refactoring into `logic_utils.py`, the return signature must match what the tests expect.
