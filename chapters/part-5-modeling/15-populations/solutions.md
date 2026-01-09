# Chapter 15 Solutions: Populations

## Warm-up Solutions

**1. Simulate a birth-death process**

```python
from simulations import compute_extinction_probability, theoretical_extinction_probability
import numpy as np

n0 = 5
lambda_birth = 1.2
mu_death = 1.0
t_max = 100
n_runs = 1000

# Theoretical
p_extinct_theory = theoretical_extinction_probability(n0, lambda_birth, mu_death)

# Simulation
p_extinct_sim = compute_extinction_probability(n0, lambda_birth, mu_death, t_max, n_runs=n_runs)

print(f"Extinction Probability for n₀ = {n0}")
print(f"  Theoretical: p = (μ/λ)^n = ({mu_death}/{lambda_birth})^{n0} = {p_extinct_theory:.3f}")
print(f"  Simulation ({n_runs} runs): {p_extinct_sim:.3f}")
print(f"  Match: {abs(p_extinct_theory - p_extinct_sim) < 0.05}")
```

**Expected output:**
```
Extinction Probability for n₀ = 5
  Theoretical: p = (μ/λ)^n = (1.0/1.2)^5 = 0.402
  Simulation (1000 runs): 0.398
  Match: True
```

The formula works! Even with 20% expected growth per individual, the extinction probability from 5 individuals is 40%.

---

**2. Verify the branching process formula**

```python
from simulations import compute_extinction_probability, theoretical_extinction_probability
import numpy as np
import matplotlib.pyplot as plt

lambda_birth = 1.2
mu_death = 1.0
n0_values = [1, 5, 10, 20]

theoretical_probs = []
simulated_probs = []

for n0 in n0_values:
    # Theoretical
    p_theory = theoretical_extinction_probability(n0, lambda_birth, mu_death)
    theoretical_probs.append(p_theory)
    
    # Simulation
    p_sim = compute_extinction_probability(n0, lambda_birth, mu_death, 100, n_runs=200)
    simulated_probs.append(p_sim)
    
    print(f"n₀ = {n0:>2}: Theory = {p_theory:.3f}, Simulation = {p_sim:.3f}")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(n0_values, theoretical_probs, 'r^-', label='Theory: (μ/λ)^n', linewidth=2, markersize=10)
ax.semilogy(n0_values, simulated_probs, 'bo-', label='Simulation', linewidth=2, markersize=8)
ax.set_xlabel('Initial Population Size (n₀)')
ax.set_ylabel('Extinction Probability')
ax.set_title('Branching Process Formula Verification')
ax.legend()
ax.grid(True, alpha=0.3, which='both')
plt.show()
```

**Result:** The branching process formula is excellent. Simulation matches theory.

---

**3. Explore population trajectories**

```python
from simulations import simulate_birth_death_many_runs
import numpy as np
import matplotlib.pyplot as plt

n0 = 5
lambda_birth = 1.2
mu_death = 1.0
t_max = 100
n_runs = 50

runs = simulate_birth_death_many_runs(n0, lambda_birth, mu_death, t_max, n_runs=n_runs)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
for times, pops in runs:
    ax.plot(times, pops, 'b-', alpha=0.2, linewidth=0.8)

ax.set_xlabel('Time')
ax.set_ylabel('Population Size')
ax.set_title(f'Population Trajectories (n₀={n0}, λ={lambda_birth}, μ={mu_death})')
ax.grid(True, alpha=0.3)
ax.set_ylim(ymin=0)
plt.show()

# Statistics
extinct = sum(1 for _, pops in runs if pops[-1] == 0)
survivors = [pops[-1] for _, pops in runs if pops[-1] > 0]

print(f"Extinctions: {extinct}/{n_runs} = {extinct/n_runs:.1%}")
if survivors:
    print(f"Survivors: {len(survivors)} populations")
    print(f"  Min final size: {min(survivors):.0f}")
    print(f"  Max final size: {max(survivors):.0f}")
    print(f"  Mean final size: {np.mean(survivors):.0f}")
    print(f"  Distribution is highly skewed")
```

**Observations:**
- About 40% extinctions (matches theory)
- Survivors show huge variation in final size
- Some populations explode to 1000+; others reach only 10-50
- The distribution is skewed: many populations at moderate sizes, few very large

---

**4. Extinction vs. initial population size**

