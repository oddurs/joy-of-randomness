# Chapter 6 Solutions: Random Walks in the Wild

## Warm-up Solutions

**1. Visualize step-length distributions**

```python
from simulations import simulate_realistic_animal_track, extract_step_lengths
import numpy as np
import matplotlib.pyplot as plt

x, y = simulate_realistic_animal_track(5000)
steps = extract_step_lengths(x, y)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Linear scale
axes[0].hist(steps, bins=40, density=True, alpha=0.7, edgecolor='black')
axes[0].set_xlabel('Step Length')
axes[0].set_ylabel('Density')
axes[0].set_title('Step Lengths (Linear Scale)')
axes[0].grid(True, alpha=0.3)

# Log-log scale (CCDF)
sorted_steps = np.sort(steps)
ccdf = 1 - np.arange(len(sorted_steps)) / len(sorted_steps)
axes[1].loglog(sorted_steps, ccdf, 'o-', markersize=3, alpha=0.7)
axes[1].set_xlabel('Step Length')
axes[1].set_ylabel('P(S > s)')
axes[1].set_title('Cumulative Distribution (log-log)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Step length statistics:")
print(f"  Mean: {np.mean(steps):.3f}")
print(f"  Std:  {np.std(steps):.3f}")
print(f"  Max:  {np.max(steps):.3f}")
print(f"  Min:  {np.min(steps):.3f}")
```

**Expected output:** The histogram on the left shows an exponential-like tail (density decreases smoothly). The log-log CCDF plot shows curvature, suggesting a transition between exponential and power-law regimes. The animal track has more long steps than a pure exponential, but not a true power law.

---

**2. Compare two trajectory types**

```python
from simulations import (simulate_ideal_random_walk_2d, 
                         simulate_levy_flight_2d, 
                         extract_step_lengths)
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
num_steps = 5000

# Ideal random walk
x_ideal, y_ideal = simulate_ideal_random_walk_2d(num_steps)
dist_ideal = np.sqrt(x_ideal[-1]**2 + y_ideal[-1]**2)
distances_ideal = np.sqrt(x_ideal**2 + y_ideal**2)
max_dist_ideal = np.max(distances_ideal)
steps_ideal = extract_step_lengths(x_ideal, y_ideal)
path_length_ideal = np.sum(steps_ideal)

# Lévy flight
x_levy, y_levy = simulate_levy_flight_2d(num_steps, alpha=1.5)
dist_levy = np.sqrt(x_levy[-1]**2 + y_levy[-1]**2)
distances_levy = np.sqrt(x_levy**2 + y_levy**2)
max_dist_levy = np.max(distances_levy)
steps_levy = extract_step_lengths(x_levy, y_levy)
path_length_levy = np.sum(steps_levy)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].plot(x_ideal, y_ideal, linewidth=0.3, alpha=0.7, label='Ideal')
axes[0].scatter([0], [0], color='red', s=100, zorder=5)
axes[0].scatter([x_ideal[-1]], [y_ideal[-1]], color='green', s=100, zorder=5)
axes[0].set_title('Ideal Random Walk')
axes[0].set_aspect('equal')
axes[0].grid(True, alpha=0.3)

axes[1].plot(x_levy, y_levy, linewidth=0.3, alpha=0.7, label='Lévy')
axes[1].scatter([0], [0], color='red', s=100, zorder=5)
axes[1].scatter([x_levy[-1]], [y_levy[-1]], color='green', s=100, zorder=5)
axes[1].set_title('Lévy Flight (α=1.5)')
axes[1].set_aspect('equal')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print metrics
print("Comparison of walk metrics:")
print(f"{'Metric':<20} {'Ideal':<15} {'Lévy':<15}")
print("-" * 50)
print(f"{'Final distance':<20} {dist_ideal:>13.2f}    {dist_levy:>13.2f}")
print(f"{'Max distance':<20} {max_dist_ideal:>13.2f}    {max_dist_levy:>13.2f}")
print(f"{'Path length':<20} {path_length_ideal:>13.2f}    {path_length_levy:>13.2f}")
print(f"{'Efficiency (final/path)':<20} {dist_ideal/path_length_ideal:>13.4f}    {dist_levy/path_length_levy:>13.4f}")
```

**Expected output:** The Lévy flight reaches a much larger final distance (since a few giant jumps dominate). The max distance is also larger. Interestingly, the path length (sum of steps) is similar, but the Lévy flight "uses" those steps more efficiently to spread out.

