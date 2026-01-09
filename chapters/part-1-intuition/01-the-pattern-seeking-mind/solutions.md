# Solutions for Chapter 1: The Pattern-Seeking Mind

---

## Warm-Up Solutions

### 1.1: Generate a Streak

```python
import random

def longest_streak(flips):
    """Find the longest consecutive sequence of heads."""
    max_streak = 0
    current_streak = 0
    for flip in flips:
        if flip == 'H':
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak

flips = [random.choice(['H', 'T']) for _ in range(100)]
print(f"Longest streak: {longest_streak(flips)}")
```

**Expected result:** Around 7 (could range from 4 to 12 or so).

**Why?** This is what we expect from randomness. Most people underestimate how long streaks should be.

---

### 1.2: Birthday Pairs

Think about it intuitively: with 50 people, you have many pairs—50 × 49 / 2 = 1,225 pairs. Each pair is an opportunity for a birthday match. That's a lot of chances!

To calculate this formally, we compute the probability that *all* birthdays are different, then take the complement:

$$P(\text{all different}) = \frac{365}{365} \times \frac{364}{365} \times \frac{363}{365} \times \cdots \times \frac{316}{365}$$

Then the probability of at least one match is:

$$P(\text{match}) = 1 - P(\text{all different}) \approx 0.97$$

**Answer:** About 97% for 50 people.

```python
def birthday_probability(n):
    prob_no_match = 1.0
    for i in range(n):
        prob_no_match *= (365 - i) / 365
    return 1 - prob_no_match

print(f"50 people: {birthday_probability(50):.1%}")  # ~97%
```

---

## Exploration Solutions

### 1.3: Hand-Generated vs. Machine-Generated

```python
import random

def count_runs(flips):
    """Count transitions between H and T."""
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

# Generate machine flips
machine_flips = [random.choice(['H', 'T']) for _ in range(100)]

print(f"Your sequence stats:")
print(f"  Runs: {count_runs(your_flips)}")
print(f"  Longest streak: {longest_streak(your_flips)}")
print(f"  Heads: {your_flips.count('H')}/100")
print()
print(f"Machine sequence stats:")
print(f"  Runs: {count_runs(machine_flips)}")
print(f"  Longest streak: {longest_streak(machine_flips)}")
print(f"  Heads: {machine_flips.count('H')}/100")
```

**Typical findings:**
- Human sequences have more runs (~60-70 per 100 flips)
- Random sequences have fewer (~50-55 per 100 flips)
- Human sequences are more "balanced" (closer to 50H/50T early)
- Random sequences are more "streaky" (might have 60H/40T early)

**Why?** Humans unconsciously try to create patterns that feel balanced and avoid repetition. True randomness doesn't care about balance in short runs.

---

### 1.4: Many Simulations

```python
import random
import matplotlib.pyplot as plt
import statistics

def longest_streak(flips):
    max_streak = 0
    current_streak = 0
    for flip in flips:
        if flip == 'H':
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak

def simulate_flips(num_flips, num_simulations):
    """Run simulations and collect statistics."""
    longest_streaks = []
    differences = []
    
    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(num_flips)]
        longest_streaks.append(longest_streak(flips))
        heads = flips.count('H')
        differences.append(abs(heads - (num_flips / 2)))
    
    return longest_streaks, differences

# Generate data
longest_streaks, differences = simulate_flips(100, 10000)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(longest_streaks, bins=20, edgecolor='black')
axes[0].set_xlabel("Longest Streak Length")
axes[0].set_ylabel("Frequency")
axes[0].set_title("Distribution of Longest Streaks (100 flips, 10k sims)")
axes[0].axvline(statistics.mean(longest_streaks), color='red', linestyle='--')

axes[1].hist(differences, bins=20, edgecolor='black')
axes[1].set_xlabel("|Heads - Tails|")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Distribution of Imbalance")
axes[1].axvline(statistics.mean(differences), color='red', linestyle='--')

plt.tight_layout()
plt.show()

# Print stats
print(f"Longest Streak Stats:")
print(f"  Mean: {statistics.mean(longest_streaks):.2f}")
print(f"  Stdev: {statistics.stdev(longest_streaks):.2f}")
print(f"Imbalance Stats:")
print(f"  Mean |H - T|: {statistics.mean(differences):.2f}")
print(f"  Stdev: {statistics.stdev(differences):.2f}")
```

**Expected results:**
- Longest streak is roughly normally distributed around 7
- Imbalance (|H - T|) is also roughly normal, centered around 8-9

---

## Challenge Solutions

### 1.5: Build a Clustering Detector

