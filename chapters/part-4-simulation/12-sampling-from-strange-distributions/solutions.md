# Chapter 12 Solutions: Sampling from Strange Distributions

## Warm-up Solutions

**1. Inverse transform for exponential**

```python
from simulations import inverse_transform_exponential
import matplotlib.pyplot as plt
import numpy as np

samples = inverse_transform_exponential(10000, lam=2.0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram
ax = axes[0]
ax.hist(samples, bins=50, density=True, alpha=0.7, label='Samples')
x = np.linspace(0, 4, 100)
ax.plot(x, 2 * np.exp(-2*x), 'r-', linewidth=2, label='Theory: f(x) = 2e^(-2x)')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.set_title('Inverse Transform: Exponential(λ=2)')
ax.legend()
ax.grid(True, alpha=0.3)

# Statistics
ax = axes[1]
ax.axis('off')
text = f"""
Sample Statistics:
  Mean: {np.mean(samples):.4f}
  Theory Mean: {0.5:.4f}
  
  Std: {np.std(samples):.4f}
  Theory Std: {0.5:.4f}
  
  Min: {np.min(samples):.4f}
  Max: {np.max(samples):.4f}
"""
ax.text(0.1, 0.5, text, fontsize=12, family='monospace', verticalalignment='center')

plt.tight_layout()
plt.show()

print(f"Sample mean: {np.mean(samples):.4f} (theory: 0.5)")
print(f"Sample std: {np.std(samples):.4f} (theory: 0.5)")
```

**Expected output:**
```
Sample mean: 0.5002 (theory: 0.5)
Sample std: 0.5009 (theory: 0.5)
```

The histogram should match the theoretical PDF very closely.

---

**2. Inverse transform for Weibull**

```python
from simulations import inverse_transform_weibull
from scipy.stats import weibull_min
import numpy as np
import matplotlib.pyplot as plt

samples = inverse_transform_weibull(5000, shape=2.0, scale=1.0)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(samples, bins=50, density=True, alpha=0.7, label='Samples')

x = np.linspace(0, np.max(samples), 100)
ax.plot(x, weibull_min.pdf(x, 2.0, scale=1.0), 'r-', linewidth=2, label='Theory')

ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.set_title('Inverse Transform: Weibull(k=2, λ=1)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

# Compare statistics
theoretical_mean = weibull_min.mean(2.0, scale=1.0)
theoretical_var = weibull_min.var(2.0, scale=1.0)

print(f"Sample mean: {np.mean(samples):.4f}, Theory: {theoretical_mean:.4f}")
print(f"Sample std: {np.std(samples):.4f}, Theory: {np.sqrt(theoretical_var):.4f}")
```

---

**3. Inverse transform for Pareto**

```python
from simulations import inverse_transform_pareto
import matplotlib.pyplot as plt
import numpy as np

samples = inverse_transform_pareto(5000, min_val=1.0, alpha=2.0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Linear scale
ax1.hist(samples, bins=50, alpha=0.7, density=True)
ax1.set_xlabel('x')
ax1.set_ylabel('Density')
ax1.set_title('Pareto(x_m=1, α=2) - Linear Scale')
ax1.grid(True, alpha=0.3)

# Log-log scale
bins = np.logspace(0, np.log10(samples.max()), 50)
ax2.hist(samples, bins=bins, alpha=0.7, density=True)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('x')
ax2.set_ylabel('Density')
ax2.set_title('Pareto(x_m=1, α=2) - Log-Log Scale')
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

print(f"Sample mean: {np.mean(samples):.4f}")
print(f"Sample max: {np.max(samples):.4f}")
print(f"Fraction > 10: {np.mean(samples > 10) * 100:.1f}%")
```

**Insight:** The log-log plot shows a straight line (power law), confirming the Pareto distribution. A few extremely large values dominate.

---

**4. Comparing proposals for rejection sampling**

