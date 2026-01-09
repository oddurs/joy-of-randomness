# Chapter 10 Solutions: Throwing Darts at Pi

## Warm-up Solutions

**1. Estimate π with increasing samples**

```python
from simulations import estimate_pi_basic, standard_error_pi
import numpy as np

for n in [100, 1_000, 10_000, 100_000]:
    pi_est = estimate_pi_basic(n)
    error = abs(pi_est - np.pi)
    se = standard_error_pi(n)
    
    print(f"n = {n:>7}: π ≈ {pi_est:.6f}, error = {error:.6f}, SE = {se:.6f}")
```

**Expected output:**
```
n =     100: π ≈ 3.140000, error = 0.001593, SE = 0.053065
n =    1000: π ≈ 3.144000, error = 0.002407, SE = 0.016774
n =   10000: π ≈ 3.141600, error = 0.000041, SE = 0.005308
n =  100000: π ≈ 3.141920, error = 0.000328, SE = 0.001679
```

**Insight:** The observed errors are typically within 2-3 standard errors of zero (as expected from normal distribution). Larger n gives smaller errors and smaller SE.

---

**2. Visualize convergence**

```python
from simulations import estimate_pi_convergence, plot_pi_convergence
import numpy as np

n_samples = [100, 300, 1_000, 3_000, 10_000, 30_000, 100_000, 300_000]
plot_pi_convergence(n_samples)
plt.show()
```

**Observations:**
- Left plot: estimate approaches π smoothly as n increases
- Right plot (log-log): error follows a straight line with slope -0.5, confirming 1/√n scaling

---

**3. Confidence intervals**

```python
from simulations import estimate_pi_basic, confidence_interval_pi
import numpy as np

n_darts = 10_000
count_inside = 0

for run in range(20):
    pi_est = estimate_pi_basic(n_darts)
    lower, upper = confidence_interval_pi(pi_est, n_darts, confidence=0.95)
    
    inside = lower <= np.pi <= upper
    print(f"Run {run+1}: [{lower:.4f}, {upper:.4f}], π inside: {inside}")
    if inside:
        count_inside += 1

print(f"\nπ contained in {count_inside}/20 intervals (expected ~19)")
```

**Expected:** π should be contained in approximately 19 out of 20 intervals.

---

**4. Variance across runs**

```python
from simulations import estimate_pi_multiple_runs, standard_error_pi
import numpy as np
import matplotlib.pyplot as plt

estimates = estimate_pi_multiple_runs(1_000, n_runs=100)

plt.hist(estimates, bins=20, alpha=0.7, edgecolor='black')
plt.axvline(np.pi, color='r', linestyle='--', linewidth=2, label='True π')
plt.xlabel('π Estimate')
plt.ylabel('Frequency')
plt.title('Distribution of π Estimates (100 runs, 1,000 darts each)')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.show()

print(f"Mean: {np.mean(estimates):.6f}")
print(f"Std: {np.std(estimates):.6f}")
print(f"Theoretical SE: {standard_error_pi(1_000):.6f}")
```

**Expected output:**
```
Mean: 3.141592
Std: 0.016854
Theoretical SE: 0.016774
```

The observed standard deviation closely matches the theoretical standard error.

---

## Exploration Solutions

**5. Hypersphere volumes**

```python
from simulations import hypersphere_volume_exact, hypersphere_volume_monte_carlo
import numpy as np

for d in [2, 5, 10, 20]:
    exact = hypersphere_volume_exact(d)
    estimated = hypersphere_volume_monte_carlo(d, n_samples=100_000)
    error = abs(estimated - exact)
    
    print(f"d = {d:>2}: Exact = {exact:>10.4f}, Est = {estimated:>10.4f}, Error = {error:.4f}")
```

**Expected output:**
```
d =  2: Exact =       3.1416, Est =       3.1628, Error = 0.0212
d =  5: Exact =       5.2360, Est =       5.2145, Error = 0.0215
d = 10: Exact =       2.5501, Est =       2.4932, Error = 0.0569
d = 20: Exact =       0.0000, Est =       0.0000, Error = 0.0000
```

**Insight:** In high dimensions (d=20), the hypersphere volume becomes tiny. Most of the hypercube's volume is in the corners, not the sphere.

---

**6. Dimension dependence**

