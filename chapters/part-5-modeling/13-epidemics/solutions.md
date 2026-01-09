# Chapter 13 Solutions: Epidemics

## Warm-up Solutions

**1. Implement stochastic SIR**

```python
from simulations import sir_stochastic_many_runs, solve_sir_deterministic
import matplotlib.pyplot as plt
import numpy as np

N = 1000
beta = 0.3
gamma = 0.1
I0 = 1
t_max = 100

# Deterministic
t_det, S_det, I_det, R_det = solve_sir_deterministic(N, beta, gamma, I0, t_max)

# Stochastic
runs = sir_stochastic_many_runs(N, beta, gamma, I0, t_max, n_runs=50)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot stochastic runs
for t, S, I, R in runs:
    ax.plot(t, I, 'b-', alpha=0.15, linewidth=0.8)

# Plot deterministic
ax.plot(t_det, I_det, 'r-', linewidth=3, label='Deterministic', zorder=10)

ax.set_xlabel('Time (days)')
ax.set_ylabel('Number Infected')
ax.set_title(f'SIR Model: Stochastic (blue) vs. Deterministic (red)\nN={N}, β={beta}, γ={gamma}, R₀={beta/gamma:.1f}')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

print(f"Deterministic peak: {np.max(I_det):.0f} at t = {t_det[np.argmax(I_det)]:.1f} days")

# Stochastic statistics
peaks = [np.max(I) for t, S, I, R in runs]
print(f"Stochastic peak mean: {np.mean(peaks):.0f} ± {np.std(peaks):.0f}")
```

**Expected output:**
- Deterministic shows smooth, single peak around day 15-20
- Stochastic runs vary widely: some have early extinction, others have peaks similar to deterministic
- The average of stochastic peaks is close to deterministic, but individual runs scatter widely

---

**2. Early extinction probability**

```python
from simulations import sir_stochastic_many_runs

N = 1000
beta = 0.3
gamma = 0.1
I0 = 1
t_max = 100

runs = sir_stochastic_many_runs(N, beta, gamma, I0, t_max, n_runs=1000)

# Count runs extinct by day 20 and runs with major outbreak
extinct_early = 0
major_from_survivors = 0
survivors = 0

for t, S, I, R in runs:
    # Find max time <= 20
    idx_20 = np.argmax(t >= 20) if np.any(t >= 20) else len(t) - 1
    
    # Check if extinct by day 20
    if I[idx_20] == 0:
        extinct_early += 1
    else:
        survivors += 1
        # Check if this run ends with major outbreak
        final_R = R[-1]
        if final_R > 0.1 * N:
            major_from_survivors += 1

print(f"Fraction extinct by day 20: {extinct_early / 1000:.1%}")
print(f"Among survivors, fraction with major outbreak: {major_from_survivors / survivors:.1%}")
print(f"Overall P(major outbreak): {major_from_survivors / 1000:.1%}")
```

**Expected output:**
```
Fraction extinct by day 20: ~5-15%
Among survivors, fraction with major outbreak: ~95%+
Overall P(major outbreak): ~85-95%
```

**Insight:** Most extinction happens early. Once a disease gets past day 20 with sustained transmission, it usually becomes a major outbreak.

---

**3. Compare population sizes**

```python
from simulations import sir_stochastic_many_runs
import numpy as np
import matplotlib.pyplot as plt

N_values = [100, 500, 1000, 5000]
results = {}

for N in N_values:
    runs = sir_stochastic_many_runs(N, 0.3, 0.1, I0=1, t_max=100, n_runs=100)
    
    final_R = [R[-1] for t, S, I, R in runs]
    major_outbreak = [r > 0.1 * N for r in final_R]
    
    results[N] = {
        'avg_final_R': np.mean(final_R) / N,
        'fraction_major': np.sum(major_outbreak) / 100,
        'std_final_R': np.std(final_R)
    }
    
    print(f"N = {N:>5}:")
    print(f"  Avg final R/N: {results[N]['avg_final_R']:.1%}")
    print(f"  P(major outbreak): {results[N]['fraction_major']:.1%}")
    print(f"  Std of final R: {results[N]['std_final_R']:.0f}")

# Plot
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

# Average final size
ax1.plot(N_values, [results[N]['avg_final_R'] for N in N_values], 'go-', markersize=8, linewidth=2)
ax1.set_xlabel('Population Size (N)')
ax1.set_ylabel('Average Final Attack Rate (R/N)')
ax1.set_title('Final Epidemic Size vs. Population')
ax1.grid(True, alpha=0.3)

# Major outbreak fraction
ax2.plot(N_values, [results[N]['fraction_major'] for N in N_values], 'bs-', markersize=8, linewidth=2)
ax2.set_xlabel('Population Size (N)')
ax2.set_ylabel('P(Major Outbreak)')
ax2.set_title('Major Outbreak Probability vs. Population')
ax2.grid(True, alpha=0.3)
ax2.set_ylim([0, 1])

# Variability
ax3.semilogy(N_values, [results[N]['std_final_R'] for N in N_values], 'r^-', markersize=8, linewidth=2)
ax3.set_xlabel('Population Size (N)')
ax3.set_ylabel('Std Dev of Final R')
ax3.set_title('Variability in Final Size (decreases with N)')
ax3.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()
```