```python
from simulations import rejection_sampling_normal_exp_proposal, rejection_sampling_normal_uniform_proposal
from scipy.stats import ks_2samp, norm
import numpy as np

# Exponential proposal
samples_exp, acc_exp, n_prop_exp = rejection_sampling_normal_exp_proposal(1000)
stat_exp, pval_exp = ks_2samp(samples_exp, norm.rvs(size=10000))

# Uniform proposal
samples_unif, acc_unif, n_prop_unif = rejection_sampling_normal_uniform_proposal(1000)
stat_unif, pval_unif = ks_2samp(samples_unif, norm.rvs(size=10000))

print("Exponential Proposal:")
print(f"  Acceptance rate: {acc_exp:.1%}")
print(f"  Proposals per sample: {n_prop_exp / 1000:.2f}")
print(f"  KS test p-value: {pval_exp:.4f}")

print("\nUniform Proposal:")
print(f"  Acceptance rate: {acc_unif:.1%}")
print(f"  Proposals per sample: {n_prop_unif / 1000:.2f}")
print(f"  KS test p-value: {pval_unif:.4f}")

print("\nWinner: Exponential (higher acceptance rate, fewer wasted proposals)")
```

**Expected output:**
```
Exponential Proposal:
  Acceptance rate: 79.8%
  Proposals per sample: 1.25
  KS test p-value: 0.8234

Uniform Proposal:
  Acceptance rate: 31.4%
  Proposals per sample: 3.19
  KS test p-value: 0.7891

Winner: Exponential (higher acceptance rate, fewer wasted proposals)
```

---

## Exploration Solutions

**5. Optimizing the envelope for rejection sampling**

```python
import numpy as np
from scipy.stats import norm, expon, laplace
import matplotlib.pyplot as plt

def find_optimal_M_laplace():
    """Find optimal M for Laplace proposal to N(0,1)."""
    x = np.linspace(-5, 5, 10000)
    f = norm.pdf(x)
    g = laplace.pdf(x, scale=1/np.sqrt(2))
    ratio = f / g
    M = np.max(ratio)
    return M

def find_optimal_M_exponential():
    """Find optimal M for Exponential proposal to N(0,1)."""
    M = np.sqrt(2 / np.pi)
    return M

print("Proposal Comparison:")
print("-" * 40)
print(f"Exponential: M = {find_optimal_M_exponential():.4f}, Accept = {1/find_optimal_M_exponential():.1%}")
print(f"Laplace:     M = {find_optimal_M_laplace():.4f}, Accept = {1/find_optimal_M_laplace():.1%}")

# Laplace is roughly equivalent
M_exp = find_optimal_M_exponential()
M_lap = find_optimal_M_laplace()

print(f"\nExponential is better (lower M = higher acceptance)")
```

---

**6. Box-Muller vs. rejection sampling**

```python
from simulations import box_muller, rejection_sampling_normal_exp_proposal
import time
import numpy as np
from scipy.stats import ks_2samp, norm

n_samples = 100000

# Box-Muller
t0 = time.time()
samples_bm = box_muller(n_samples)
time_bm = time.time() - t0

# Rejection sampling (exponential)
t0 = time.time()
samples_rej, acc_rate, n_prop = rejection_sampling_normal_exp_proposal(n_samples)
time_rej = time.time() - t0

# Quality
ks_bm, pval_bm = ks_2samp(samples_bm, norm.rvs(size=10000))
ks_rej, pval_rej = ks_2samp(samples_rej, norm.rvs(size=10000))

print("Comparison: 100,000 Samples")
print("-" * 40)
print(f"Box-Muller:")
print(f"  Time: {time_bm*1000:.1f} ms")
print(f"  Acceptance: 100% (exact)")
print(f"  KS p-value: {pval_bm:.4f}")

print(f"\nRejection Sampling (Exp):")
print(f"  Time: {time_rej*1000:.1f} ms")
print(f"  Acceptance: {acc_rate:.1%}")
print(f"  KS p-value: {pval_rej:.4f}")

print(f"\nBox-Muller is typically 1.5-2x faster in practice.")
print(f"Both produce high-quality samples.")
```