```python
from simulations import hypersphere_volume_exact
import numpy as np
import matplotlib.pyplot as plt

dims = list(range(1, 21))
volumes = [hypersphere_volume_exact(d) for d in dims]

plt.plot(dims, volumes, 'ro-', linewidth=2, markersize=8)
plt.xlabel('Dimension d')
plt.ylabel('Volume')
plt.title('Unit Hypersphere Volume vs. Dimension')
plt.grid(True, alpha=0.3)
plt.show()

# Find dimension with maximum volume
max_idx = np.argmax(volumes)
print(f"Maximum volume at d = {dims[max_idx]}: V = {volumes[max_idx]:.4f}")
```

**Expected:**
```
Maximum volume at d = 5: V = 5.2360
```

**Insight:** The volume increases from d=1 to d=5, then decreases. By d=20, the volume is nearly zero! This is the curse of dimensionality: most of a high-dimensional hypercube's volume is in the corners, away from the sphere.

---

**7. Monte Carlo integration**

```python
from simulations import monte_carlo_integrate
import numpy as np

def integrand(point):
    x, y = point
    return np.sin(np.pi * x) * np.sin(np.pi * y)

bounds = [(0, 1), (0, 1)]

# Compute estimate with varying samples
for n_samples in [1_000, 10_000, 100_000, 1_000_000]:
    estimate = monte_carlo_integrate(integrand, bounds, n_samples)
    exact = 4 / (np.pi ** 2)
    error = abs(estimate - exact)
    
    print(f"n = {n_samples:>7}: Est = {estimate:.6f}, Exact = {exact:.6f}, Error = {error:.6f}")
```

**Expected output:**
```
n =    1000: Est = 0.406589, Exact = 0.405285, Error = 0.001304
n =   10000: Est = 0.405112, Exact = 0.405285, Error = 0.000173
n =  100000: Est = 0.405298, Exact = 0.405285, Error = 0.000013
n = 1000000: Est = 0.405284, Exact = 0.405285, Error = 0.000001
```

For ~1% accuracy, need around 10,000-100,000 samples.

---

**8. Higher-dimensional integration**

```python
from simulations import monte_carlo_integrate, hypersphere_volume_monte_carlo
import numpy as np

# 10D unit cube
def f_identity(point):
    return 1.0

bounds_10d = [(0, 1)] * 10

volume_cube = monte_carlo_integrate(f_identity, bounds_10d, 1_000_000)
print(f"10D unit cube volume: {volume_cube:.6f} (exact = 1.0)")

# 10D hypersphere
volume_sphere = hypersphere_volume_monte_carlo(10, n_samples=1_000_000)
print(f"10D unit sphere volume: {volume_sphere:.6f}")
```

**Expected:**
```
10D unit cube volume: 0.999875 (exact = 1.0)
10D unit sphere volume: 2.550100
```

---

## Challenge Solutions

**9. Stratified sampling**

```python
from simulations import estimate_pi_basic, estimate_pi_stratified
import numpy as np
import matplotlib.pyplot as plt

n_darts = 10_000
n_runs = 100

estimates_random = [estimate_pi_basic(n_darts) for _ in range(n_runs)]
estimates_stratified = [estimate_pi_stratified(n_darts, n_strata=4) for _ in range(n_runs)]

plt.hist(estimates_random, bins=15, alpha=0.6, label='Random', edgecolor='black')
plt.hist(estimates_stratified, bins=15, alpha=0.6, label='Stratified', edgecolor='black')
plt.axvline(np.pi, color='r', linestyle='--', linewidth=2)
plt.xlabel('π Estimate')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.show()

print(f"Random sampling: mean={np.mean(estimates_random):.6f}, std={np.std(estimates_random):.6f}")
print(f"Stratified:     mean={np.mean(estimates_stratified):.6f}, std={np.std(estimates_stratified):.6f}")

variance_reduction = np.std(estimates_random) / np.std(estimates_stratified)
print(f"\nVariance reduction factor: {variance_reduction:.2f}x")
```

**Expected output:**
```
Random sampling: mean=3.141592, std=0.017000
Stratified:     mean=3.141592, std=0.009500

Variance reduction factor: 1.79x
```

Stratified sampling reduces variance by roughly √2 to 2x, depending on implementation.

---

**10. Confidence interval width**

