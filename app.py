import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# Maps each difficulty to a maximum number of allowed attempts.
# Edge case: if difficulty is an unexpected value not in this map,
# this will raise a KeyError — only "Easy", "Normal", "Hard" are valid.
attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIXME Bug #5: attempts started at 1, so first submit incremented to 2, miscounting score
    # Fixed: start at 0 so first submit correctly becomes attempt 1
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_count" not in st.session_state:
    # FIXME Bug #8: input field was not cleared on New Game — fixed by tracking game_count in key
    st.session_state.game_count = 0

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

if "end_message" not in st.session_state:
    st.session_state.end_message = None

st.subheader("Make a guess")

st.info(
    # FIXME Bug #3: range was hardcoded to "1 and 100" — now uses {low} and {high} from get_range_for_difficulty.
    # Fixed!
    # FIXME Bug #11: attempts left could show negative — clamped to minimum of 0
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_count}"
)

col1, col2, col3 = st.columns(3)
with col1:
    
    submit = st.button("Submit Guess 🚀", disabled=st.session_state.status != "playing")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if show_hint and st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

if new_game:
    # FIXME Bug #6: New Game did not reset status, history, and used hardcoded range instead of difficulty range
    # FIXME Bug #13: score was never reset on New Game — now resets to 0
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.last_hint = None
    st.session_state.end_message = None
    st.session_state.game_count += 1  # changes input key → clears the text input
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(st.session_state.end_message or "You already won. Start a new game to play again.")
    else:
        st.error(st.session_state.end_message or "Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIXME Bug #12: invalid inputs (empty, non-numeric) were being saved to history
        # Fixed: only valid guesses are recorded
        st.error(err)
    else:
        # FIXME Bug #7: attempts incremented before validation, wasting attempts on invalid input
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXME Bug #2: secret was cast to str on even attempts, breaking int comparison with guess.
        # Bug #2 FIXED.
        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)

        st.session_state.last_hint = HINT_MESSAGES[outcome]

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.end_message = (
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.session_state.end_message = (
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            st.rerun()

# FIXME Bug #9: debug info was above the submit block — history always showed one guess behind
# Fixed: moved to bottom so history reflects the current attempt
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
