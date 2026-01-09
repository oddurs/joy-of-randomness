# Solutions for Chapter 4: The Drunkard's Walk

These are complete solutions and explanations for the exercises. Try the exercises first before looking here!

---

## Warm-up Solutions

### Exercise 4.1: Plot a Single Walk

**Solution:**

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from simulations import simulate_random_walk

# Generate a single walk
walk = simulate_random_walk(1000)

# Plot it
plt.figure(figsize=(12, 6))
plt.plot(walk, linewidth=0.8, alpha=0.7)
plt.xlabel("Step Number")
plt.ylabel("Position")
plt.title("A Single Random Walk: 1000 Steps")
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Starting point')
plt.legend()
plt.show()

# Report statistics
final_position = walk[-1]
max_distance = max(abs(walk))
min_distance = min(abs(walk))

print(f"Final position: {final_position}")
print(f"Maximum distance from origin: {max_distance}")
print(f"Minimum distance from origin: {min_distance}")
```

**What to expect:**
- Final position will be some random value, typically within ±50 or so
- Maximum distance is usually much larger than the final position (since the walker doesn't always move monotonically away)
- The path will look jagged and chaotic, but not meaningfully so

**Key insight:** Every run is different. This is the essential feature of randomness.

---

### Exercise 4.2: Repeat the Experiment

**Solution:**

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from simulations import simulate_random_walk

# Run 5 walks
num_walks = 5
num_steps = 1000
final_positions = []
colors = ['blue', 'orange', 'green', 'red', 'purple']

plt.figure(figsize=(14, 7))

for i in range(num_walks):
    walk = simulate_random_walk(num_steps)
    final_positions.append(walk[-1])
    plt.plot(walk, linewidth=0.8, alpha=0.7, label=f'Walk {i+1}', color=colors[i])

plt.xlabel("Step Number")
plt.ylabel("Position")
plt.title("5 Random Walks: 1000 Steps Each")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# Report
print("Final positions:", final_positions)
print(f"Range: {min(final_positions)} to {max(final_positions)}")
print(f"Spread: {max(final_positions) - min(final_positions)}")
```

**What to expect:**
- Final positions vary widely, maybe from -50 to +80, or some other range
- Each walk has a unique trajectory
- Some walkers go higher, some lower, some oscillate

**Key insight:** The five walks are independent. Their final positions are scattered. This suggests that if we run 100 or 10,000 walks, we'll see a distribution.

---

### Exercise 4.3: The Distribution

**Solution:**

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from simulations import simulate_random_walk

# Generate 10,000 walks of 100 steps
num_walks = 10000
num_steps = 100
final_positions = []

for _ in range(num_walks):
    walk = simulate_random_walk(num_steps)
    final_positions.append(walk[-1])

final_positions = np.array(final_positions)

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(final_positions, bins=50, density=True, alpha=0.7, edgecolor='black')
plt.xlabel("Final Position")
plt.ylabel("Density")
plt.title(f"Distribution of Final Positions ({num_walks:,} walks, {num_steps} steps)")
plt.grid(True, alpha=0.3)

# Overlay normal distribution
from scipy.stats import norm
mu = 0
sigma = np.sqrt(num_steps)
x = np.linspace(-50, 50, 1000)
plt.plot(x, norm.pdf(x, mu, sigma), 'r-', linewidth=2, label=f'Normal(0, {sigma:.1f})')
plt.legend()
plt.show()

# Statistics
print(f"Mean: {final_positions.mean():.2f}")
print(f"Median: {np.median(final_positions):.2f}")
print(f"Std Dev: {final_positions.std():.2f}")
print(f"√100 = {np.sqrt(100):.2f}")
print(f"Min: {final_positions.min()}")
print(f"Max: {final_positions.max()}")
```

**What to expect:**
- A bell curve centered at zero
- Standard deviation around 10 (√100)
- The theoretical normal distribution matches the histogram well

**Key insight:** The ensemble has structure. Individual walks are chaotic, but many walks together form a beautiful, predictable distribution.

---

## Exploration Solutions

### Exercise 4.4: The √n Relationship

**Solution:**

```python
import numpy as np
import matplotlib.pyplot as plt
from simulations import test_sqrt_n_scaling

# Test different step counts
step_counts = [10, 50, 100, 500, 1000, 5000, 10000]
observed_stds, theoretical_stds = test_sqrt_n_scaling(step_counts, num_walks_per_count=5000)

# Create log-log plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.loglog(step_counts, observed_stds, 'o-', label='Observed', linewidth=2, markersize=8)
ax.loglog(step_counts, theoretical_stds, 's--', label='Theoretical (√n)', linewidth=2, markersize=8)

ax.set_xlabel("Number of Steps (log scale)")
ax.set_ylabel("Standard Deviation (log scale)")
ax.set_title("√n Scaling: Observed vs. Theoretical")
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.show()