---

**3. Power-law exponent estimation**

```python
from simulations import simulate_levy_flight_2d, extract_step_lengths, fit_power_law_exponent
import numpy as np

true_alpha = 1.8
num_trials = 10
estimates = []

np.random.seed(42)
for trial in range(num_trials):
    x, y = simulate_levy_flight_2d(10000, alpha=true_alpha)
    steps = extract_step_lengths(x, y)
    alpha_est = fit_power_law_exponent(steps, x_min=0.5)
    estimates.append(alpha_est)
    print(f"Trial {trial+1}: α_est = {alpha_est:.3f}")

estimates = np.array(estimates)
print(f"\nSummary:")
print(f"  True α: {true_alpha}")
print(f"  Mean estimate: {np.mean(estimates):.3f}")
print(f"  Std of estimates: {np.std(estimates):.4f}")
print(f"  95% CI: [{np.percentile(estimates, 2.5):.3f}, {np.percentile(estimates, 97.5):.3f}]")
```

**Expected output:** The estimates cluster around 1.8 with some scatter. Standard deviation typically ~0.05-0.1. Longer walks (more steps) give tighter estimates.

---

## Exploration Solutions

**4. Return probability in 2D**

```python
from simulations import simulate_ideal_random_walk_2d
import numpy as np

num_walks = 100
num_steps = 10000
threshold = 0.1

returns = 0

for walk_id in range(num_walks):
    x, y = simulate_ideal_random_walk_2d(num_steps)
    distances = np.sqrt(x**2 + y**2)
    
    if np.min(distances[1:]) < threshold:  # Skip first point (always 0)
        returns += 1

return_prob = returns / num_walks
print(f"Return probability (distance < {threshold}): {return_prob:.2%}")
print(f"Pólya's theorem predicts: 100% in 2D")
print(f"Match: {'Yes' if return_prob > 0.95 else 'No'}")
```

**Expected output:** ~100% (or very close, e.g., 98-100%). This confirms Pólya's theorem for 2D random walks.

---

**5. Spread comparison: Step size effects**

```python
from simulations import (simulate_ideal_random_walk_2d, 
                         simulate_correlated_random_walk_2d,
                         simulate_levy_flight_2d)
import numpy as np
import matplotlib.pyplot as plt

step_counts = [100, 500, 1000, 5000, 10000]
replicates = 5

results = {
    'fixed': [],
    'exponential': [],
    'power_law': []
}

for num_steps in step_counts:
    for walk_type in results:
        distances = []
        for _ in range(replicates):
            if walk_type == 'fixed':
                x, y = simulate_ideal_random_walk_2d(num_steps)
            elif walk_type == 'exponential':
                x, y = simulate_correlated_random_walk_2d(num_steps, step_dist='exponential')
            else:  # power_law
                x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
            
            distances.append(np.sqrt(x[-1]**2 + y[-1]**2))
        
        results[walk_type].append(np.mean(distances))

fig, ax = plt.subplots(figsize=(10, 6))

for walk_type, distances in results.items():
    ax.loglog(step_counts, distances, 'o-', label=walk_type, linewidth=2)

# Reference line: √n
sqrt_n = np.sqrt(np.array(step_counts))
ax.loglog(step_counts, sqrt_n / sqrt_n[0] * results['fixed'][0], 'k--', alpha=0.5, label='√n')

ax.set_xlabel('Number of Steps (log)')
ax.set_ylabel('Mean Final Distance (log)')
ax.set_title('Spread Comparison: Different Step Distributions')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

print("Slope (log-log), which is exponent β in r ~ n^β:")
for walk_type, distances in results.items():
    log_steps = np.log(step_counts)
    log_distances = np.log(distances)
    slope = np.polyfit(log_steps, log_distances, 1)[0]
    print(f"  {walk_type:12s}: β = {slope:.3f} {'(close to √n=0.5)' if abs(slope - 0.5) < 0.1 else ''}")
```

**Expected output:** Fixed and exponential are close to √n (β ≈ 0.5), while power-law (Lévy) spreads faster (β ≈ 0.67 for α=1.5, since β ≈ 1/α).

---

**6. Direction persistence**