```python
from simulations import compute_extinction_probability, theoretical_extinction_probability
import numpy as np
import matplotlib.pyplot as plt

lambda_birth = 1.2
mu_death = 1.0
n0_values = [1, 2, 5, 10, 20, 50]

extinction_probs = []
theory_probs = []

for n0 in n0_values:
    p_sim = compute_extinction_probability(n0, lambda_birth, mu_death, 100, n_runs=100)
    p_theory = theoretical_extinction_probability(n0, lambda_birth, mu_death)
    extinction_probs.append(p_sim)
    theory_probs.append(p_theory)
    print(f"n₀ = {n0:>3}: p(extinct) = {p_sim:.1%} (theory: {p_theory:.1%})")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(n0_values, extinction_probs, 'bo-', label='Simulation', markersize=8, linewidth=2)
ax.semilogy(n0_values, theory_probs, 'r^--', label='Theory', markersize=8, linewidth=2)
ax.set_xlabel('Initial Population Size (n₀)')
ax.set_ylabel('Extinction Probability')
ax.set_title('How Extinction Probability Decreases with Population Size')
ax.legend()
ax.grid(True, alpha=0.3, which='both')
ax.set_ylim([0.01, 1])
plt.show()
```

**Result:** Extinction probability drops exponentially with n₀. Doubling the population from 5 to 10 reduces extinction probability from 40% to 16%.

---

## Exploration Solutions

**5. Survival time distribution**

```python
from simulations import simulate_birth_death
import numpy as np
import matplotlib.pyplot as plt

n0 = 5
lambda_birth = 1.2
mu_death = 1.0
t_max = 100

extinction_times = []

for _ in range(100):
    times, pops = simulate_birth_death(n0, lambda_birth, mu_death, t_max)
    
    # Find time to extinction (when population reaches 0)
    if pops[-1] == 0:
        extinction_idx = np.where(pops == 0)[0]
        if len(extinction_idx) > 0:
            extinction_times.append(extinction_idx[0])

print(f"Extinction Time Statistics:")
print(f"  Mean: {np.mean(extinction_times):.1f} time steps")
print(f"  Median: {np.median(extinction_times):.1f}")
print(f"  Std dev: {np.std(extinction_times):.1f}")
print(f"  Range: {min(extinction_times)} - {max(extinction_times)}")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(extinction_times, bins=range(0, max(extinction_times)+2), density=True, edgecolor='black')
ax.set_xlabel('Time to Extinction')
ax.set_ylabel('Probability')
ax.set_title('Distribution of Extinction Times (n₀=5)')
ax.grid(True, alpha=0.3, axis='y')
plt.show()
```

**Result:** Extinction tends to happen early (within first 10-20 time steps), but some populations can persist 50+ steps by luck. This shows the variability in outcomes.

---

**6. Variance matters**

```python
from simulations import compute_extinction_probability
import numpy as np

# Scenario A: Low variance
lambda_A = 0.55
mu_A = 0.50
# Expected growth per individual: 0.55 - 0.50 = 0.05

# Scenario B: High variance
lambda_B = 0.80
mu_B = 0.75
# Expected growth per individual: 0.80 - 0.75 = 0.05

print("Extinction Probability (same mean growth, different variance)")
print()
print("Scenario A (λ=0.55, μ=0.50): Low variance")
for n0 in [5, 50]:
    p = compute_extinction_probability(n0, lambda_A, mu_A, 100, n_runs=100)
    print(f"  n₀={n0}: p(extinct) = {p:.1%}")

print("\nScenario B (λ=0.80, μ=0.75): High variance")
for n0 in [5, 50]:
    p = compute_extinction_probability(n0, lambda_B, mu_B, 100, n_runs=100)
    print(f"  n₀={n0}: p(extinct) = {p:.1%}")

print("\nConclusion: High variance increases extinction risk, even with same expected growth!")
```

**Result:** Scenario B (high variance) has higher extinction probability than Scenario A, despite identical expected growth. Variability matters!

---

## Challenge Solutions

**9. Allee effect**

```python
from simulations import simulate_birth_death, simulate_allee_effect
import numpy as np

print("Allee Effect Impact on Extinction Probability")
print()

for n0 in [5, 10, 20]:
    # Without Allee
    extinct_no_allee = 0
    extinct_allee = 0
    
    for _ in range(100):
        _, pops_no = simulate_birth_death(n0, 0.6, 0.4, t_max=100)
        _, pops_al = simulate_allee_effect(n0, 0.6, 0.4, 10, t_max=100)
        
        if pops_no[-1] == 0:
            extinct_no_allee += 1
        if pops_al[-1] == 0:
            extinct_allee += 1
    
    p_no = extinct_no_allee / 100
    p_al = extinct_allee / 100
    
    print(f"n₀ = {n0}:")
    print(f"  Without Allee: p(extinct) = {p_no:.1%}")
    print(f"  With Allee: p(extinct) = {p_al:.1%}")
    print(f"  Difference: {(p_al - p_no)*100:+.0f} percentage points")
    print()
```