# Print comparison table
print("Steps  | Observed Std | Theoretical | Ratio")
print("-" * 45)
for n, obs, theo in zip(step_counts, observed_stds, theoretical_stds):
    ratio = obs / theo
    print(f"{n:>5d}  | {obs:>12.2f} | {theo:>11.2f} | {ratio:.3f}")
```

**What to expect:**
- Observed and theoretical points lie almost exactly on top of each other
- The ratios are all very close to 1.0 (within 0.01 or so)
- On a log-log plot, both lines form a straight line with slope 0.5 (since y = √x is equivalent to log(y) = 0.5 log(x))

**Key insight:** The theory perfectly predicts the data. This is the power of probability: we can derive formulas for random phenomena.

---

### Exercise 4.5: First Returns

**Solution:**

```python
import numpy as np
import matplotlib.pyplot as plt
from simulations import first_return_time

# Collect first return times
num_walks = 1000
max_steps = 100000
first_returns = []

for _ in range(num_walks):
    ret_time = first_return_time(max_steps)
    if ret_time is not None:
        first_returns.append(ret_time)

first_returns = np.array(first_returns)

# Plot on log-log scale
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(first_returns, bins=50, alpha=0.7, edgecolor='black')
axes[0].set_xlabel("Steps Until First Return")
axes[0].set_ylabel("Count")
axes[0].set_title(f"First Return Times ({len(first_returns)} returns)")
axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].grid(True, alpha=0.3, which='both')