```python
from simulations import simulate_correlated_random_walk_2d, extract_step_lengths
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
num_steps = 3000

# Low and high persistence
x_low, y_low = simulate_correlated_random_walk_2d(num_steps, persistence=0.1)
x_high, y_high = simulate_correlated_random_walk_2d(num_steps, persistence=0.5)

steps_low = extract_step_lengths(x_low, y_low)
steps_high = extract_step_lengths(x_high, y_high)

straightness_low = np.sqrt(x_low[-1]**2 + y_low[-1]**2) / np.sum(steps_low)
straightness_high = np.sqrt(x_high[-1]**2 + y_high[-1]**2) / np.sum(steps_high)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(x_low, y_low, linewidth=0.3, alpha=0.7)
axes[0].scatter([0], [0], color='red', s=100, zorder=5)
axes[0].set_title(f'Low Persistence (σ=0.1)\nStraightness={straightness_low:.3f}')
axes[0].set_aspect('equal')
axes[0].grid(True, alpha=0.3)

axes[1].plot(x_high, y_high, linewidth=0.3, alpha=0.7)
axes[1].scatter([0], [0], color='red', s=100, zorder=5)
axes[1].set_title(f'High Persistence (σ=0.5)\nStraightness={straightness_high:.3f}')
axes[1].set_aspect('equal')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Straightness comparison:")
print(f"  Low persistence (σ=0.1):  {straightness_low:.4f}")
print(f"  High persistence (σ=0.5): {straightness_high:.4f}")
```

**Expected output:** High persistence leads to straighter paths (higher straightness value). The path looks more "committed" to a direction.

---

**7. The Lévy hypothesis in action**

```python
from simulations import (simulate_levy_flight_2d, 
                         simulate_ideal_random_walk_2d,
                         extract_step_lengths)
import numpy as np

# Place 10 food items randomly
np.random.seed(42)
num_food = 10
food_x = np.random.uniform(-50, 50, num_food)
food_y = np.random.uniform(-50, 50, num_food)

def find_food(x, y, food_x, food_y, max_distance=2.0):
    """Find if walk visits any food within max_distance."""
    for i in range(1, len(x)):
        for fx, fy in zip(food_x, food_y):
            dist = np.sqrt((x[i] - fx)**2 + (y[i] - fy)**2)
            if dist < max_distance:
                return i  # Return step number when food found
    return None

# Compare walkers
num_trials = 20
steps_to_food_levy = []
steps_to_food_ideal = []

for trial in range(num_trials):
    # Lévy flight
    x, y = simulate_levy_flight_2d(10000, alpha=1.5)
    steps = find_food(x, y, food_x, food_y, max_distance=2.0)
    if steps is not None:
        steps_to_food_levy.append(steps)
    
    # Ideal walk
    x, y = simulate_ideal_random_walk_2d(10000)
    steps = find_food(x, y, food_x, food_y, max_distance=2.0)
    if steps is not None:
        steps_to_food_ideal.append(steps)

print(f"Finding food in sparse environment:")
print(f"  Lévy flights: found food in {len(steps_to_food_levy)}/{num_trials} trials")
if steps_to_food_levy:
    print(f"    Mean steps to food: {np.mean(steps_to_food_levy):.0f}")
print(f"  Ideal walks: found food in {len(steps_to_food_ideal)}/{num_trials} trials")
if steps_to_food_ideal:
    print(f"    Mean steps to food: {np.mean(steps_to_food_ideal):.0f}")

if len(steps_to_food_levy) > 0 and len(steps_to_food_ideal) > 0:
    ratio = np.mean(steps_to_food_ideal) / np.mean(steps_to_food_levy)
    print(f"\nLévy flights are {ratio:.1f}x faster at finding food")
```

**Expected output:** Lévy flights find food faster (in fewer steps) because the long jumps help explore the sparse environment more efficiently.

---

## Challenge Solutions

**8. Multi-species analysis**

```python
from simulations import simulate_realistic_animal_track, extract_step_lengths, fit_power_law_exponent
import numpy as np
import matplotlib.pyplot as plt

species_list = ['albatross', 'turtle', 'bacterium', 'default']
results = {}

for species in species_list:
    x, y = simulate_realistic_animal_track(5000, species=species)
    steps = extract_step_lengths(x, y)
    alpha = fit_power_law_exponent(steps, x_min=0.5)
    results[species] = {'steps': steps, 'alpha': alpha}

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for ax, species in zip(axes, species_list):
    steps = results[species]['steps']
    alpha = results[species]['alpha']
    
    sorted_steps = np.sort(steps)
    ccdf = 1 - np.arange(len(sorted_steps)) / len(sorted_steps)
    
    ax.loglog(sorted_steps, ccdf, 'o-', markersize=2, alpha=0.7)
    ax.set_title(f"{species}: α ≈ {alpha:.2f}")
    ax.set_xlabel('Step Length')
    ax.set_ylabel('P(S > s)')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Power-law exponents by species:")
for species in species_list:
    print(f"  {species:12s}: α = {results[species]['alpha']:.3f}")
```