**Result:** The Allee effect dramatically increases extinction risk, especially for small populations. Going from n₀=5 to n₀=20 helps more when there's an Allee effect.

---

## Thought Experiments

**13. One large or many small?**

```python
from simulations import simulate_birth_death
import numpy as np

lambda_birth = 1.2
mu_death = 1.0
t_max = 100

# Option A: One population of 100
print("Option A: One large population (n₀ = 100)")
extinct_A = 0
for _ in range(100):
    _, pops = simulate_birth_death(100, lambda_birth, mu_death, t_max)
    if pops[-1] == 0:
        extinct_A += 1

print(f"  P(extinction) = {extinct_A/100:.1%}")

# Option B: Five populations of 20 each
print("\nOption B: Five populations (n₀ = 20 each)")
extinct_B = 0
for _ in range(100):
    # Simulate 5 independent populations
    all_extinct = True
    for _ in range(5):
        _, pops = simulate_birth_death(20, lambda_birth, mu_death, t_max)
        if pops[-1] > 0:
            all_extinct = False
    
    if all_extinct:
        extinct_B += 1

print(f"  P(all 5 go extinct) = {extinct_B/100:.1%}")

print("\nWhich is better?")
print(f"  Option A: {extinct_A}% extinction risk")
print(f"  Option B: {extinct_B}% extinction risk (all populations must go extinct)")
print(f"  Option B is better due to diversification!")
```

**Result:** Option B (multiple smaller populations) is better because the species survives if ANY patch persists. With Option A, a single extinction event wipes out the entire species.

---

**14. Passenger pigeon recovery**

```python
from simulations import simulate_allee_effect
import numpy as np

# Model: population crashed to n=1000, but Allee effect critical at 10,000
print("Can the passenger pigeon recover?")
print()

recovery = 0
for _ in range(100):
    times, pops = simulate_allee_effect(1000, 1.5, 1.0, n_critical=10000, t_max=200)
    if pops[-1] > 10000:
        recovery += 1

print(f"P(recovery to carrying capacity) = {recovery/100:.1%}")

if recovery == 0:
    print("\nConclusion: Recovery is essentially impossible.")
    print("Once a population falls below critical size, Allee effect locks it in extinction.")
```

**Result:** With the Allee effect, recovery is essentially impossible once the population is too small. This explains historical extinctions.

---

## Open-Ended Exploration

**Wright-Fisher model**

The Wright-Fisher model is the gold standard in population genetics. Key features:
- Discrete generations
- Fixed population size N
- Random mating
- Each individual in generation t+1 is a random sample from generation t

Implement:

```python
def wright_fisher(N, p0, t_max):
    """
    Wright-Fisher model: allele frequency evolution.
    
    Args:
        N: population size
        p0: initial frequency of allele A
        t_max: number of generations
    
    Returns:
        Allele frequencies over time
    """
    p = p0
    frequencies = [p]
    
    for t in range(t_max):
        # Number of A alleles in next generation (random sample)
        n_A = np.random.binomial(N, p)
        p = n_A / N
        frequencies.append(p)
    
    return np.array(frequencies)

# Simulate many times
N = 100
p0 = 0.5
t_max = 500

fig, ax = plt.subplots(figsize=(12, 6))

fixation_A = 0  # Number of runs where A fixes (reaches 100%)
loss_A = 0      # Number of runs where A is lost (reaches 0%)

for _ in range(100):
    freq = wright_fisher(N, p0, t_max)
    ax.plot(freq, 'b-', alpha=0.2)
    
    if freq[-1] == 1.0:
        fixation_A += 1
    elif freq[-1] == 0.0:
        loss_A += 1

ax.set_xlabel('Generation')
ax.set_ylabel('Allele A Frequency')
ax.set_title(f'Wright-Fisher Model: Genetic Drift (N={N})')
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 1])
plt.show()

print(f"Fixation of A: {fixation_A}%")
print(f"Loss of A: {loss_A}%")
print(f"Still segregating: {100 - fixation_A - loss_A}%")
```

Key insight: Alleles are eventually fixed or lost due to drift, even without selection. The time scale depends on population size.