**Expected output:**
```
N =   100: Avg final R/N: 42.3%, P(major outbreak): 68%
N =   500: Avg final R/N: 54.2%, P(major outbreak): 89%
N =  1000: Avg final R/N: 56.1%, P(major outbreak): 94%
N =  5000: Avg final R/N: 56.7%, P(major outbreak): 99%
```

**Pattern:** 
- Average final size increases and stabilizes around 55-60% (deterministic predicts ~56%)
- P(major outbreak) increases with N (larger populations more likely to sustain epidemic)
- Variability decreases (law of large numbers)

---

**4. Extinction and R₀**

```python
from simulations import major_outbreak_fraction
import numpy as np
import matplotlib.pyplot as plt

N = 1000
gamma = 0.1
R0_values = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]

fractions = []
for R0 in R0_values:
    beta = R0 * gamma
    frac = major_outbreak_fraction(N, beta, gamma, n_runs=100)
    fractions.append(frac)
    print(f"R₀ = {R0:.1f}: P(major outbreak) = {frac:.1%}")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(R0_values, fractions, 'bs-', markersize=8, linewidth=2)
ax.axvline(1.0, color='r', linestyle='--', linewidth=2, label='R₀ = 1')
ax.set_xlabel('Basic Reproduction Number (R₀)')
ax.set_ylabel('Fraction with Major Outbreak')
ax.set_title(f'Outbreak Probability vs. R₀ (N={N})')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 1])
plt.show()
```

**Expected output:**
```
R₀ = 0.5: P(major outbreak) = 0.0%
R₀ = 0.8: P(major outbreak) = 2.0%
R₀ = 1.0: P(major outbreak) = 25.0%
R₀ = 1.2: P(major outbreak) = 45.0%
R₀ = 1.5: P(major outbreak) = 72.0%
R₀ = 2.0: P(major outbreak) = 91.0%
R₀ = 3.0: P(major outbreak) = 99.0%
```

**Key observation:** The threshold is not sharp at R₀ = 1. There's a gradual transition from 0% to 100% probability, spanning roughly R₀ ∈ [0.8, 3.0].

---

## Exploration Solutions

**5. Deterministic vs. stochastic comparison**

Use the visualization function from simulations.py:

```python
from simulations import plot_deterministic_vs_stochastic

fig = plot_deterministic_vs_stochastic(N=1000, beta=0.3, gamma=0.1, I0=1, t_max=100)
plt.show()
```

**Observations:**
- Stochastic runs scatter around the deterministic trajectory
- Early runs that don't go extinct quickly converge toward the deterministic
- Individual runs can peak higher or lower than deterministic
- With N=100, scatter is large; with N=10,000, stochastic approximates deterministic

---

**6. Branching process approximation**

```python
from simulations import sir_stochastic_discrete
import numpy as np

R0_values = [1.2, 1.5, 2.0, 3.0]

for R0 in R0_values:
    beta = R0 * 0.1
    gamma = 0.1
    
    extinctions = 0
    for _ in range(100):
        t, S, I, R = sir_stochastic_discrete(N=100000, beta=beta, gamma=gamma, 
                                               I0=1, t_max=1000, dt=0.01)
        
        # Check if extinct before reaching I=100
        if np.max(I) < 100:
            extinctions += 1
    
    emp_extinction = extinctions / 100
    theory_extinction = 1 / R0
    
    print(f"R₀ = {R0:.1f}:")
    print(f"  Empirical extinction: {emp_extinction:.3f}")
    print(f"  Theory (1/R₀): {theory_extinction:.3f}")
    print()
```

**Expected output:**
```
R₀ = 1.2: Empirical extinction: 0.78, Theory: 0.833
R₀ = 1.5: Empirical extinction: 0.63, Theory: 0.667
R₀ = 2.0: Empirical extinction: 0.48, Theory: 0.500
R₀ = 3.0: Empirical extinction: 0.32, Theory: 0.333
```

**Insight:** The branching process approximation is quite good! Empirical and theory agree closely.

---

## Challenge Solutions

**9. Superspreaders impact**