**Expected output:** Albatross and turtle show more power-law-like behavior (lower α, more extreme jumps), while bacterium and default show more exponential behavior (higher α, closer to 2).

---

**9. Anomalous diffusion**

```python
from simulations import (simulate_ideal_random_walk_2d, 
                         simulate_correlated_random_walk_2d,
                         simulate_levy_flight_2d)
import numpy as np
import matplotlib.pyplot as plt

step_counts = np.logspace(1, 4, 8, dtype=int)  # 10 to 10000 steps
num_replicates = 10

results = {
    'ideal': [],
    'exponential': [],
    'levy_1.5': []
}

for num_steps in step_counts:
    for walk_type in results:
        distances_squared = []
        for _ in range(num_replicates):
            if walk_type == 'ideal':
                x, y = simulate_ideal_random_walk_2d(num_steps)
            elif walk_type == 'exponential':
                x, y = simulate_correlated_random_walk_2d(num_steps, step_dist='exponential')
            else:  # levy
                x, y = simulate_levy_flight_2d(num_steps, alpha=1.5)
            
            r_squared = x[-1]**2 + y[-1]**2
            distances_squared.append(r_squared)
        
        results[walk_type].append(np.mean(distances_squared))

fig, ax = plt.subplots(figsize=(10, 6))

for walk_type, r_squared_vals in results.items():
    ax.loglog(step_counts, r_squared_vals, 'o-', label=walk_type, linewidth=2, markersize=8)

# Reference lines
slope_ideal = 1.0
slope_levy = 2 / 1.5  # Approximately 1.33

ax.loglog(step_counts, (step_counts / step_counts[0])**slope_ideal * results['ideal'][0], 
          'k--', alpha=0.3, label=f'n^{slope_ideal}')
ax.loglog(step_counts, (step_counts / step_counts[0])**slope_levy * results['levy_1.5'][0], 
          'r--', alpha=0.3, label=f'n^{slope_levy:.2f}')

ax.set_xlabel('Number of Steps (log)')
ax.set_ylabel('<r²> (log)')
ax.set_title('Anomalous Diffusion')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

# Compute exponents
print("Anomalous diffusion exponents (β where <r²> ~ n^β):")
for walk_type, r_squared_vals in results.items():
    log_steps = np.log(step_counts)
    log_r2 = np.log(r_squared_vals)
    beta = np.polyfit(log_steps, log_r2, 1)[0]
    print(f"  {walk_type:15s}: β = {beta:.3f}")
```

**Expected output:** Ideal and exponential have β ≈ 1 (normal diffusion). Lévy flight has β ≈ 1.33 (superdiffusion).

---

**10. Power-law fitting with noise**

```python
from simulations import fit_power_law_exponent
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
true_alpha = 1.6
num_trials = 50
noise_level = 0.2

estimates = []

for trial in range(num_trials):
    # Generate Lévy flight with power-law steps
    steps = np.random.pareto(a=true_alpha) + 1.0
    for _ in range(4999):
        steps = np.append(steps, np.random.pareto(a=true_alpha) + 1.0)
    
    # Add noise
    noise = 1 + noise_level * np.random.randn(len(steps))
    steps_noisy = steps * noise
    
    alpha_est = fit_power_law_exponent(steps_noisy, x_min=0.5)
    estimates.append(alpha_est)

estimates = np.array(estimates)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(estimates, bins=15, edgecolor='black', alpha=0.7)
ax.axvline(true_alpha, color='red', linestyle='--', linewidth=2, label=f'True α = {true_alpha}')
ax.axvline(np.mean(estimates), color='green', linestyle='--', linewidth=2, label=f'Mean estimate = {np.mean(estimates):.3f}')
ax.set_xlabel('Estimated α')
ax.set_ylabel('Count')
ax.set_title(f'Effect of {noise_level*100:.0f}% Multiplicative Noise on Power-Law Exponent')
ax.legend()
plt.tight_layout()
plt.show()

print(f"With {noise_level*100:.0f}% noise:")
print(f"  True α: {true_alpha}")
print(f"  Mean estimate: {np.mean(estimates):.3f}")
print(f"  Std of estimates: {np.std(estimates):.4f}")
print(f"  Bias: {np.mean(estimates) - true_alpha:.4f}")
```

