import pytest
from logic_utils import check_guess

# These are Unit test for first bug I found about Hint
def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"

def test_too_high():
    result = check_guess(80, 50)
    assert result =="Too High"

def test_too_low():
    result = check_guess(30, 50)
    assert result == "Too Low"


# Bug #1: hints were inverted — "Go HIGHER" when guess was too high, "Go LOWER" when too low
def test_bug1_high_guess_not_inverted():
    # Before fix: check_guess(60, 50) incorrectly returned "Too Low"
    result = check_guess(60, 50)
    assert result == "Too High", "Bug #1: high guess should return 'Too High', not 'Too Low'"

def test_bug1_low_guess_not_inverted():
    # Before fix: check_guess(40, 50) incorrectly returned "Too High"
    result = check_guess(40, 50)
    assert result == "Too Low", "Bug #1: low guess should return 'Too Low', not 'Too High'"

# Bug #2: secret was cast to str on even attempts, breaking int comparison
def test_bug2_int_secret_wins():
    # Before fix: secret was sometimes "50" (str), so 50 == "50" was False and never won
    result = check_guess(50, 50)
    assert result == "Win", "Bug #2: int guess vs int secret should return 'Win'"

def test_bug2_str_secret_breaks_comparison():
    # Demonstrates the original bug — passing str secret causes a TypeError in Python 3
    with pytest.raises(TypeError):
        check_guess(50, "50")



# def test_winning_guess():
#     # If the secret is 50 and guess is 50, it should be a win
#     result = check_guess(50, 50)
#     assert result == "Win"

# def test_guess_too_high():
#     # If secret is 50 and guess is 60, hint should be "Too High"
#     result = check_guess(60, 50)
#     assert result == "Too High"

# def test_guess_too_low():
#     # If secret is 50 and guess is 40, hint should be "Too Low"
#     result = check_guess(40, 50)
#     assert result == "Too Low"