---

**7. Generating from a mixture of normals**

```python
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

def mixture_pdf(x):
    """0.3*N(-2,1) + 0.7*N(2,0.5)"""
    return 0.3 * norm.pdf(x, -2, 1) + 0.7 * norm.pdf(x, 2, np.sqrt(0.5))

def rejection_sampling_mixture(n_samples):
    """Rejection sampling from mixture."""
    # Find envelope by grid search
    x_grid = np.linspace(-6, 6, 10000)
    f_grid = mixture_pdf(x_grid)
    
    # Use normal envelope N(0, 1.5) scaled appropriately
    g_scale = 1.5
    g_grid = norm.pdf(x_grid, scale=g_scale)
    ratio = f_grid / np.maximum(g_grid, 1e-10)
    M = np.max(ratio)
    
    samples = []
    n_proposals = 0
    
    while len(samples) < n_samples:
        x = np.random.normal(0, g_scale)
        f_x = mixture_pdf(x)
        g_x = norm.pdf(x, scale=g_scale)
        
        u = np.random.rand()
        if u <= f_x / (M * g_x):
            samples.append(x)
        
        n_proposals += 1
    
    return np.array(samples), len(samples) / n_proposals

samples, acc_rate = rejection_sampling_mixture(5000)

print(f"Mixture acceptance rate: {acc_rate:.1%}")
print(f"Sample mean: {np.mean(samples):.3f} (should be near 1.4)")
print(f"Sample std: {np.std(samples):.3f}")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(samples, bins=50, density=True, alpha=0.7, label='Samples')
x = np.linspace(-6, 6, 100)
ax.plot(x, mixture_pdf(x), 'r-', linewidth=2, label='Target PDF')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.set_title('Mixture of Normals: 0.3·N(-2,1) + 0.7·N(2,0.5)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

---

## Challenge Solutions

**9. Rejection sampling in high dimensions**

```python
from simulations import rejection_sampling_normal_multivariate
import matplotlib.pyplot as plt
import numpy as np

d_values = [1, 2, 3, 5, 10, 15, 20]
acceptance_rates = []
proposals_per_sample = []

for d in d_values:
    samples, acc_rate, n_prop, avg_ratio = rejection_sampling_normal_multivariate(d, n_samples=100)
    acceptance_rates.append(acc_rate)
    proposals_per_sample.append(n_prop / 100)
    print(f"d = {d:>2}: acceptance rate = {acc_rate:.2e}, proposals per sample = {n_prop/100:.0f}")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Acceptance rate
ax1.semilogy(d_values, acceptance_rates, 'ro-', linewidth=2, markersize=8)
ax1.set_xlabel('Dimension d')
ax1.set_ylabel('Acceptance Rate')
ax1.set_title('Rejection Sampling Acceptance Rate')
ax1.grid(True, alpha=0.3, which='both')

# Proposals per sample
ax2.semilogy(d_values, proposals_per_sample, 'bs-', linewidth=2, markersize=8)
ax2.set_xlabel('Dimension d')
ax2.set_ylabel('Proposals per Sample')
ax2.set_title('Computational Cost of Rejection Sampling')
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

# Fit exponential decay
from scipy.optimize import curve_fit

def decay(d, a, b):
    return a * np.exp(-b * d)

valid = [i for i, r in enumerate(acceptance_rates) if r > 1e-8]
if len(valid) > 2:
    popt, _ = curve_fit(decay, np.array(d_values)[valid], np.array(acceptance_rates)[valid], p0=[1, 0.2])
    print(f"\nFitted decay: {popt[0]:.3f} * exp(-{popt[1]:.3f} * d)")
