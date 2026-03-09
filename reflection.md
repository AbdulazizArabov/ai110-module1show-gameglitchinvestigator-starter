# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Answer: I noticed that when the application was booting, there are stickman icon that was changing until the application loadaded fully. The main page of the game was displayed and the game had apparent bugs.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
Answer: Logic bug — hints were inverted ("Go HIGHER" when too high, "Go LOWER" when too low), this function originally should have worked the right way but it was deliberately bugged.
 State bug — on even attempts, secret was cast to 'str' causing type-mismatch  
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Answer: Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Answer: I reviewed the code first and everything seemed to with no bugs but I asked claude to review the code and it found four bugs and I can tell you about Bug #1. I asked it to explain the problem and after I comprehended the bug, AI suggested fix. I reviewed it's suggestions and fixed the bug and claude was my assistant with finding the problem with code logic. I could verify the result by playing the game after the bug fix and seeing the code logic.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Answer: First, I understood the program and the bug well. Then I asked for suggestion from claude.ai. I asked 
correct promps and demanded related and correct fixed. There was no incorrect suggestions. I verified everything by playing the game and reading the code logic
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Answer: After fixing the bug I went to play the Glitchy Guesser Game. I also read the fixed part of the code and tried to comphrehend it's logic. I came to this conclusion after multiple test cases. I wrote those test cases to verify that the bug is fixed. I wrote test case for each bug and tests were successful.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
Answer:   Test I ran: test_too_high using pytest
                                                                                        def test_too_high():
      result = check_guess(80, 50)
      assert result == "Too High"

  What it showed: When I first wrote this test, I accidentally swapped the arguments — check_guess(50, 80) — which made the test fail with:

  AssertionError: assert 'Too Low' == 'Too High'

  This showed me that argument order matters — check_guess(guess, secret) — and that the test failure immediately revealed my mistake. After swapping to check_guess(80, 50), the test passed, confirming that Bug #1 (inverted hints) was correctly fixed.

- Did AI help you design or understand any tests? How?
Answer: I ran 2 types of tests for two bugs, I ran 7 tests from which 3 are Unit tests and the other four are regression tests. I learned how to design and write unit tests for firt time. AI helped to undertand that tests are crucial to verify that the problem was fixed.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
