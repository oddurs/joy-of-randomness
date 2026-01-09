# Solutions: What Does Random Even Look Like?

---

## 2.1: Counting Runs

**Solution:**

```python
def count_runs(sequence):
    """Count the number of runs in a sequence."""
    if not sequence:
        return 0
    
    num_runs = 1
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            num_runs += 1
    
    return num_runs

# Test cases
print(count_runs("HHHTTHT"))    # Expected: 4
print(count_runs("HTHTH"))      # Expected: 5
print(count_runs("HHHHH"))      # Expected: 1
```

**Explanation:**

We iterate through the sequence. Whenever we see a flip that differs from the previous one, we've exited a run and entered a new one. We count each time that happens, starting with 1 (for the first run).

The key insight: a sequence that alternates (H, T, H, T) has many runs. A sequence that clusters (HHHH, TTTT) has few runs. This difference tells us something about whether a sequence was hand-generated (which tends to alternate) or machine-generated (which tolerates clustering).

---

## 2.2: Longest Streak

**Solution:**

```python
def longest_streak(sequence):
    """Find the longest consecutive run of identical outcomes."""
    if not sequence:
        return 0
    
    current_length = 1
    max_length = 1
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length

# Generate 100 flips
import random
sequence_100 = [random.choice(['H', 'T']) for _ in range(100)]
print(f"Longest streak in 100 flips: {longest_streak(sequence_100)}")

# Generate 1000 flips
sequence_1000 = [random.choice(['H', 'T']) for _ in range(1000)]
print(f"Longest streak in 1000 flips: {longest_streak(sequence_1000)}")
```

**Explanation:**

When we have 100 flips, the longest streak averages around 7. When we have 1000 flips, it's typically 10-11. The longest streak grows, but slowly—roughly as the logarithm of the number of flips.

Why? Because each new flip gives us another opportunity to extend a streak. With ten times more flips, we don't get ten times longer streaks; the growth is much slower. This is why a streak of 20 in 10,000 flips is still perfectly normal—we've had so many opportunities to build long runs.

---

## 2.3: Human vs. Machine

**Solution:**

```python
import random

# Hand-generated sequence (example)
hand_sequence = "HTHTHTHHTTHTHHTTHTTHHTHTTHTHHTHTHHTTHHT"  # Your intuitive sequence

# Machine-generated sequence
machine_sequence = ''.join([random.choice(['H', 'T']) for _ in range(100)])

# Compare
print(f"Hand-generated:")
print(f"  Runs: {count_runs(hand_sequence)}")
print(f"  Longest streak: {longest_streak(hand_sequence)}")

print(f"\nMachine-generated:")
print(f"  Runs: {count_runs(machine_sequence)}")
print(f"  Longest streak: {longest_streak(machine_sequence)}")
```

**Typical result:**

- Hand-generated: 65-75 runs, longest streak of 3-4
- Machine-generated: 45-55 runs, longest streak of 7-9

**Explanation:**

Humans avoid long runs. We think "okay, that's enough heads, time for tails." We're uncomfortable with HHHH because it looks like a pattern (or bias). Real randomness doesn't have that discomfort—it lets runs happen naturally.

The machine tolerates clustering because each flip is independent. The previous flip doesn't influence the next, so we often get runs by pure chance. This is what fair randomness actually looks like.

---

## 2.4: Distribution of Streaks

**Solution:**

```python
import random
from collections import Counter
import statistics

# Generate 10,000 sequences of 100 flips each
streaks = []
for _ in range(10000):
    sequence = [random.choice(['H', 'T']) for _ in range(100)]
    streaks.append(longest_streak(sequence))

# Analyze the distribution
print(f"Average: {statistics.mean(streaks):.2f}")
print(f"Median: {statistics.median(streaks)}")
print(f"Most common: {Counter(streaks).most_common(1)[0][0]}")

# Count streaks of 8+
count_8_plus = sum(1 for s in streaks if s >= 8)
percentage_8_plus = (count_8_plus / len(streaks)) * 100
print(f"\nStreaks of 8 or more: {count_8_plus} ({percentage_8_plus:.1f}%)")

# Print distribution
print("\nFull distribution:")
for length in sorted(Counter(streaks).keys()):
    count = Counter(streaks)[length]
    pct = (count / len(streaks)) * 100
    print(f"  Streak {length}: {pct:5.1f}% ({count:4d})")
```

**Typical output:**

- Average longest streak: 7.1
- Median: 7
- Streaks of 8+: ~30%

**Intuition:**

