# Exercises for Chapter 1: The Pattern-Seeking Mind

---

## Warm-Up Exercises

### 1.1: Generate a Streak

Generate 100 coin flips and find the longest consecutive run of heads.

```python
import random

flips = [random.choice(['H', 'T']) for _ in range(100)]
# Your code here to find the longest streak
```

**What to report:** The length of the longest streak.

**Follow-up:** Does this match the 7 we expected? Run it a few times. How much does it vary?

---

### 1.2: Birthday Pairs

In a group of 50 people, how many pairs would you expect to share a birthday?

Hint: Start with what fraction of pairs will *not* share a birthday (like we did with 23), then work backward.

**What to report:** Your calculated probability that at least two people share a birthday in a group of 50.

---

## Exploration Exercises

### 1.3: Hand-Generated vs. Machine-Generated

Generate your own sequence of 100 coin flips by hand (or by thinking of one). Write it down.

Now generate 100 machine flips:

```python
import random

machine_flips = [random.choice(['H', 'T']) for _ in range(100)]
print(''.join(machine_flips))
```

Compare them statistically:

```python
def count_runs(flips):
    """Count the number of transitions (H->T or T->H)."""
    runs = 1
    for i in range(1, len(flips)):
        if flips[i] != flips[i-1]:
            runs += 1
    return runs

def longest_streak(flips):
    """Find longest consecutive same result."""
    max_streak = 0
    current_streak = 1
    for i in range(1, len(flips)):
        if flips[i] == flips[i-1]:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    return max_streak

# Analyze both sequences
```

**What to report:**
- Number of runs in each sequence (transitions between H and T)
- Longest streak in each sequence
- Count of heads vs. tails in each

**Reflection:** Which sequence has more runs? Why do you think humans create more transitions than randomness does?

---

### 1.4: Many Simulations

Run 10,000 simulations of 100 coin flips. For each, record:
- The longest streak of heads
- The longest streak of tails
- The absolute difference between heads and tails count

Then plot the distribution of each.

```python
import random
import matplotlib.pyplot as plt

def simulate_flips(num_flips, num_simulations):
    """Run many simulations and collect statistics."""
    # Your code here
    pass

# Generate data and plot
```

**What to report:**
- Three histograms (one for each statistic)
- The mean and standard deviation of each

**Reflection:** Do these distributions match your intuition? What surprises you?

---

## Challenge Exercises

### 1.5: Build a Clustering Detector

Write a function that looks at 2D random points and tries to detect "suspicious" clustering.

One simple approach: divide the square into a grid (say, 10×10 cells), count points in each cell, and see if any cell has way more points than expected.

```python
import random
import math

def detect_clustering(points, num_cells=10):
    """
    Divide the square into a grid and check if clustering is 'suspicious'.
    
    Args:
        points: List of (x, y) tuples in [0, 1] × [0, 1]
        num_cells: Grid size (num_cells × num_cells)
    
    Returns:
        Boolean: True if clustering looks suspicious
    """
    # Your code here
    pass

# Test it
random_points = [(random.random(), random.random()) for _ in range(200)]
print(detect_clustering(random_points))

# Run many random samples—how often does it trigger?
suspicions = 0
for _ in range(1000):
    points = [(random.random(), random.random()) for _ in range(200)]
    if detect_clustering(points):
        suspicions += 1

print(f"Triggered {suspicions}/1000 times")
```

**What to report:**
- Your clustering detection function
- How often it triggers on truly random data

**Reflection:** If it triggers often on random data, that's the clustering illusion in action. Should a real clustering detector trigger less often?

---

### 1.6: The Monkey Typewriter

If a monkey randomly pressed keys on a keyboard, how many times would you need to press keys to expect to see "the" appear by chance?

Let's model a simpler version: a monkey presses a 26-letter keyboard randomly. How many presses to see "abc" appear in a row?

```python
import random

def find_pattern(pattern, num_trials=100000):
    """
    Simulate random letter presses until the pattern appears.
    Run this multiple times to see typical number of presses.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    for trial in range(num_trials):
        # Simulate pressing random keys until pattern appears
        sequence = ''
        presses = 0
        while pattern not in sequence:
            sequence += random.choice(letters)
            presses += 1
            # Prevent infinite loops by limiting to, say, 10 million presses
            if presses > 10_000_000:
                return None
        yield presses

# Run a few times
results = list(find_pattern("abc", num_trials=10))
print(f"Times to see 'abc': {results}")
print(f"Average: {sum(results) / len(results):.0f}")
```

**What to report:**
- How many key presses, on average, until "abc" appears?
- Try different patterns: "aaa", "aba", "abc". Do they take different times?

**Reflection:** This is why the Bible Code is impressive-sounding but not actually surprising—with enough text, patterns *must* appear by chance.

---

## Thought Experiments

### 1.7: The Unfair Coin

You flip a coin 1000 times and get heads 742 times (74.2%). Is the coin unfair?

Don't do math. Just think about randomness. What would convince you the coin is actually biased?

---

### 1.8: The Cancer Cluster

A small town has 5,000 residents. In a given year, you'd expect about 12 cancer cases. Last year, they had 18 cases—that's a 50% spike!

The local paper runs a headline: "Cancer Crisis in Oak Heights." People are scared. A lawsuit is filed.

How would you investigate this? What data would you want to see?

---

### 1.9: The Hot Hand—Your Take

Watch a basketball player make a few shots in a row. Does it *feel* like they're in a hot hand? Why?

Now think: how would you tell the difference between a player having a hot hand and a player just getting lucky for a few shots?

What data would you need?

---

## Solutions

Solutions to these exercises appear in [solutions.md](solutions.md).