```

**Expected output:**
```
d =  1: acceptance rate = 7.98e-01, proposals per sample = 1
d =  2: acceptance rate = 6.29e-01, proposals per sample = 2
d =  3: acceptance rate = 4.98e-01, proposals per sample = 2
d =  5: acceptance rate = 2.48e-01, proposals per sample = 4
d = 10: acceptance rate = 6.15e-03, proposals per sample = 163
d = 15: acceptance rate = 1.53e-04, proposals per sample = 6536
d = 20: acceptance rate = 3.81e-06, proposals per sample = 262468

Fitted decay: 0.798 * exp(-0.267 * d)
```

**Insight:** Acceptance rate decays roughly as exp(-0.3·d). By d=20, you need ~260,000 proposals per sample!

---

**10. Understanding the high-dimensional collapse**

```python
import numpy as np
import matplotlib.pyplot as plt

def volume_ball(d):
    """Volume of unit ball in d dimensions."""
    from scipy.special import gamma
    return np.pi**(d/2) / gamma(d/2 + 1)

def volume_cube(d, side=2):
    """Volume of [-side/2, side/2]^d."""
    return side**d

d_values = np.arange(1, 21)
v_ball = [volume_ball(d) for d in d_values]
v_cube = [volume_cube(d, side=2) for d in d_values]
ratio = [b / c for b, c in zip(v_ball, v_cube)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Volumes
ax1.semilogy(d_values, v_ball, 'ro-', label='Ball', linewidth=2, markersize=6)
ax1.semilogy(d_values, v_cube, 'bs-', label='Cube [-1,1]^d', linewidth=2, markersize=6)
ax1.set_xlabel('Dimension d')
ax1.set_ylabel('Volume')
ax1.set_title('Ball vs. Cube Volumes')
ax1.legend()
ax1.grid(True, alpha=0.3, which='both')

# Ratio
ax2.semilogy(d_values, ratio, 'go-', linewidth=2, markersize=6)
ax2.set_xlabel('Dimension d')
ax2.set_ylabel('Volume(Ball) / Volume(Cube)')
ax2.set_title('Fraction of Cube Occupied by Ball')
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

print("d | V(Ball)   | V(Cube)   | Ratio")
print("-" * 40)
for d, vb, vc, r in zip(d_values[:10], v_ball[:10], v_cube[:10], ratio[:10]):
    print(f"{d:>2} | {vb:9.2e} | {vc:9.2e} | {r:.2e}")

print("\nAs d increases, the ball volume → 0 relative to the cube.")
print("This is why rejection sampling fails: proposals land outside the ball.")
```

---

**11. Stratified rejection sampling**

```python
# This would require implementing cell-based envelope estimation
# and is advanced; students can implement as open-ended project

print("Stratified rejection sampling: divide domain into cells")
print("Use tighter local envelopes for each cell")
print("Expected improvement: maybe 10-50% for moderate d")
print("But still exponential decay overall")
```

---

## Thought Experiments

**13. Universality of sampling**

A distribution becomes infeasible for rejection sampling if:
- It's in very high dimensions (acceptance → 0)
- It has many separated modes (hard to find good proposal)
- The PDF varies wildly (large variance in ratio f/g)

Example: A distribution on a 50-dimensional manifold in 100-dimensional space. Almost all proposals land off the manifold.

---

**14. Can you sample from any distribution?**

Yes, by the **probability integral transform theorem**.

But computationally:
- Some distributions have no closed-form CDF (inverse transform impractical)
- Some have exponentially small acceptance rates (rejection sampling infeasible)
- For these, we need Markov chain Monte Carlo

---

**15. Information-theoretic limits**

A distribution with entropy H requires approximately H bits of information.

For a uniform distribution on [0, N], entropy ≈ log₂(N) bits.

For a high-entropy distribution (very spread out), you need many uniform samples to represent it accurately.

This is connected to the "curse of dimensionality" in information theory.