So a streak of 8 in 100 flips is not rare—it happens 15-20% of the time. A streak of 9 happens maybe 8-10% of the time. This is crucial for developing good intuition about randomness. When you see a long streak, it doesn't mean the process is biased. It means the process is random.

---

## 2.5: The Runs Test

**Solution:**

```python
import random
import statistics
import math

def count_runs(sequence):
    if not sequence:
        return 0
    num_runs = 1
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            num_runs += 1
    return num_runs

def expected_runs(n):
    """Expected number of runs for a fair process."""
    return n / 2 + 1

def std_dev_runs(n):
    """Standard deviation of runs."""
    return 0.5 * math.sqrt(n / 2)

def runs_test(sequence, alpha=2.0):
    """
    Test if a sequence is random using the runs test.
    Returns True if the sequence passes (looks random).
    """
    n = len(sequence)
    observed = count_runs(sequence)
    expected = expected_runs(n)
    std_dev = std_dev_runs(n)
    
    z_score = abs(observed - expected) / std_dev
    return z_score <= alpha

# Generate 100 sequences and test them
sequences = [[random.choice([0, 1]) for _ in range(100)] for _ in range(100)]

passed = sum(1 for seq in sequences if runs_test(seq))
print(f"Sequences passing runs test: {passed} / 100")

# Calculate the differences
differences = []
for seq in sequences:
    observed = count_runs(seq)
    expected = expected_runs(len(seq))
    differences.append(observed - expected)

print(f"\nDifferences from expected:")
print(f"  Mean: {statistics.mean(differences):.2f}")
print(f"  Std Dev: {statistics.stdev(differences):.2f}")
print(f"  Min: {min(differences)}, Max: {max(differences)}")
```

**Explanation:**

The runs test compares what we observe to what we'd expect from a fair process. The expected value assumes independence and fairness. If the number of runs is far from what we expect, that's suspicious.