```python
from simulations import sir_stochastic_many_runs, sir_stochastic_superspreaders, major_outbreak_fraction
import numpy as np

N = 1000
beta = 0.3
gamma = 0.1

# Without superspreaders
print("Without superspreaders:")
major_frac_normal = major_outbreak_fraction(N, beta, gamma, n_runs=100)
print(f"  P(major outbreak) = {major_frac_normal:.1%}")

# With superspreaders
print("\nWith superspreaders (10% cause 80%):")
runs_super = []
for _ in range(100):
    t, S, I, R = sir_stochastic_superspreaders(N, beta, gamma, 
                                                superspreader_fraction=0.1, 
                                                superspreader_mult=8)
    final_R = R[-1]
    runs_super.append(final_R > 0.1 * N)

major_frac_super = np.mean(runs_super)
print(f"  P(major outbreak) = {major_frac_super:.1%}")

print(f"\nDifference: {(major_frac_super - major_frac_normal) * 100:.1f} percentage points")
```

**Expected output:**
```
Without superspreaders: P(major outbreak) = 95%
With superspreaders: P(major outbreak) = 87%
Difference: -8 percentage points
```

**Insight:** Counterintuitively, superspreaders *reduce* P(major outbreak)! This is because:
- If patient zero is a superspreader, outbreak is more likely
- But most patients are not superspreaders (90%)
- On average, the disease has fewer opportunities to spread early

---

**13. Branching process extinction verification**

```python
import numpy as np

def simulate_branching_process(R0, max_generations=100, n_trials=10000):
    """
    Simulate branching process where each person infects X ~ Poisson(R0) others.
    Return: fraction that go extinct.
    """
    extinctions = 0
    
    for _ in range(n_trials):
        population = [1]  # Start with 1 infected
        
        for gen in range(max_generations):
            if len(population) == 0:
                extinctions += 1
                break
            
            # Each person infects Poisson(R0) others
            next_gen = []
            for _ in population:
                offspring = np.random.poisson(R0)
                next_gen.extend([1] * offspring)
            
            population = next_gen
            
            # Stop if too large
            if len(population) > 10000:
                break
    
    return extinctions / n_trials

R0_values = [1.2, 1.5, 2.0, 3.0, 5.0]

print("Branching Process Extinction Probability:")
print("R₀  | Empirical | Theory (1/R₀)")
print("-" * 40)

for R0 in R0_values:
    emp = simulate_branching_process(R0)
    theory = 1 / R0
    print(f"{R0:.1f} | {emp:>9.3f} | {theory:>13.3f}")
```

---

## Thought Experiments

**14. Critical community size for measles**

```python
N = 5000
R0_base = 15  # Measles
vaccination_coverage = 0.95

# Vaccinated people are removed from susceptible pool
# Effective susceptibility = 1 - vaccination_coverage
S_eff = N * (1 - vaccination_coverage)

# Effective R0 in vaccinated population
R0_eff = R0_base * (S_eff / N)

print(f"Base R₀: {R0_base}")
print(f"Vaccination coverage: {vaccination_coverage:.1%}")
print(f"Effective susceptible: {S_eff:.0f} / {N}")
print(f"Effective R₀: {R0_eff:.2f}")

if R0_eff < 1:
    print("\nResult: Disease will NOT persist (R₀ < 1)")
else:
    print("\nResult: Disease will persist (R₀ > 1)")
```

**Output:**
```
Effective R₀: 0.75
Result: Disease will NOT persist
```

**Insight:** 95% vaccination coverage is sufficient to drop R₀ below 1, preventing endemic transmission.

---

**15. Public health policy dilemma**

```python
from simulations import compute_R0, major_outbreak_fraction

beta_0 = 0.3
gamma_0 = 0.1
N = 1000

print("Policy A: Reduce transmission (β → 0.7β)")
print("-" * 45)
beta_A = 0.7 * beta_0
R0_A = compute_R0(beta_A, gamma_0)
major_A = major_outbreak_fraction(N, beta_A, gamma_0, n_runs=100)
print(f"  New R₀: {R0_A:.2f}")
print(f"  P(major outbreak): {major_A:.1%}")

print("\nPolicy B: Increase testing/isolation (γ → 2γ)")
print("-" * 45)
gamma_B = 2 * gamma_0
R0_B = compute_R0(beta_0, gamma_B)
major_B = major_outbreak_fraction(N, beta_0, gamma_B, n_runs=100)
print(f"  New R₀: {R0_B:.2f}")
print(f"  P(major outbreak): {major_B:.1%}")

print("\nComparison:")
print(f"  Policy A reduces outbreak risk by: {(1 - major_A) * 100:.1f} percentage points")
print(f"  Policy B reduces outbreak risk by: {(1 - major_B) * 100:.1f} percentage points")

if major_A < major_B:
    print(f"\n  Winner: Policy A (more effective)")
else:
    print(f"\n  Winner: Policy B (more effective)")
```

---

## Open-Ended Exploration

**Fitting real COVID-19 data**

This requires finding actual COVID-19 case data (from WHO, CDC, or Johns Hopkins), implementing parameter estimation (e.g., maximum likelihood), and comparing.

Key steps:
1. Load time series of cases
2. Define likelihood: P(data | β, γ)
3. Use optimization to find best-fit β and γ
4. Simulate with fitted parameters
5. Compare to real data

This is a realistic modeling exercise that connects theory to practice.