# Statistics
axes[1].axis('off')
stats_text = f"""
First Return Statistics

Returns observed: {len(first_returns)} / {num_walks}
Did not return: {num_walks - len(first_returns)}

Minimum: {first_returns.min()} steps
Maximum: {first_returns.max()} steps
Median: {np.median(first_returns):.0f} steps
Mean: {first_returns.mean():.0f} steps

Key insight: Return happens with ~100% probability!
"""
axes[1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

plt.tight_layout()
plt.show()
```

**What to expect:**
- Nearly all walkers (>99%) return within 100,000 steps
- Return times range from 2 (the minimum possible) to 100,000
- The distribution has a heavy tail (a log-log plot shows this is approximately power-law)
- Median is around 2,000-5,000 steps depending on your random sample

**Key insight:** In 1D, return is inevitable. This is a special property of 1D (called *recurrence*). In 2D it still holds, but in 3D and higher, walkers escape to infinity with some probability.

---

### Exercise 4.6: Maximum Distance

**Solution:**

```python
import numpy as np
import matplotlib.pyplot as plt
from simulations import maximum_distance_reached, find_final_position_only

# Track max distance and final position for many walks
num_walks = 1000
num_steps = 1000

max_distances = []
final_positions = []

for _ in range(num_walks):
    max_dist = maximum_distance_reached(num_steps)
    max_distances.append(max_dist)
    
    # Also track final position for comparison
    pos = 0
    for _ in range(num_steps):
        pos += random.choice([-1, 1])
    final_positions.append(abs(pos))

max_distances = np.array(max_distances)
final_positions = np.array(final_positions)

# Compare distributions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(max_distances, bins=50, alpha=0.7, edgecolor='black', label='Max distance')
axes[0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', label='|Final position|')
axes[0].set_xlabel("Distance from Origin")
axes[0].set_ylabel("Count")
axes[0].set_title("Max Distance vs. Final Position")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Statistics
axes[1].axis('off')
stats_text = f"""
Distance Statistics ({num_walks} walks, {num_steps} steps)

Max Distance:
  Mean: {max_distances.mean():.1f}
  Median: {np.median(max_distances):.1f}
  Std Dev: {max_distances.std():.1f}

|Final Position|:
  Mean: {final_positions.mean():.1f}
  Median: {np.median(final_positions):.1f}
  Std Dev: {final_positions.std():.1f}

Key insight: Max distance is always ≥ final position
(The walker doesn't always drift monotonically away)
"""
axes[1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()
```

**What to expect:**
- Max distance is larger than final position (on average, by a factor of around 1.3-1.4)
- Both scale with √n but the constants are different
- Max distance should be around √n × 1.2 or so on average

**Key insight:** The maximum excursion is bigger than the final position because the walker wanders around, doesn't go in a straight line.

---

## Challenge Solutions

### Exercise 4.7: Step Size Variations

**Solution:**

```python
import numpy as np
import matplotlib.pyplot as plt
from simulations import simulate_random_walk_custom_steps, find_final_position_only

num_walks = 5000
num_steps = 1000

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Baseline: ±1
final_positions = np.array([find_final_position_only(num_steps) for _ in range(num_walks)])
axes[0, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='blue')
axes[0, 0].set_title(f"Steps: ±1 (baseline)")
axes[0, 0].set_ylabel("Count")
axes[0, 0].grid(True, alpha=0.3)
print(f"±1 steps: mean={final_positions.mean():.1f}, std={final_positions.std():.1f}, theory={np.sqrt(num_steps):.1f}")

# ±2 steps
final_positions = np.array([
    simulate_random_walk_custom_steps(num_steps, [-2, 2])[-1]
    for _ in range(num_walks)
])
axes[0, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='orange')
axes[0, 1].set_title(f"Steps: ±2")
axes[0, 1].grid(True, alpha=0.3)
print(f"±2 steps: mean={final_positions.mean():.1f}, std={final_positions.std():.1f}, theory={2*np.sqrt(num_steps):.1f}")

# Steps: -1, +3
final_positions = np.array([
    simulate_random_walk_custom_steps(num_steps, [-1, 3])[-1]
    for _ in range(num_walks)
])
axes[1, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='green')
axes[1, 0].set_title(f"Steps: -1 or +3 (unequal, not symmetric)")
axes[1, 0].set_ylabel("Count")
axes[1, 0].grid(True, alpha=0.3)
print(f"-1,+3 steps: mean={final_positions.mean():.1f}, std={final_positions.std():.1f}")

# Steps: -1, +1 with unequal probability
final_positions = np.array([
    simulate_random_walk_custom_steps(num_steps, [-1]*25 + [1]*75)[-1]
    for _ in range(num_walks)
])
axes[1, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='red')
axes[1, 1].set_title(f"Steps: -1 (25%), +1 (75%)")
axes[1, 1].grid(True, alpha=0.3)
print(f"-1(25%),+1(75%): mean={final_positions.mean():.1f}, std={final_positions.std():.1f}")

plt.suptitle("Effect of Step Distribution on Final Positions")
plt.tight_layout()
plt.show()
```

**What to expect:**
- **±1 steps:** std ≈ 31
- **±2 steps:** std ≈ 62 (doubles with step size)
- **-1, +3 steps:** mean ≈ 1000 (biased), std varies
- **Unequal probability:** mean ≠ 0 (biased), std ≈ 31

**Analysis:**
- Step size scales the spread linearly
- Unequal probabilities shift the mean
- All distributions remain approximately normal (CLT)

**Theory behind the numbers:**
- For ±1 steps: Var = 1, so σ = √n
- For ±2 steps: Var = 4, so σ = 2√n
- For -1, +3: expected value = 1 per step, variance ≈ 4, so mean ≈ n, std ≈ 2√n

---

### Exercise 4.8: Biased Walks

**Solution:**

```python
import numpy as np
import matplotlib.pyplot as plt
from simulations import simulate_biased_random_walk

num_walks = 10000
num_steps = 1000

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

biases = [0.5, 0.6, 0.7]
colors = ['blue', 'orange', 'green']

for idx, p in enumerate(biases):
    final_positions = np.array([
        simulate_biased_random_walk(num_steps, p_forward=p)[-1]
        for _ in range(num_walks)
    ])
    
    axes[idx].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color=colors[idx])
    axes[idx].set_title(f"P(+1) = {p}")
    axes[idx].set_xlabel("Final Position")
    axes[idx].grid(True, alpha=0.3)
    
    # Theory
    mean_theoretical = (p - (1-p)) * num_steps  # p - q = 2p - 1
    var_theoretical = 4 * p * (1-p) * num_steps
    std_theoretical = np.sqrt(var_theoretical)
    
    print(f"Bias {p}:")
    print(f"  Observed: mean={final_positions.mean():.1f}, std={final_positions.std():.1f}")
    print(f"  Theory:   mean={mean_theoretical:.1f}, std={std_theoretical:.1f}")

plt.suptitle("Biased Random Walks: Effect of Bias on Final Position Distribution")
plt.tight_layout()
plt.show()
```

**What to expect:**

| P(+1) | Expected Mean | Expected Std |
|-------|---------------|--------------|
| 0.5 (fair) | 0 | √1000 ≈ 31.6 |
| 0.6 | 200 | √960 ≈ 31.0 |
| 0.7 | 400 | √840 ≈ 29.0 |

The key insight: as bias increases, the mean drifts, but the variance actually *decreases* (because the steps are less spread out when biased).

---

### Exercise 4.9: Zero Crossings

**Solution:**

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from simulations import count_zero_crossings

num_walks = 1000
num_steps = 1000

crossings = []
for _ in range(num_walks):
    c = count_zero_crossings(num_steps)
    crossings.append(c)

crossings = np.array(crossings)

plt.figure(figsize=(10, 6))
plt.hist(crossings, bins=30, alpha=0.7, edgecolor='black')
plt.xlabel("Number of Zero Crossings")
plt.ylabel("Count")
plt.title(f"Distribution of Zero Crossings ({num_walks} walks, {num_steps} steps)")
plt.grid(True, alpha=0.3)
plt.show()

print(f"Mean crossings: {crossings.mean():.1f}")
print(f"Median crossings: {np.median(crossings):.1f}")
print(f"Std Dev: {crossings.std():.1f}")
print(f"Min: {crossings.min()}, Max: {crossings.max()}")
```

**What to expect:**
- Average around 30-35 zero crossings per 1000-step walk
- Some walks with very few (0-5), some with many (60+)
- The distribution is roughly normal but skewed

**Key insight:** The walker's sign changes frequently. A random walk crosses zero about once every √(πn/2) steps on average, which gives roughly 25 crossings for 1000 steps (order-of-magnitude).

---

## Thought Experiment Solutions

### Exercise 4.10: The Prediction Problem

**Answer:**

You'd guess the walker stays around +30. After another 100 steps, the position is:

$$\text{Position}' = 30 + X'$$

where $X'$ is the displacement from the next 100 steps, which is a new random variable with the same distribution as the original (mean 0, std ≈ 10).

**Expected value of Position':** 30 (the new steps average to zero)  
**Expected std of Position':** √(10² + 10²) = √200 ≈ 14

So you'd expect the position around 30, with uncertainty of about ±14.

**Confidence:** Low! You know the rough center but not the spread. In fact, after another 1000 steps, the walker could be almost anywhere from -100 to +200.

**Key insight:** Independence means you can't use current position to predict future position more than one step ahead. The past is independent of the future.

---

### Exercise 4.11: The Escape Problem

**Answer:**

1. **In 2D:** Still returns to origin (with probability 1, though average return time is much longer).
2. **In 3D:** Returns with probability only about 0.34. The walker is likely to escape to infinity.
3. **In 4D and higher:** Escape is even more likely.

**Intuition:** Higher dimensions have "more space." In 1D, you're constrained to a line—you must cross any given point eventually. In 2D, you have more room to wander but still recurrent. In 3D+, the walker can find "pockets" of space and escape.

**Geometric reason:** In d dimensions, the number of lattice points at distance r from the origin grows like r^(d-1). The walker explores by random walk, which "uses up" lattice points. In d=1, 2, the rate of discovery is slow enough that recurrence holds. In d≥3, the growth of space outpaces the walker.

---

### Exercise 4.12: The √n Intuition

**Explanation:**

If steps were *all* in the same direction, you'd be at position ±n.  
If steps were *random*, they cancel: each left cancels a right.

In reality, you get some cancellation but not complete. The net effect:
- Expected number of +1 steps: n/2
- Expected number of -1 steps: n/2
- Net position: approximately (n/2) - (n/2) = 0

But there's randomness in how many +1's you get. If you get k more +1's than -1's, your position is k. The variance of k is approximately n/4. So the std of position is √(n/4) = √n/2.

**Why not n?** Because the steps *mostly* cancel. Only the *imbalance* matters, and the imbalance grows slowly.

**Why √n and not constant?** Because even with cancellation, the imbalances add up. The more steps, the more opportunity for imbalance, but the rate of growth is √n, not n.

**Variances vs. Standard Deviations:**
- Variance of one step: 1
- Variance of n steps: 1 + 1 + ... + 1 = n
- Standard deviation of n steps: √n

Variances add. Standard deviations don't (they're square roots of variances).

---

### Exercise 4.13: Real-World Intuition

**Analysis:**

1. **Stock price:** Yes, approximately a random walk (efficient market hypothesis). Daily returns are roughly random.

2. **Bank account:** Sort of. Regular deposits/withdrawals are predictable (not random), but random transactions might follow a random walk pattern.

3. **Person in a crowd:** Not really. People move with intention and constraints (can't walk through walls).

4. **Bacteria in petri dish:** Initially yes (exponential growth), but then no (limited resources, crowding).

5. **River water level:** No. Shows seasonality (winter rain), trends (climate), memory (wet year makes next year wetter).

6. **Daily temperature:** No. Strong daily cycle (warmer afternoon) and seasonal cycle (summer hot, winter cold).

**Random walk properties needed:**
- Independent steps (each step unaffected by previous)
- No external trend or force
- No memory or seasonality
- Symmetric (equal chance of up/down)

Most real phenomena violate at least one of these. But many are *approximately* random walks over short timescales.

---

## Key Takeaways

After working through these exercises, you should understand:

1. **Individual paths are unpredictable** (chaos), but **ensembles have structure** (statistics)
2. **√n scaling** is fundamental to sums of independent random variables
3. **The Central Limit Theorem** explains why distributions become normal
4. **Variance and standard deviation** have different addition rules
5. **Real processes** are rarely perfect random walks but often approximate them
6. **Dimension matters** (recurrence in 1D/2D, escape in 3D+)

These principles extend throughout probability, statistics, and physics.
