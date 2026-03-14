import pytest
from streamlit.testing.v1 import AppTest
from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess

# ── Basic unit tests ──────────────────────────────────────────────────────────

def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"

def test_too_high():
    result = check_guess(80, 50)
    assert result == "Too High"

def test_too_low():
    result = check_guess(30, 50)
    assert result == "Too Low"

# ── Bug #1: hints were inverted ───────────────────────────────────────────────

def test_bug1_high_guess_not_inverted():
    # Before fix: check_guess(60, 50) incorrectly returned "Too Low"
    result = check_guess(60, 50)
    assert result == "Too High", "Bug #1: high guess should return 'Too High', not 'Too Low'"

def test_bug1_low_guess_not_inverted():
    # Before fix: check_guess(40, 50) incorrectly returned "Too High"
    result = check_guess(40, 50)
    assert result == "Too Low", "Bug #1: low guess should return 'Too Low', not 'Too High'"

# ── Bug #2: secret cast to str on even attempts ───────────────────────────────

def test_bug2_int_secret_wins():
    # Before fix: secret was sometimes "50" (str), so 50 == "50" was always False
    result = check_guess(50, 50)
    assert result == "Win", "Bug #2: int guess vs int secret should return 'Win'"

def test_bug2_str_secret_breaks_comparison():
    # Demonstrates the original bug — passing str secret causes a TypeError in Python 3
    with pytest.raises(TypeError):
        check_guess(50, "50")

# ── Bug #3: difficulty range hardcoded to 1-100 ───────────────────────────────

def test_bug3_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20, "Bug #3: Easy range should be 1-20"

def test_bug3_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100, "Bug #3: Normal range should be 1-100"

def test_bug3_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 50, "Bug #3: Hard range should be 1-50"

# ── Bug #4: win score used attempt_number + 1 ─────────────────────────────────

def test_bug4_win_on_first_attempt():
    # First attempt should give full 100 points — no deduction
    score = update_score(0, "Win", 1)
    assert score == 100, "Bug #4: winning on attempt 1 should give 100 points"

def test_bug4_win_on_second_attempt():
    # Second attempt deducts 10 → 90 points
    score = update_score(0, "Win", 2)
    assert score == 90, "Bug #4: winning on attempt 2 should give 90 points"

# ── Bug #5: attempts started at 1 instead of 0 ───────────────────────────────

def test_bug5_first_attempt_score():
    # After fix: attempts starts at 0, first submit increments to 1
    # Winning on first guess → 100 points, no deduction
    score = update_score(0, "Win", 1)
    assert score == 100, "Bug #5: first attempt should score 100, not 90"

# ── Bug #6: New Game button did not reset status, history, or use correct range ──

def test_bug6_hard_range_not_hardcoded():
    low, high = get_range_for_difficulty("Hard")
    assert high == 50, "Bug #6: Hard mode new game secret should use range 1-50, not 1-100"

def test_bug6_easy_range_not_hardcoded():
    low, high = get_range_for_difficulty("Easy")
    assert high == 20, "Bug #6: Easy mode new game secret should use range 1-20, not 1-100"

def test_bug6_new_game_resets_status():
    # After New Game, status should be "playing" again
    at = AppTest.from_file("../app.py").run()
    at.session_state.status = "lost"
    at.run()
    at.button[1].click().run()
    assert at.session_state.status == "playing", "Bug #6: New Game should reset status to 'playing'"

def test_bug6_new_game_resets_history():
    # After New Game, history should be empty
    at = AppTest.from_file("../app.py").run()
    at.session_state.history = [10, 20, 30]
    at.run()
    at.button[1].click().run()
    assert at.session_state.history == [], "Bug #6: New Game should clear guess history"

def test_bug6_win_score_resets_to_zero():
    score = update_score(0, "Win", 1)
    assert score == 100, "Bug #6: fresh game win on attempt 1 should score 100"

# ── Bug #7: attempts incremented before validation ────────────────────────────

def test_bug7_invalid_text_does_not_increment_attempts():
    # Submitting non-numeric text should not count as an attempt
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].set_value("abc")
    at.button[0].click().run()
    assert at.session_state.attempts == 0, "Bug #7: non-numeric input should not increment attempts"

def test_bug7_empty_input_does_not_increment_attempts():
    # Submitting empty input should not count as an attempt
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].set_value("")
    at.button[0].click().run()
    assert at.session_state.attempts == 0, "Bug #7: empty input should not increment attempts"

def test_bug7_valid_input_increments_attempts():
    # A real number guess should count as one attempt
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("42")
    at.button[0].click().run()
    assert at.session_state.attempts == 1, "Bug #7: valid guess should increment attempts to 1"

# ── Bug #8: input field not cleared on New Game ───────────────────────────────

def test_bug8_input_cleared_on_new_game():
    # After clicking New Game, the text input should be empty
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].set_value("42")
    at.button[1].click().run()
    assert at.text_input[0].value == "", "Bug #8: input field should be cleared after New Game"

# ── Bug #9: debug history showed one guess behind ─────────────────────────────

def test_bug9_history_reflects_current_attempt():
    # After submitting a guess, history should immediately contain that guess
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("42")
    at.button[0].click().run()
    assert 42 in at.session_state.history, "Bug #9: history should contain the guess just submitted"

# ── Bug #10: wrong guesses deducted score ─────────────────────────────────────

def test_bug10_too_high_does_not_deduct_score():
    # A "Too High" outcome should leave the score unchanged
    score = update_score(100, "Too High", 1)
    assert score == 100, "Bug #10: 'Too High' should not deduct score"

