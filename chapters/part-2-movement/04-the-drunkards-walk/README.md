# Chapter 4: The Drunkard's Walk

## Metadata

```yaml
Part: 2 - Movement
Topics: Random walks, path dependence, diffusion
Key Concepts: 1D walks, step distribution, expected displacement, variance scaling
```

---

## The Random Walker's Paradox

Here's something counterintuitive.

A person stands at a lamppost and takes random steps—equal probability of moving left or right. After 100 steps, how far from the lamppost are they?

Your first instinct might be: close to zero. After all, if they go left as often as they go right, the steps should cancel out.

But that's not quite right.

Yes, the expected position is zero by symmetry. But they're rarely *at* zero. Instead, they're scattered far from the lamppost, wandering unpredictably. And the farther they walk, the farther away they tend to be—not in a deterministic way, but as a matter of probability.

This is the magic of random walks: individual paths are chaotic and hard to predict, but the ensemble has beautiful structure.

---

## Taking One Walk

Let's watch a single drunkard stumble.

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_random_walk(num_steps, start=0):
    """Simulate a 1D random walk."""
    position = start
    history = [position]
    
    for _ in range(num_steps):
        # Random step: +1 or -1 with equal probability
        step = random.choice([-1, 1])
        position += step
        history.append(position)
    
    return np.array(history)

# One walk of 1000 steps
walk = simulate_random_walk(1000)

plt.figure(figsize=(12, 6))
plt.plot(walk, linewidth=0.8, alpha=0.7)
plt.xlabel("Step Number")
plt.ylabel("Position")
plt.title("A Single Random Walk: 1000 Steps")
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Starting point')
plt.legend()
plt.show()

print(f"Final position: {walk[-1]}")
print(f"Maximum distance from origin: {max(abs(walk))}")
```

What do you notice? The path is jagged and unpredictable. It wanders up, down, sideways. Sometimes it returns near the origin; sometimes it drifts far away. The final position could be +40, -50, +8—there's no way to predict it from the rules alone.

Run this a few times. Every execution is different, chaotic in its own way.

But here's the thing: if we run *many* walks, patterns emerge.

---

## Many Walks Reveal Structure

Let's run 10,000 walks of 1000 steps each and look at where they end up:

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_random_walk(num_steps, start=0):
    """Simulate a 1D random walk."""
    position = start
    history = [position]
    
    for _ in range(num_steps):
        step = random.choice([-1, 1])
        position += step
        history.append(position)
    
    return np.array(history)

# Run many walks
num_walks = 10000
num_steps = 1000
final_positions = []

for _ in range(num_walks):
    walk = simulate_random_walk(num_steps)
    final_positions.append(walk[-1])

final_positions = np.array(final_positions)

# Plot the distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(final_positions, bins=50, density=True, alpha=0.7, edgecolor='black')
axes[0].set_xlabel("Final Position")
axes[0].set_ylabel("Density")
axes[0].set_title("Distribution of Final Positions (10,000 walks)")
axes[0].grid(True, alpha=0.3)

# Overlay the theoretical normal distribution
mu = 0
sigma = np.sqrt(num_steps)
x = np.linspace(-100, 100, 1000)
from scipy.stats import norm
axes[0].plot(x, norm.pdf(x, mu, sigma), 'r-', linewidth=2, label=f'Normal(0, √{num_steps})')
axes[0].legend()

# Statistics
axes[1].axis('off')
stats_text = f"""
Simulation Statistics (10,000 walks, 1000 steps)

Mean final position: {final_positions.mean():.1f}
Median final position: {np.median(final_positions):.1f}

Standard deviation: {final_positions.std():.1f}
√(number of steps): {np.sqrt(num_steps):.1f}

Min position: {final_positions.min()}
Max position: {final_positions.max()}
"""
axes[1].text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()

print(f"Observed standard deviation: {final_positions.std():.2f}")
print(f"Theoretical (√n): {np.sqrt(num_steps):.2f}")
print(f"Ratio: {final_positions.std() / np.sqrt(num_steps):.3f}")
```

Look at that distribution. It's a bell curve centered at zero, exactly what we'd expect from the symmetry of the problem. But the *width* of that curve is striking.

After 1000 steps, the standard deviation is around 31—approximately √1000. This is not a coincidence.

---

## The Mathematics of Spreading

Let's think about why the spread grows like √n.

Suppose our walker takes n steps, each step being +1 or -1 with equal probability. The final position is:

$$S_n = X_1 + X_2 + \cdots + X_n$$

where each $X_i$ is our random step.

**Expected value:** By symmetry, $E[X_i] = 0$, so $E[S_n] = 0$.

**Variance:** Each step has variance $\text{Var}(X_i) = 1$ (since $X_i$ is ±1 with equal probability). Because the steps are independent, the variances *add*:

$$\text{Var}(S_n) = \text{Var}(X_1) + \text{Var}(X_2) + \cdots + \text{Var}(X_n) = n$$