In practice, nearly all fair sequences pass the test (we'd expect ~95% to pass if we set alpha=2). If a sequence fails, it might be biased—or it might just be in the unlucky 5%.

---

## 2.6: Biased Coins

**Solution:**

```python
import random
from collections import Counter
import statistics

def simulate_biased_streaks(bias, num_sequences=10000, flips_per_sequence=100):
    """Simulate streaks for a biased coin."""
    streaks = []
    for _ in range(num_sequences):
        sequence = [random.random() < bias for _ in range(flips_per_sequence)]
        streaks.append(longest_streak(sequence))
    return streaks

# Fair coin (50/50)
fair_streaks = simulate_biased_streaks(0.5)

# Slightly biased (51/49)
slightly_biased = simulate_biased_streaks(0.51)

# Very biased (60/40)
very_biased = simulate_biased_streaks(0.60)

print("Average longest streak:")
print(f"  Fair coin (50%):       {statistics.mean(fair_streaks):.2f}")
print(f"  Slightly biased (51%): {statistics.mean(slightly_biased):.2f}")
print(f"  Very biased (60%):     {statistics.mean(very_biased):.2f}")

# Test runs test on biased sequences
print("\nRuns test on biased coins (100 sequences of 100 flips):")
for bias, label in [(0.5, "Fair"), (0.51, "51%"), (0.60, "60%")]:
    sequences = [[random.random() < bias for _ in range(100)] for _ in range(100)]
    passed = sum(1 for seq in sequences if runs_test(seq))
    print(f"  {label}: {passed} / 100 passed")
```

**Key finding:**

A slightly biased coin (51%) is nearly indistinguishable from a fair coin using the runs test. You'd need a much larger sample to detect such a slight bias. But a heavily biased coin (60%) shows up more clearly in the distribution of runs.

---

## 2.7: Pattern Hunting

**Solution:**

```python
import random
import statistics

def find_pattern_first_occurrence(sequence, pattern):
    """Find the position of the first occurrence of a pattern."""
    pattern_tuple = tuple(pattern)
    for i in range(len(sequence) - len(pattern) + 1):
        if tuple(sequence[i:i+len(pattern)]) == pattern_tuple:
            return i
    return None

# Generate 1000 sequences
sequences = [[random.choice([0, 1]) for _ in range(100)] for _ in range(1000)]

# Test pattern HTH (represented as [1, 0, 1])
pattern_hth = [1, 0, 1]
positions_hth = []
for seq in sequences:
    pos = find_pattern_first_occurrence(seq, pattern_hth)
    if pos is not None:
        positions_hth.append(pos)

print(f"Pattern HTH (1-0-1):")
print(f"  Found in {len(positions_hth)} / 1000 sequences")
print(f"  Average position: {statistics.mean(positions_hth):.1f}")
print(f"  Median position: {statistics.median(positions_hth)}")

# Test pattern HHHH (represented as [1, 1, 1, 1])
pattern_hhhh = [1, 1, 1, 1]
positions_hhhh = []
for seq in sequences:
    pos = find_pattern_first_occurrence(seq, pattern_hhhh)
    if pos is not None:
        positions_hhhh.append(pos)

print(f"\nPattern HHHH (1-1-1-1):")
print(f"  Found in {len(positions_hhhh)} / 1000 sequences")
print(f"  Average position: {statistics.mean(positions_hhhh):.1f}")
print(f"  Median position: {statistics.median(positions_hhhh)}")
```

**Explanation:**

The pattern [1, 0, 1] should appear on average at position around 8 if we're expecting it randomly. But because we're looking for the first occurrence in a sequence of 100, we'll find it much sooner—typically around position 15-25, depending on luck.

The pattern [1, 1, 1, 1] might not appear in every 100-flip sequence; the probability of it appearing is less than 100%. When it does appear, it's typically later than the 3-flip pattern, just because 4-flip patterns are rarer.

---

## 2.8: When Is a Sequence "Too Random"?

**Answer:**

The perfectly alternating sequence (HTHTH...TH) is highly suspicious. It's too balanced, too alternating. A sequence this orderly would almost never appear by chance. The runs test would flag it as highly suspicious (way too many runs).

This is a key insight: randomness is *messy*. If your random number generator produces perfectly balanced, perfectly alternating sequences, something is wrong. Real randomness has clusters, imbalances, and patterns. The paradox is that true randomness often looks non-random.

---

## 2.9: The Gambler's Intuition

**Answer:**

No. Tails is not more likely on the next flip. Each flip is independent. The fact that we just saw seven heads doesn't change the probability of the next flip—it's still 50/50 if the coin is fair.

This is the **gambler's fallacy**: the belief that past results influence future independent events. It's tempting to think "okay, we're 'due' for tails now," but that's not how probability works.

However, here's where it gets subtle: if we see long enough streak, it *does* provide evidence about the fairness of the coin. A single streak of seven heads is normal. But if we see many very long streaks, or if the streaks seem consistently biased (always headed in the same direction), that's evidence of bias. But that evidence is about whether the coin is fair, not about what's "due" to happen next.

**Intuition to develop:**

- Seven heads in a row? Perfectly normal for a fair coin.
- Ten very long streaks all in the "heads" direction? That might suggest the coin is biased.
- But even if it's biased toward heads (60% heads), each individual flip is still either H or T with that probability. There's no "catching up" mechanism.

---

## 2.10: Automating Randomness Checks

**Solution:**

```python
import random
import math

def runs_test_detailed(sequence, alpha=2.0):
    """
    Run the runs test and return detailed information.
    Returns (passes, z_score, observed, expected)
    """
    n = len(sequence)
    observed = count_runs(sequence)
    expected = (n / 2) + 1
    std_dev = 0.5 * math.sqrt(n / 2)
    
    z_score = abs(observed - expected) / std_dev
    passes = z_score <= alpha
    
    return passes, z_score, observed, expected

# Generate 1000 sequences (or load from file)
sequences = [[random.choice([0, 1]) for _ in range(100)] 
             for _ in range(1000)]

# Test each one
suspicious = []
for i, seq in enumerate(sequences):
    passes, z_score, observed, expected = runs_test_detailed(seq)
    if not passes:
        suspicious.append((i, z_score, observed, expected))

# Report
print(f"Total sequences: {len(sequences)}")
print(f"Suspicious (more than 2 std dev from expected): {len(suspicious)}")
print(f"Percentage suspicious: {(len(suspicious) / len(sequences)) * 100:.1f}%")

if suspicious:
    print(f"\nMost suspicious sequence:")
    idx, z_score, observed, expected = max(suspicious, key=lambda x: x[1])
    print(f"  Index: {idx}")
    print(f"  Z-score: {z_score:.2f}")
    print(f"  Observed runs: {observed}, Expected: {expected:.1f}")
```

**Important caveat:**

If all sequences pass the runs test, that's good—it suggests they came from a fair source. But the runs test alone isn't sufficient. A sequence could pass the runs test and still be non-random in other ways. For example, if every tenth flip is always heads while the rest are random, the runs test might not catch it.

This is why, in practice, we use multiple tests (frequency test, autocorrelation test, entropy tests, etc.) to gain confidence that a sequence is truly random.