```python
import random

def detect_clustering(points, num_cells=10, threshold_percentile=95):
    """
    Detect suspicious clustering by checking grid cell occupancy.
    
    Args:
        points: List of (x, y) tuples in [0, 1] × [0, 1]
        num_cells: Grid size
        threshold_percentile: Trigger if max exceeds this percentile of expected
    
    Returns:
        Boolean: True if clustering looks suspicious
    """
    # Expected points per cell
    expected = len(points) / (num_cells * num_cells)
    
    # Count points in grid
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    
    for x, y in points:
        cell_x = min(int(x * num_cells), num_cells - 1)
        cell_y = min(int(y * num_cells), num_cells - 1)
        grid[cell_x][cell_y] += 1
    
    # Find max
    max_count = max(max(row) for row in grid)
    
    # Use binomial distribution idea: for n=expected and p=1, 
    # we might see up to ~2*sqrt(expected) above expected
    threshold = expected * (threshold_percentile / 100)
    
    return max_count > threshold

# Test it
random_points = [(random.random(), random.random()) for _ in range(200)]
print(f"Single test: {detect_clustering(random_points)}")

# Run many times
suspicions = 0
for _ in range(1000):
    points = [(random.random(), random.random()) for _ in range(200)]
    if detect_clustering(points, threshold_percentile=95):
        suspicions += 1

print(f"Triggered on {suspicions}/1000 truly random samples")
# Should be around 50 (5% of samples exceed the 95th percentile by chance)
```

**Key insight:** If your detector triggers too often on truly random data, you've just demonstrated the clustering illusion—you'll see "suspicious" clusters in random noise.

---

### 1.6: The Monkey Typewriter

```python
import random

def find_pattern(pattern, num_trials=10):
    """
    Simulate random letter presses until pattern appears.
    
    Returns a list of (number of presses, trial number) for each trial.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    results = []
    
    for trial in range(num_trials):
        sequence = ''
        presses = 0
        
        while pattern not in sequence:
            sequence += random.choice(letters)
            presses += 1
            
            # Prevent infinite loops
            if presses > 100_000_000:
                break
        
        results.append(presses)
    
    return results

# Try different patterns
for pattern in ['a', 'aa', 'aaa', 'abc', 'aba']:
    results = find_pattern(pattern, num_trials=5)
    avg = sum(results) / len(results)
    print(f"Pattern '{pattern}': avg {avg:.0f} presses (range: {min(results)}-{max(results)})")
```

**Expected results:**
- 'a': ~26 (one in 26 letters)
- 'aa': ~676 (26² expected)
- 'aaa': ~17,576 (26³ expected)
- 'abc': ~17,576 (26³ expected)
- 'aba': Much longer! Because after seeing 'ab', you have to start over if you don't get 'a'

**Why?** Overlapping patterns are harder. This is why the Bible Code isn't actually miraculous—with enough text, any pattern eventually appears by sheer chance.

---

## Thought Experiment Solutions

### 1.7: The Unfair Coin

**Analysis:** 742 heads out of 1000 is 74.2%. That's a massive deviation from 50%!

With randomness in coin flips, there's *always* variation around the expected 50%. The size of this variation shrinks as you flip more—it's proportional to the square root of the number of flips.

Specifically, with 1000 flips, the standard deviation (a measure of expected fluctuation) is:

$$\sigma = \sqrt{n \cdot p \cdot (1-p)} = \sqrt{1000 \cdot 0.5 \cdot 0.5} \approx 16$$

So 742 heads is about $(742 - 500) / 16 \approx 15$ standard deviations away from the expected 500. That's *extremely* unlikely—a probability around $10^{-50}$.

**Answer:** The coin is almost certainly biased. With 742/1000, you don't need more data—this is decisive.

---

### 1.8: The Cancer Cluster

**What you'd want to investigate:**

1. **Time series:** Did this town have 12 cases the previous years? Is 18 actually unusual?
2. **Baseline calculation:** For a town of 5,000, what's the expected variation in cancer cases? Standard deviation matters.
3. **Exposure data:** Any actual risk factors changed? New factory? Environmental issue?
4. **Lookback:** How many towns have you checked? If you've examined 1,000 towns, some will have unusual clusters by chance.
5. **Comparison:** What are neighboring towns experiencing?

**The key insight:** One year of data is not enough. You need a baseline and understanding of expected random variation. Most "clusters" disappear when you look at longer time series.

---

### 1.9: The Hot Hand—Your Take

**The feeling:** Yes, it *feels* like something is happening when a player hits three shots in a row. Our brains are pattern detectors.

**How to test it:**
- Compare the shooting percentage *after* a made shot vs. *after* a missed shot
- Account for selection bias (defenders might play tighter after a hit)
- Use rigorous statistical tests, not just eyeballing sequences

**The reality:** This is genuinely contested. Some recent work suggests the hot hand might exist (contrary to earlier claims). But our intuitions wildly overestimate it—we see hot hands in coin flips, so we can't trust our feelings here.