**Standard deviation:** $\sigma = \sqrt{n}$

So the spread of the distribution grows like the square root of the number of steps. This is why the walker gets farther away, but slowly—much slower than if the steps were biased in one direction.

Here's the key insight: when you add many independent random quantities, their sum grows like the square root of the number of terms. This is a fundamental principle in probability, and it shows up everywhere in nature.

---

## Testing the Square Root Scaling

Let's verify this by comparing the observed spread to the theoretical √n prediction:

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_random_walk(num_steps, start=0):
    """Simulate a 1D random walk."""
    position = start
    for _ in range(num_steps):
        position += random.choice([-1, 1])
    return position

# Test different walk lengths
step_counts = [10, 50, 100, 500, 1000, 5000, 10000]
observed_stds = []
theoretical_stds = []

for n in step_counts:
    # Run many walks for each step count
    final_positions = [simulate_random_walk(n) for _ in range(10000)]
    observed_stds.append(np.std(final_positions))
    theoretical_stds.append(np.sqrt(n))

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.loglog(step_counts, observed_stds, 'o-', label='Observed', linewidth=2, markersize=8)
ax.loglog(step_counts, theoretical_stds, 's--', label='Theoretical (√n)', linewidth=2, markersize=8)

ax.set_xlabel("Number of Steps (log scale)")
ax.set_ylabel("Standard Deviation of Final Position (log scale)")
ax.set_title("Random Walk Spread: Observed vs. Theory")
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

# Print comparison
print("Number of Steps | Observed Std | Theoretical | Ratio")
print("=" * 55)
for n, obs, theo in zip(step_counts, observed_stds, theoretical_stds):
    ratio = obs / theo
    print(f"{n:>14d} | {obs:>12.2f} | {theo:>11.2f} | {ratio:.3f}")
```

The agreement is nearly perfect. Theory and simulation walk hand in hand.

---

## The Central Limit Theorem at Work

Why is the distribution of final positions so perfectly normal?

There's a deep theorem called the **Central Limit Theorem** that explains this. It says: when you sum many independent random quantities, the distribution of the sum is approximately normal, regardless of the distribution of the individual terms.

In our case, we're summing 1000 random steps, each one ±1 with equal probability. The CLT predicts:
- The sum should be approximately normal
- With mean 0
- With standard deviation √n

This prediction is exactly what we observe.

The beauty of the Central Limit Theorem is that it doesn't care about the original distribution of the steps. Whether the steps come from coin flips, dice rolls, or any other random process (with finite variance), the sum will be approximately normal. This is why normal distributions are so ubiquitous in nature.

---

## Beyond Perfect Symmetry

What happens if the steps are different sizes? Or if they're not perfectly symmetric?

Let's try a few variations:

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_walk_with_steps(num_steps, step_dist):
    """Simulate a random walk with custom step distribution."""
    position = 0
    for _ in range(num_steps):
        position += random.choice(step_dist)
    return position

# Different step distributions
num_walks = 10000
num_steps = 1000

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Scenario 1: Steps of ±1
final_positions = [simulate_walk_with_steps(num_steps, [-1, 1]) for _ in range(num_walks)]
axes[0, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black')
axes[0, 0].set_title("Steps: ±1")
axes[0, 0].set_ylabel("Count")
axes[0, 0].set_xlim(-150, 150)

# Scenario 2: Steps of ±2
final_positions = [simulate_walk_with_steps(num_steps, [-2, 2]) for _ in range(num_walks)]
axes[0, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='orange')
axes[0, 1].set_title("Steps: ±2")
axes[0, 1].set_xlim(-150, 150)

# Scenario 3: Steps of ±1 and ±3 (unequal)
final_positions = [simulate_walk_with_steps(num_steps, [-1, 1, 1, 1, 3, 3, 3, 3]) for _ in range(num_walks)]
axes[1, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='green')
axes[1, 0].set_title("Steps: -1 (1/8), +1 (3/8), +3 (4/8)")
axes[1, 0].set_ylabel("Count")
axes[1, 0].set_xlim(-150, 150)

# Scenario 4: Biased walk (+1 with probability 0.6, -1 with probability 0.4)
def biased_walk(num_steps, p=0.6):
    position = 0
    for _ in range(num_steps):
        position += 1 if random.random() < p else -1
    return position

final_positions = [biased_walk(num_steps) for _ in range(num_walks)]
axes[1, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='red')
axes[1, 1].set_title("Biased: +1 with p=0.6, -1 with p=0.4")
axes[1, 1].set_xlim(-150, 150)

plt.tight_layout()
plt.show()
```

Notice what happens:
- Different step sizes change the width of the distribution but keep the same shape
- Unequal step probabilities change the expected value but the distribution still looks normal
- A biased walk drifts away from zero but maintains a normal shape around its new center

