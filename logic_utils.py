# FIX: I have refatored logic into logic_utils.py using Claude Agent mode.


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty level.

    Maps a difficulty label to the lower and upper bounds of the secret number
    range used during a game session. Unrecognised difficulty strings fall back
    to the Normal range.

    Args:
        difficulty (str): The difficulty label selected by the player.
            Supported values: ``"Easy"``, ``"Normal"``, ``"Hard"``.

    Returns:
        tuple[int, int]: A ``(low, high)`` pair representing the inclusive
        bounds of the secret number range.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Normal")
        (1, 100)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts whole-number strings as well as decimal strings (e.g. ``"7.0"``),
    truncating the fractional part via ``int(float(raw))``. Returns a
    three-element tuple so the caller can distinguish success from failure
    without raising an exception.

    Args:
        raw (str | None): The raw text entered by the player. May be ``None``
            or an empty string when the input field has not been filled in.

    Returns:
        tuple[bool, int | None, str | None]: A three-element tuple
        ``(ok, guess_int, error_message)`` where:

        * ``ok`` (bool) — ``True`` if parsing succeeded, ``False`` otherwise.
        * ``guess_int`` (int | None) — The parsed integer value when
          ``ok`` is ``True``; ``None`` on failure.
        * ``error_message`` (str | None) — A human-readable description of
          the validation failure when ``ok`` is ``False``; ``None`` on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.9")
        (True, 3, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess(None)
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare a player's guess to the secret number and return the outcome.

    Performs a simple three-way comparison and maps the result to one of three
    canonical outcome strings consumed by both the UI and the test suite.

    Args:
        guess (int): The integer value submitted by the player.
        secret (int): The secret number the player is trying to guess.

    Returns:
        str: One of three outcome strings:

        * ``"Win"`` — the guess exactly matches the secret.
        * ``"Too High"`` — the guess is greater than the secret.
        * ``"Too Low"`` — the guess is less than the secret.

    Examples:
        >>> check_guess(50, 50)
        'Win'
        >>> check_guess(75, 50)
        'Too High'
        >>> check_guess(25, 50)
        'Too Low'
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return the new cumulative score after a guess attempt.

    Scoring rules:
    * **Win** — awards ``max(100 - 10 * (attempt_number - 1), 10)`` points,
      so a first-attempt win scores 100, a second-attempt win scores 90, and
      the minimum award per win is 10 points regardless of attempt count.
    * **Too High / Too Low** — no points are added or deducted; the score is
      returned unchanged.

    Args:
        current_score (int): The player's score before this attempt.
        outcome (str): The result of the guess — one of ``"Win"``,
            ``"Too High"``, or ``"Too Low"``.
        attempt_number (int): The 1-based index of the current attempt
            (1 for the first guess, 2 for the second, and so on).

    Returns:
        int: The updated cumulative score after applying the outcome.

    Examples:
        >>> update_score(0, "Win", 1)
        100
        >>> update_score(100, "Win", 2)
        190
        >>> update_score(50, "Too High", 3)
        50
        >>> update_score(50, "Too Low", 3)
        50
        >>> update_score(0, "Win", 11)
        10
    """
    if outcome == "Win":
        # FIXME Bug #4: win score deducted 10 points per attempt including the first
        # Fixed: first attempt scores 100, each subsequent attempt deducts 10
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME Bug #10: wrong guesses were deducting 5 points from score on every attempt
    # Fixed: score only changes on a win — wrong guesses do not affect score
    if outcome == "Too High":
        return current_score

    if outcome == "Too Low":
        return current_score

    return current_score