**Expected output:** Noise introduces systematic bias and increased variance. Estimates may shift by 0.05-0.1 depending on noise level.

---

**11. Optimal search strategy**

```python
from simulations import (simulate_ideal_random_walk_2d, 
                         simulate_correlated_random_walk_2d,
                         simulate_levy_flight_2d)
import numpy as np

# Food setup
num_food = 10
food_density = 1 / 100  # 1 food per 100 square units
area = 10000

food_x = np.random.uniform(0, 100, num_food)
food_y = np.random.uniform(0, 100, num_food)

def count_food_found(x, y, food_x, food_y, detection_radius=1.0):
    """Count how many food items are visited."""
    visited = set()
    for i in range(len(x)):
        for j, (fx, fy) in enumerate(zip(food_x, food_y)):
            dist = np.sqrt((x[i] - fx)**2 + (y[i] - fy)**2)
            if dist < detection_radius:
                visited.add(j)
    return len(visited)

strategies = {
    'fixed': lambda n: simulate_ideal_random_walk_2d(n),
    'exponential': lambda n: simulate_correlated_random_walk_2d(n, step_dist='exponential'),
    'levy_1.5': lambda n: simulate_levy_flight_2d(n, alpha=1.5),
    'levy_1.7': lambda n: simulate_levy_flight_2d(n, alpha=1.7),
    'levy_1.9': lambda n: simulate_levy_flight_2d(n, alpha=1.9),
}

energy = 10000
num_trials = 10

results = {strategy: [] for strategy in strategies}

for trial in range(num_trials):
    for strategy, func in strategies.items():
        x, y = func(energy)
        food_found = count_food_found(x, y, food_x, food_y, detection_radius=1.0)
        results[strategy].append(food_found)

print("Food found (mean ± std across 10 trials):")
for strategy, counts in results.items():
    mean_count = np.mean(counts)
    std_count = np.std(counts)
    print(f"  {strategy:15s}: {mean_count:4.1f} ± {std_count:.1f}")

best_strategy = max(results.items(), key=lambda x: np.mean(x[1]))
print(f"\nBest strategy: {best_strategy[0]} with {np.mean(best_strategy[1]):.1f} food items on average")
```

**Expected output:** Lévy flights (especially α around 1.5-1.7) typically find more food than fixed or pure exponential walks.

---

## Thought Experiments

**12. Why not always Lévy?**

Possible constraints:
1. **Predation risk:** Making long jumps might expose you to predators or risky environments.
2. **Energy cost:** Large jumps might be metabolically expensive or require more energy than small steps.
3. **Terrain constraints:** Real environments have obstacles, cliffs, and barriers that penalize long jumps.
4. **Social constraints:** Group animals can't disperse too widely without losing contact.
5. **Patchy environments:** If food is clustered, overshooting with large jumps wastes time and energy.

**13. Brownian vs. Lévy**

Consequences of superdiffusion:
- Reaches boundaries/walls faster (might get trapped or fall off cliffs)
- Harder to stay within a home range or territory
- May overshoots resources and miss smaller patches
- In hostile environments, faster spread = higher predation risk
- But in sparse, unpredictable environments, the exploration advantage outweighs the risks

**14. From discrete to continuous**

Real modifications:
- **Continuous-time RW:** Variable waiting times between steps; can model rest periods or energy depletion
- **Drift:** Preferred direction changes effective diffusion (systematic movement toward/away)
- **Obstacles:** Reflecting boundaries, absorbing barriers, patchy habitats
- **Heterogeneous environment:** Variable step size or speed depending on terrain
- **Sensory feedback:** Not purely random; biased toward promising directions

**15. Biological reality check**

(This requires actual data; discussion points depend on what you find.)

Typical outcomes:
- Many species show power-law-like tails but not perfect power laws
- Transitions between behaviors (local search vs. long-range movement)
- Environmental factors strongly influence step distributions
- Seasonal/daily variations in movement patterns