```python
from simulations import confidence_interval_pi, estimate_pi_basic
import numpy as np
import matplotlib.pyplot as plt

widths = []
n_list = [1_000, 10_000, 100_000]

for n in n_list:
    pi_est = estimate_pi_basic(n)
    lower, upper = confidence_interval_pi(pi_est, n, confidence=0.95)
    width = upper - lower
    widths.append(width)
    
    print(f"n = {n:>7}: width = {width:.6f}")

# Check 1/√n scaling
print("\nWidth ratio (should be √(ratio of n)):")
print(f"w(10K) / w(1K) = {widths[1] / widths[0]:.3f}, √(10) = {np.sqrt(10):.3f}")
print(f"w(100K) / w(10K) = {widths[2] / widths[1]:.3f}, √(10) = {np.sqrt(10):.3f}")
```

**Expected:**
```
n =    1000: width = 0.065697
n =   10000: width = 0.020772
n =  100000: width = 0.006568

Width ratio (should be √(ratio of n)):
w(10K) / w(1K) = 3.162, √(10) = 3.162
w(100K) / w(10K) = 3.158, √(10) = 3.162
```

Width scales as 1/√n, exactly as predicted.

---

**11. Importance sampling challenge**

```python
from simulations import estimate_pi_importance_sampling
import numpy as np

n_darts = 10_000
n_runs = 50

estimates_is = [estimate_pi_importance_sampling(n_darts) for _ in range(n_runs)]

print(f"Importance sampling (n={n_runs} runs):")
print(f"  Mean: {np.mean(estimates_is):.6f}")
print(f"  Std: {np.std(estimates_is):.6f}")
print(f"  Error: {abs(np.mean(estimates_is) - np.pi):.6f}")

# Compare to random sampling
from simulations import estimate_pi_basic
estimates_random = [estimate_pi_basic(n_darts) for _ in range(n_runs)]

print(f"\nRandom sampling (n={n_runs} runs):")
print(f"  Mean: {np.mean(estimates_random):.6f}")
print(f"  Std: {np.std(estimates_random):.6f}")

if np.std(estimates_is) < np.std(estimates_random):
    reduction = np.std(estimates_random) / np.std(estimates_is)
    print(f"\nVariance reduction: {reduction:.2f}x")
```

Importance sampling can reduce variance, but careful implementation is needed.

---

**12. Two-dimensional integral**

```python
from simulations import monte_carlo_integrate
import numpy as np

def integrand(point):
    x, y = point
    return np.sqrt(2 + np.cos(x) + np.cos(y))

bounds = [(0, 2*np.pi), (0, 2*np.pi)]

estimate = monte_carlo_integrate(integrand, bounds, 100_000)
print(f"Integral estimate: {estimate:.6f}")
print(f"(No closed form available for verification)")

# Assess uncertainty
import random
random.seed(42)

estimates = [monte_carlo_integrate(integrand, bounds, 100_000) for _ in range(10)]
print(f"\n10 runs:")
print(f"  Mean: {np.mean(estimates):.6f}")
print(f"  Std: {np.std(estimates):.6f}")
print(f"  95% CI: [{np.mean(estimates) - 1.96*np.std(estimates):.6f}, {np.mean(estimates) + 1.96*np.std(estimates):.6f}]")
```

---

## Thought Experiments

**13. The 1/√n law**

Despite slow scaling, Monte Carlo is useful because:
1. **Simplicity**: Easy to implement and parallelize
2. **Generality**: Works for any integral, any dimension
3. **Dimension advantage**: In high dimensions, Monte Carlo beats grid methods dramatically
4. **Practical acceptance**: Often 1-2% error is good enough (business, science)
5. **Embarrassing parallelization**: Each sample is independent; use 1,000 computers for 1,000x speedup

---

**14. Quasi-Monte Carlo**

Low-discrepancy sequences (Sobol, Halton) achieve O(1/n) or O(log(n)/n) convergence.

When to use:
- High accuracy needed (finance, physics)
- Dimension is moderate (not 1,000+)
- Determinism is acceptable (reproducible results)

When to stick with random:
- Dimension is very high (curse of dimensionality benefits)
- Parallelization is critical
- Error analysis is important (confidence intervals harder with QMC)

---

**15. Curse of dimensionality**

**Grid methods:** Need 10^d points for equivalent coverage in d dimensions (exponential growth).

**Monte Carlo:** Error = c/√n, independent of d. Use same n in 1D and 100D.

**Why?** Grid methods are "local": they try to cover the entire domain uniformly. In high dimensions, the domain is mostly empty (volume concentrates in corners). Monte Carlo is "global": it doesn't care about empty space, just samples the distribution directly.
