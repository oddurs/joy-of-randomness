# Exercises: What Does Random Even Look Like?

---

## 2.1: Counting Runs (Warm-up)

Write a function `count_runs(sequence)` that counts the number of runs in a binary sequence. A run is a maximal sequence of identical outcomes.

For example:
- `count_runs("HHHTTHT")` should return `4` (runs: "HHH", "TT", "H", "T")
- `count_runs("HTHTH")` should return `5` (each flip is its own run)
- `count_runs("HHHHH")` should return `1` (one long run)

Test your function with both hand-generated and machine-generated sequences.

---

## 2.2: Longest Streak (Warm-up)

Implement `longest_streak(sequence)` that returns the length of the longest run of identical outcomes.

Generate 100 coin flips. What's the longest streak? Generate 1000 coin flips. What's the longest streak now? How much longer is it? Why?

---

## 2.3: Human vs. Machine (Exploration)

Write down a "random" sequence of 100 heads and tails. Don't flip anything—use your intuition.

Then generate a truly random sequence of 100 coin flips. Compare the two:

```python
# Compute for both:
num_runs_hand = count_runs(your_hand_sequence)
num_runs_machine = count_runs(machine_sequence)
longest_hand = longest_streak(your_hand_sequence)
longest_machine = longest_streak(machine_sequence)
```

Which sequence has more runs? Why do you think that is? Count how many times each sequence switches from heads to tails. What's the pattern?

---

## 2.4: Distribution of Streaks (Exploration)

Generate 10,000 sequences of 100 flips each. For each, compute the longest streak. Plot the distribution.

What's the most common longest streak length? What's the average? What percentage of sequences have a longest streak of 8 or more? Use this to build intuition about what a "suspicious" streak length really is.

---

## 2.5: The Runs Test (Challenge)

In the chapter, we derived that for a fair process with $n$ flips, the expected number of runs is roughly $\frac{n}{2} + 1$.

Implement this formula. Generate 100 sequences of 100 flips each. For each, compute:
- Observed number of runs
- Expected number of runs (using the formula)
- Difference

Plot the histogram of differences. Do all sequences fall within what you'd expect, or do some look suspicious? Try implementing a simple "runs test" that flags a sequence as suspicious if it's more than 2 standard deviations from the expected value.

$$\text{StdDev} \approx \frac{1}{2}\sqrt{\frac{n}{2}}$$

---

## 2.6: Biased Coins (Challenge)

Modify your simulation to generate sequences from a *biased* coin (e.g., 60% heads, 40% tails).

How does the distribution of longest streaks change? How does the runs test perform—does it flag biased sequences as suspicious? What if the coin is only slightly biased (51% heads)?

---

## 2.7: Pattern Hunting (Challenge)

Pick a specific pattern (e.g., "HTH" or "HHHH") and search for it in random sequences.

Generate 1000 sequences of 100 flips. For each, find the position of the first occurrence of your pattern. What's the average position? Does it match what you'd theoretically expect?

Bonus: What about overlapping occurrences? Does "HHH" appear at the same rate as "HTH"?

---

## 2.8: When Is a Sequence "Too Random"? (Thought Experiment)

Suppose you flip a coin 100 times and get exactly 50 heads and 50 tails, with runs alternating perfectly: HTHTH...TH.

Is this sequence random? Why or why not? If you were a casino and saw this sequence from your random number generator, would you be concerned? What does this tell you about what "too balanced" means?

---

## 2.9: The Gambler's Intuition (Thought Experiment)

You've just watched a coin come up heads seven times in a row. You know it's a fair coin. Is tails now more likely on the next flip?

Explain your answer using what you've learned about randomness and runs. What would a friend need to understand to avoid the gambler's fallacy?

---

## 2.10: Automating Randomness Checks (Challenge)

You have a file of 1000 binary sequences. Write a program that:
1. Computes the number of runs in each sequence
2. Computes the expected value and standard deviation
3. Flags any sequence that's more than 2 standard deviations from the expected value
4. Reports how many sequences were flagged as "suspicious"

If all sequences pass the test, can you be confident they came from a fair source? Why or why not?