def test_bug10_too_low_does_not_deduct_score():
    # A "Too Low" outcome should leave the score unchanged
    score = update_score(100, "Too Low", 1)
    assert score == 100, "Bug #10: 'Too Low' should not deduct score"

def test_bug10_wrong_guess_score_unchanged_in_app():
    # In the running app, a wrong guess should not change the score from 0
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("1")
    at.button[0].click().run()
    assert at.session_state.score == 0, "Bug #10: wrong guess should not deduct from score"

# ── Bug #11: attempts left showed negative ────────────────────────────────────

def test_bug11_attempts_left_not_negative():
    # Even after exceeding the attempt limit, "Attempts left" should show 0, not negative
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    for i in range(1, 10):
        if at.session_state.status != "playing":
            break
        at.text_input[0].set_value(str(i))
        at.button[0].click().run()
    for info_widget in at.info:
        assert "Attempts left: -" not in info_widget.value, \
            "Bug #11: attempts left should never display a negative number"

# ── Bug #12: invalid inputs saved to history ──────────────────────────────────

def test_bug12_empty_string_is_invalid():
    ok, _, _ = parse_guess("")
    assert not ok, "Bug #12: empty string should not be a valid guess"

def test_bug12_text_input_is_invalid():
    ok, _, _ = parse_guess("abc")
    assert not ok, "Bug #12: non-numeric text should not be a valid guess"

def test_bug12_none_input_is_invalid():
    ok, _, _ = parse_guess(None)
    assert not ok, "Bug #12: None should not be a valid guess"

def test_bug12_invalid_input_not_added_to_history():
    # An invalid submission should not appear in the guess history
    at = AppTest.from_file("../app.py").run()
    at.text_input[0].set_value("abc")
    at.button[0].click().run()
    assert len(at.session_state.history) == 0, \
        "Bug #12: invalid input should not be recorded in history"

# ── Bug #13: score not reset on New Game ──────────────────────────────────────

def test_bug13_score_resets_on_new_game():
    # Score should go back to 0 when a new game is started
    at = AppTest.from_file("../app.py").run()
    at.session_state.score = 50
    at.run()
    at.button[1].click().run()
    assert at.session_state.score == 0, "Bug #13: score should reset to 0 on New Game"

# ── Attempts left display decrements correctly after each guess ───────────────

def test_attempts_left_decrements_after_guess():
    # After one valid wrong guess, attempts left should decrease by 1
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("1")
    at.button[0].click().run()
    assert at.session_state.attempts == 1, \
        "Attempts left: counter should be 1 after first guess"

def test_attempts_left_display_not_stale():
    # After a valid guess, info should reflect updated attempts count
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("1")
    at.button[0].click().run()
    for info_widget in at.info:
        assert "Attempts left: 7" in info_widget.value, \
            "Attempts left should show 7 after first guess in Normal mode (8 - 1)"

# ── Hint stored in session state after guess ──────────────────────────────────

def test_hint_stored_in_session_state_too_low():
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    at.text_input[0].set_value("1")
    at.button[0].click().run()
    assert at.session_state.last_hint == "📈 Go HIGHER!", \
        "last_hint should be set to 'Go HIGHER!' when guess is too low"

def test_hint_stored_in_session_state_too_high():
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 1
    at.run()
    at.text_input[0].set_value("99")
    at.button[0].click().run()
    assert at.session_state.last_hint == "📉 Go LOWER!", \
        "last_hint should be set to 'Go LOWER!' when guess is too high"

def test_new_game_clears_last_hint():
    # New Game should clear the last hint
    at = AppTest.from_file("../app.py").run()
    at.session_state.last_hint = "📈 Go HIGHER!"
    at.run()
    at.button[1].click().run()
    assert at.session_state.last_hint is None, \
        "last_hint should be None after New Game"

# ── End message stored in session state on win/lose ───────────────────────────

def test_end_message_set_on_win():
    # Winning should store end_message with secret and score
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 42
    at.run()
    at.text_input[0].set_value("42")
    at.button[0].click().run()
    assert at.session_state.end_message is not None, \
        "end_message should be set after winning"
    assert "42" in at.session_state.end_message, \
        "end_message should contain the secret number"

def test_end_message_set_on_loss():
    # Losing should store end_message
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 99
    at.run()
    for i in range(1, 9):
        if at.session_state.status != "playing":
            break
        at.text_input[0].set_value(str(i))
        at.button[0].click().run()
    assert at.session_state.end_message is not None, \
        "end_message should be set after losing"

def test_new_game_clears_end_message():
    # New Game should clear end_message from previous game
    at = AppTest.from_file("../app.py").run()
    at.session_state.end_message = "You won! The secret was 42. Final score: 100"
    at.run()
    at.button[1].click().run()
    assert at.session_state.end_message is None, \
        "end_message should be None after New Game"

# ── Submit button disabled when game is over ──────────────────────────────────

def test_submit_disabled_when_lost():
    # Submit button should be disabled after game is lost
    at = AppTest.from_file("../app.py").run()
    at.session_state.status = "lost"
    at.run()
    assert at.button[0].disabled, \
        "Submit button should be disabled when status is 'lost'"

def test_submit_disabled_when_won():
    # Submit button should be disabled after game is won
    at = AppTest.from_file("../app.py").run()
    at.session_state.status = "won"
    at.run()
    assert at.button[0].disabled, \
        "Submit button should be disabled when status is 'won'"

def test_submit_enabled_when_playing():
    # Submit button should be enabled during an active game
    at = AppTest.from_file("../app.py").run()
    assert not at.button[0].disabled, \
        "Submit button should be enabled when status is 'playing'"
