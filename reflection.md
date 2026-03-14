# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  Answer: There were apparent inconsistencies and randomized results nad point decutions, so there were many problems to fix at first glance. I also noticed that when the application was booting, there are stickman icon that was changing until the application loadaded fully. The main page of the game was displayed and the game had apparent bugs.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  Answer: Logic bug — hints were inverted ("Go HIGHER" when too high, "Go LOWER" when too low), this function originally should have worked the right way but it was deliberately bugged.
State bug — on even attempts, secret was cast to 'str' causing type-mismatch  
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Answer: Claude and Github Copilot

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Answer: I reviewed the code first and everything seemed to with no bugs but I asked claude to review the code and it found many bugs and I can tell you about Bug #1. I asked it to explain the problem and after I comprehended the bug, AI suggested fix. I reviewed it's suggestions and fixed the bug and claude was my assistant with finding the problem with code logic and pinpoint the line of code because of which there was a bug . I could verify the result by playing the game after the bug fix and seeing the code logic. Additionaly, AI assisted me with writing tests such as unit test and regression tests to verify that the bug is fixed and it will not come back again. I ran those tests and they were successful.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  Answer: When I asked AI to review the score logic, it told me everything looked fine and was working correctly. I trusted that and moved on, but during manual testing I noticed the score was still behaving wrong — points were being deducted even when I guessed correctly on the first attempt, and the deduction amounts were inconsistent. I went back to AI with the specific problem, but even its first fix suggestion did not fully resolve it. I had to read the code myself, trace the exact lines causing the issue, and correct it on my own with AI as a helper to pinpoint the line of code where bug was present. I verified the final result by playing multiple games and confirming the score only changed on a win with the correct amount deducted per attempt(if win from the first attempt, then no deductions).
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  Answer: After fixing the bug I went to play the Glitchy Guesser Game. I also read the fixed part of the code and tried to comphrehend it's logic. I came to this conclusion after multiple game sessions and test cases. I wrote those test cases to verify that the bug is fixed. I wrote test case for each bug and tests were successful.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  Answer:   Test I ran: test_too_high using pytest
  
    def test_too_high():  /n
      result = check_guess(80, 50) /n
      assert result == "Too High" /n

  What it showed: When I first wrote this test, I accidentally swapped the arguments — check_guess(50, 80) — which made the test fail with:

  AssertionError: assert 'Too Low' == 'Too High'

  This showed me that argument order matters — check_guess(guess, secret) — and that the test failure immediately revealed my mistake. After swapping to check_guess(80, 50), the test passed, confirming that Bug #1 (inverted hints) was correctly fixed.

- Did AI help you design or understand any tests? How?
  Answer: I had never written tests before this project, so AI was essential in helping me understand where to start. It explained the difference between unit tests and regression tests, helped me structure each test case, and showed me how to write assertions that actually verify the right thing. At first I only had 7 tests covering 2 bugs, but with AI guiding me through the process I ended up with 43 tests covering all 13 bugs, including AppTest-based tests that simulate real user interactions in the Streamlit app. Without AI walking me through it, It would take me longer to apply these tests in this appliation.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  Answer: When I first ran the app and started guessing, I noticed the hints made no sense — like I would guess higher and somehow still be wrong in the same direction. Eventually I realized the secret number itself was changing every time I clicked Submit. The reason was that `random.randint()` was sitting at the top of the script with nothing protecting it, so every time I interacted with the app, Streamlit reran the whole script and picked a brand new secret number. It was basically a rigged game.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Answer: I would tell them to think of it like this — every time you click anything in a Streamlit app, the entire Python file runs again from line 1. Any normal variable you had just gets wiped and recreated. Session state is the fix for that. It is like a small storage box that does not get thrown out on each rerun. So if you put your secret number in there, it stays the same whether you click Submit once or ten times.

- What change did you make that finally gave the game a stable secret number?
  Answer: The fix was pretty simple once I understood the problem. I wrapped the random number generation in a check: `if "secret" not in st.session_state`. That way, the first time the app loads it creates a secret and stores it in session state. Every rerun after that, it sees the secret already exists and skips generating a new one. That one change made the whole game actually playable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  Answer: Writing tests for every bug I fix. Before this project I would fix something and just assume it worked. Now I know that a fix without a test is just a guess — the bug can come back in a later change and you would never know. In this project, having 43 tests meant I could change the app with confidence and immediately know if something broke. I want to carry that habit into every future project.

  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Answer: Yes, I want to keep writing tests and using Git consistently. I have already been using Git for a while, but this project taught me to commit at meaningful checkpoints — after each bug fix — so I always have a clean version to go back to if something breaks.

- What is one thing you would do differently next time you work with AI on a coding task?
  Answer: Next time I would not trust AI's first response at face value, especially when it says everything looks fine. In this project, AI reviewed the score logic and told me it was correct — but it was not. That cost me extra time because I moved on before catching the issue myself. Going forward I want to verify AI suggestions by testing them immediately rather than assuming they are right.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  Answer: Before this project I assumed AI generated code was mostly correct and only needed small tweaks. After finding and fixing 13 bugs — some of which AI missed entirely or gave wrong fixes for — I now treat AI generated code the same way I treat any code I did not write myself: I read it, question it, and test it before trusting it.

---


## EXTRA REFLECTION FROM ME -- 6. AI Model Comparison: Claude vs GitHub Copilot

- **Claude** was the primary AI assistant throughout this project. It excelled at explaining bug root causes in plain language, helping structure tests, and walking through logic step by step. However, when reviewing the score logic it incorrectly reported that everything looked fine — missing the `attempt_number + 1` off-by-one error that was causing wrong point deductions.

- **GitHub Copilot** worked differently — rather than conversational explanations, it surfaced inline suggestions directly in the editor. It was more helpful for catching the score bug that Claude missed, flagging the specific line where `attempt_number + 1` should have been `attempt_number`. Copilot's strength was spotting small, localized code mistakes rather than explaining the bigger picture.

- **Key takeaway:** Neither tool was reliable on its own. Claude gave better explanations and test guidance, while Copilot caught line-level mistakes Claude overlooked. Using both together — and always verifying with manual testing — gave better results than relying on either one alone. 
At the end of the day, this reflection (Extra part 6) was written based on my personal experience. I am well informed that either model can suggest in-line corrections and find out which line of code is not functioning properly, but in this project, each model had advantage over the other in different aspects. I will continue to use both models in future projects, leveraging their respective strengths while being mindful of their limitations.

---