This flexibility is the power of the Central Limit Theorem: the shape persists.

---

## Recurrence: Does the Walker Return Home?

Here's a beautiful fact: in one dimension, a random walker will *almost surely* return to the origin at some point.

This might sound obvious—if the walker wanders randomly, won't they stumble back home eventually? But in higher dimensions (which we'll explore in Chapter 5), this is no longer true.

Let's verify this empirically:

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def random_walk_first_return(max_steps=100000):
    """Simulate until walker returns to origin. Return the number of steps."""
    position = 0
    for step in range(1, max_steps + 1):
        position += random.choice([-1, 1])
        if position == 0:
            return step
    return None  # Didn't return within max_steps

# Run many walks and track first returns
first_returns = []
max_steps = 100000

for _ in range(1000):
    return_time = random_walk_first_return(max_steps)
    if return_time is not None:
        first_returns.append(return_time)

first_returns = np.array(first_returns)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram (log scale)
axes[0].hist(first_returns, bins=50, alpha=0.7, edgecolor='black')
axes[0].set_xlabel("Steps Until First Return")
axes[0].set_ylabel("Count")
axes[0].set_title("Distribution of First Return Times (1000 walks)")
axes[0].set_yscale('log')
axes[0].set_xscale('log')
axes[0].grid(True, alpha=0.3)

# Statistics
axes[1].axis('off')
stats_text = f"""
First Return Times

Minimum: {first_returns.min()} steps
Maximum: {first_returns.max()} steps
Median: {np.median(first_returns):.0f} steps
Mean: {first_returns.mean():.0f} steps

Percentage that returned: {100 * len(first_returns) / 1000:.1f}%
(max_steps = {max_steps})
"""
axes[1].text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()
```

Notice: almost every walker returns to the origin, and the distribution of return times has a long tail. Some return quickly (after 2 steps is the minimum); others take a very long time.

This property—that 1D random walks are *recurrent*—is remarkable. It means every position is visited infinitely often, with probability 1. The walker will eventually visit every integer on the number line.

---

## An Unexpected Application: Brownian Motion

Robert Brown, a botanist, observed something peculiar in 1827. When he looked at pollen grains suspended in water under a microscope, they didn't sit still. They jiggled, vibrated, and drifted in chaotic patterns.

He initially thought the motion indicated life, but he found the same motion in inorganic particles. The motion was due to random bombardment by water molecules—an invisible molecular dance.

This *Brownian motion* is exactly what our random walk model describes, in the continuous limit. If particles are bombarded by many tiny random collisions, their trajectories are random walks.

Einstein later explained this mathematically, and his work led to experimental confirmation of atomic theory. The random motion of pollen grains became proof that atoms exist and move.

Here's a simple simulation of Brownian motion as a discrete random walk:

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def brownian_particle(num_steps):
    """Simulate the trajectory of a particle in Brownian motion."""
    x, y = 0, 0
    x_history = [x]
    y_history = [y]
    
    for _ in range(num_steps):
        # Random direction in 2D
        angle = random.uniform(0, 2 * np.pi)
        # Random magnitude (small displacement)
        magnitude = random.expovariate(1.0)
        
        x += magnitude * np.cos(angle)
        y += magnitude * np.sin(angle)
        
        x_history.append(x)
        y_history.append(y)
    
    return x_history, y_history

# Simulate a few particles
fig, ax = plt.subplots(figsize=(10, 10))

for _ in range(5):
    x_hist, y_hist = brownian_particle(10000)
    ax.plot(x_hist, y_hist, linewidth=0.5, alpha=0.7)

ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_title("Brownian Motion: Paths of 5 Particles")
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

These chaotic paths, which seemed to Brown like signs of life, are in fact signatures of the molecular world. They're beautiful evidence of randomness in nature.

---

## Summary

The drunkard's walk teaches us that:

1. **Individual paths are unpredictable**, but the **ensemble has structure**. Many random walks create a bell curve of final positions.

2. **Spread grows like √n**. After n steps, the typical distance from the origin is about √n. This is slower than linear drift, but inevitable.

3. **The Central Limit Theorem** explains why the final positions are normally distributed, regardless of the specific shape of the step distribution.

4. **In one dimension, walkers always return home**. The 1D random walk is *recurrent*—every position is visited infinitely often.

5. **Random walks model real phenomena**. Brownian motion of particles, diffusion of molecules, and many other natural processes are random walks in disguise.

These principles extend to higher dimensions, more complex step distributions, and biased walks. They're foundational to our understanding of randomness and motion.

---

## What Comes Next?

We've mastered the one-dimensional case. But we live in more than one dimension. What happens when our drunkard can stumble left, right, forward, and backward? 

In the next chapter, we'll take a walk in two dimensions—and discover something astonishing: a fact so strange that it stumped mathematicians for decades.

---

## Exercises

See [exercises.md](exercises.md) for guided explorations and challenges.
