# Chapter 17 Solutions: Markov Chain Monte Carlo

## Warm-up Solutions

**1. Implement Metropolis-Hastings**

```python
from simulations import metropolis_hastings, log_normal_density

# Target: N(0, 1)
def log_density(x):
    return log_normal_density(x, mean=0, var=1)

# Run MCMC
samples, acceptance_rate = metropolis_hastings(
    log_density, 
    initial_state=0,
    proposal_scale=0.5,
    n_iterations=5000
)

# Post burn-in
samples_post = samples[1000:]

print(f"Acceptance rate: {acceptance_rate:.1%}")
print(f"Mean: {np.mean(samples_post):.3f}")
print(f"Std dev: {np.std(samples_post):.3f}")
```

**Output (typical):**
```
Acceptance rate: 67.4%
Mean: -0.014
Std dev: 1.035
```

The sampler works! The acceptance rate of 67% is a bit high (ideal is 20-50%), suggesting the proposal could be wider, but the posterior estimates match the target.

---

**2. Diagnose convergence with trace plots**

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(12, 8))

for idx, initial_state in enumerate([0, 10, -20]):
    samples, _ = metropolis_hastings(log_density, initial_state, 0.5, 5000)
    
    ax = axes[idx]
    ax.plot(samples, alpha=0.7)
    ax.axhline(0, color='k', linestyle='--', alpha=0.3)
    ax.set_ylabel(f'θ (start={initial_state})')
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel('Iteration')
plt.suptitle('Convergence from Different Starting Points')
plt.tight_layout()
plt.show()
```

**Observations:**
- θ₀ = 0: settles immediately (about 100-200 iterations)
- θ₀ = 10: takes longer, about 500-1000 iterations to settle
- θ₀ = -20: similar, about 500-1000 iterations

**Burn-in recommendation:** 1000 iterations is safe for all starting points.

---

**3. Effect of proposal scale**

```python
from simulations import metropolis_hastings
import matplotlib.pyplot as plt

proposal_scales = [0.1, 0.5, 2.0]
fig, axes = plt.subplots(len(proposal_scales), 2, figsize=(12, 9))

for idx, scale in enumerate(proposal_scales):
    samples, acc_rate = metropolis_hastings(log_density, 0, scale, 2000)
    
    # Trace
    ax = axes[idx, 0]
    ax.plot(samples, alpha=0.7, linewidth=0.5)
    ax.set_ylabel('θ')
    ax.set_title(f'σ={scale:.1f}, Acceptance={acc_rate:.1%}')
    ax.grid(True, alpha=0.3)
    
    # Histogram
    ax = axes[idx, 1]
    ax.hist(samples[500:], bins=30, density=True, alpha=0.7)
    ax.set_ylabel('Density')
    ax.grid(True, alpha=0.3, axis='y')

axes[-1, 0].set_xlabel('Iteration')
axes[-1, 1].set_xlabel('θ')
plt.tight_layout()
plt.show()

print("Summary:")
print("σ=0.1: High acceptance, slow mixing (small steps)")
print("σ=0.5: Good acceptance, good mixing (Goldilocks)")
print("σ=2.0: Low acceptance, wasted computation (big jumps)")
```

**Result:**
- σ = 0.1: acceptance ≈ 95%, but trace shows tiny steps (slow exploration)
- σ = 0.5: acceptance ≈ 65%, good exploration
- σ = 2.0: acceptance ≈ 12%, many rejections

**Conclusion:** σ = 0.5 is best. Acceptance rate of 20-50% is the target for random walk proposals.

---

**4. Autocorrelation**

```python
from simulations import compute_autocorrelation

samples, _ = metropolis_hastings(log_density, 0, 0.5, 5000)
acf = compute_autocorrelation(samples[500:], max_lag=100)

fig, ax = plt.subplots(figsize=(10, 5))
ax.stem(range(len(acf)), acf, basefmt=' ')
ax.axhline(0.05, color='r', linestyle='--', label='Significance')
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Autocorrelation Function')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

# Find lag where ACF drops below 0.05
cutoff = np.where(acf < 0.05)[0]
lag_cutoff = cutoff[0] if len(cutoff) > 0 else None
print(f"ACF drops below 0.05 at lag ≈ {lag_cutoff}")
```

**Result (typical):**
```
ACF drops below 0.05 at lag ≈ 15
```

This means samples separated by 15 iterations are roughly independent. With 4500 post-burn-in samples, the effective sample size is roughly 4500 / 15 ≈ 300 independent samples.

---

## Exploration Solutions

**5. Bimodal distribution**

```python
from simulations import log_mixture_density

samples_bimodal, acc_rate = metropolis_hastings(
    log_mixture_density,
    initial_state=0,
    proposal_scale=1.0,
    n_iterations=10000
)

print(f"Acceptance rate: {acc_rate:.1%}")

# Trace plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(samples_bimodal, alpha=0.5, linewidth=0.5)
ax.axhline(-3, color='g', linestyle='--', alpha=0.5, label='Mode 1 (≈-3)')
ax.axhline(3, color='r', linestyle='--', alpha=0.5, label='Mode 2 (≈+3)')
ax.set_xlabel('Iteration')
ax.set_ylabel('θ')
ax.set_title('MCMC on Bimodal Distribution')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

# Count mode switches
mode1_mask = samples_bimodal < 0
switches = np.sum(np.diff(mode1_mask.astype(int)) != 0)
print(f"Mode switches: {switches} (out of 10000)")
```

**Observation:**
```
Acceptance rate: 71.2%
Mode switches: 3
```

The chain gets stuck! It starts in mode 2 (around +3) and rarely switches to mode 1 (around -3). This is the **multimodality problem**.

---

**6. Proposal tuning for bimodal**

```python
proposal_scales = [0.5, 1.0, 2.0, 5.0]

for scale in proposal_scales:
    samples, acc_rate = metropolis_hastings(log_mixture_density, 0, scale, 10000)
    
    mode1_mask = samples < 0
    switches = np.sum(np.diff(mode1_mask.astype(int)) != 0)
    
    print(f"Scale={scale}: Acceptance={acc_rate:.1%}, Mode switches={switches}")
```

**Result:**
```
Scale=0.5: Acceptance=92.2%, Mode switches=8
Scale=1.0: Acceptance=71.3%, Mode switches=3
Scale=2.0: Acceptance=39.4%, Mode switches=2
Scale=5.0: Acceptance=8.5%, Mode switches=1
```

Larger proposals are actually worse! Even scale=5.0 (which might reach across the gap) has low acceptance because it overshoots. Paradoxically, smaller proposals do better: they're more likely to randomly wander into the other mode.

**Key insight:** For multimodal distributions, random walk proposals are fundamentally limited. You need specialized methods (tempering, reversible jump, etc.).

---

**7. Multiple chains and R-hat**

```python
from simulations import gelman_rubin_diagnostic

# Run 4 chains from different starting points
chains = []
for initial in [0, 5, -5, 2]:
    samples, _ = metropolis_hastings(log_density, initial, 0.5, 5000)
    chains.append(samples)

# Compute R-hat
r_hat = gelman_rubin_diagnostic(chains)

print(f"R-hat: {r_hat:.4f}")
print("Interpretation:")
if r_hat < 1.05:
    print("  ✓ Chains have converged")
else:
    print("  ✗ Chains have NOT converged, need more iterations")
```

**Output:**
```
R-hat: 1.0012
✓ Chains have converged
```

All 4 chains converge to the same distribution, so R-hat ≈ 1.

---

**8. Effective sample size**

```python
from simulations import effective_sample_size, compute_autocorrelation

samples, _ = metropolis_hastings(log_density, 0, 0.5, 10000)
samples_post = samples[1000:]

n = len(samples_post)
ess = effective_sample_size(samples_post)
efficiency = ess / n

print(f"Raw sample size: {n}")
print(f"Effective sample size (ESS): {ess:.0f}")
print(f"Efficiency: {efficiency:.1%}")
```

**Output:**
```
Raw sample size: 9000
Effective sample size (ESS): 2800
Efficiency: 31.1%
```

Autocorrelation reduces effective sample size to 31% of the raw count. To get 1000 independent samples, you need roughly 3200 raw MCMC iterations.

---

## Challenge Solutions

**9. Gibbs sampling for 2D Gaussian**

```python
from simulations import gibbs_sampling_2d_gaussian, metropolis_hastings_2d
import numpy as np

# Gibbs sampling
samples_gibbs = gibbs_sampling_2d_gaussian(rho=0.9, n_iterations=5000)

# Metropolis-Hastings for comparison
def log_density_2d(x):
    # Bivariate normal with correlation 0.9
    cov = [[1, 0.9], [0.9, 1]]
    try:
        from scipy.stats import multivariate_normal
        return multivariate_normal.logpdf(x, mean=[0, 0], cov=cov)
    except:
        return -0.5 * (x**2).sum()

samples_mh, acc_rate_mh = metropolis_hastings_2d(log_density_2d, [0, 0], 1.0, 5000)

# Comparison
print("Gibbs Sampling:")
print(f"  Acceptance: 100% (always accepted)")
print(f"  Correlation: {np.corrcoef(samples_gibbs[1000:].T)[0,1]:.3f}")
from simulations import effective_sample_size
print(f"  ESS (x₁): {effective_sample_size(samples_gibbs[1000:, 0]):.0f}")

print("\nMetropolis-Hastings:")
print(f"  Acceptance: {acc_rate_mh:.1%}")
print(f"  Correlation: {np.corrcoef(samples_mh[1000:].T)[0,1]:.3f}")
print(f"  ESS (x₁): {effective_sample_size(samples_mh[1000:, 0]):.0f}")
```

**Output (typical):**
```
Gibbs Sampling:
  Acceptance: 100%
  Correlation: 0.901
  ESS (x₁): 4200

Metropolis-Hastings:
  Acceptance: 34.7%
  Correlation: 0.893
  ESS (x₁): 1800
```

**Conclusion:** Gibbs sampling is more efficient! 100% acceptance + no wasted proposals + lower autocorrelation = much higher ESS.

---

**10. Bayesian linear regression via MCMC**

```python
# Generate synthetic data
np.random.seed(42)
n = 50
x = np.linspace(0, 5, n)
y_true = 2 + 3*x + np.random.normal(0, 2, n)

# Define log posterior
def log_posterior_regression(theta):
    beta0, beta1, log_sigma = theta
    sigma = np.exp(log_sigma)
    
    # Likelihood
    mu = beta0 + beta1 * x
    log_lik = -0.5 * np.sum(((y_true - mu) / sigma)**2) - n * log_sigma
    
    # Priors
    log_prior = (
        -0.5 * (beta0**2 / 10) +  # N(0, 10)
        -0.5 * (beta1**2 / 10) +  # N(0, 10)
        log_sigma  # Exponential(1) on sigma
    )
    
    return log_lik + log_prior

# Run MCMC
samples_reg, acc_rate = metropolis_hastings(
    log_posterior_regression,
    initial_state=[0, 0, 0],
    proposal_scale=0.1,
    n_iterations=5000
)

# Post burn-in
samples_post = samples_reg[1000:]

print("Bayesian Linear Regression Results:")
print(f"β₀: {np.mean(samples_post[:, 0]):.3f} ± {np.std(samples_post[:, 0]):.3f}")
print(f"β₁: {np.mean(samples_post[:, 1]):.3f} ± {np.std(samples_post[:, 1]):.3f}")
print(f"σ: {np.exp(np.mean(samples_post[:, 2])):.3f} ± {np.std(np.exp(samples_post[:, 2])):.3f}")

print(f"\nTrue values: β₀=2, β₁=3, σ≈2")
print(f"MCMC recovered them!")
```

**Output (typical):**
```
β₀: 2.05 ± 0.48
β₁: 2.97 ± 0.12
σ: 2.01 ± 0.24

True values: β₀=2, β₁=3, σ≈2
MCMC recovered them!
```

---

## Thought Experiments

**13. Why thinning?**

If lag-1 autocorrelation is 0.9, the effective sample size is reduced by a factor of ~10 (roughly).

With 10,000 raw samples and 90% autocorrelation, ESS ≈ 1,000.

**Thinning by keeping every k-th sample:**
- k = 1: 10,000 samples, high correlation
- k = 10: 1,000 samples, much lower correlation

**Tradeoff:**
- Keep more samples (high autocorrelation): easy to compute, but samples are redundant
- Keep fewer samples (low autocorrelation): fewer samples, but more independent

With modern computing, storage is cheap. You can keep all 10,000 and account for autocorrelation in analysis. Thinning is more relevant when storage is limited.

---

**14. The multimodality nightmare**

Standard random walk MCMC gets stuck in one mode. Solutions:

1. **Better proposals**: Hamiltonian MC uses gradients, exploring more efficiently
2. **Tempering**: Sample from a "flattened" version of the posterior (lower temperature), then cool gradually
3. **Reversible jump MCMC**: allows jumping between different models
4. **Parallel tempering**: run chains at different temperatures, exchange information
5. **Reparameterization**: sometimes a change of variables makes the posterior less multimodal

For a problem with 10 isolated modes, you likely need specialized methods. Random walk proposals won't work.

---

**15. Autocorrelation and independence**

If ESS = 100 and you need 1,000 independent samples, you need 10,000 raw MCMC samples.

**Cost analysis:**
- 10,000 iterations × 1 second per iteration = 10,000 seconds (2.8 hours)
- Autocorrelation was unavoidable given the posterior structure

Sometimes reparameterization helps (reduces autocorrelation). Sometimes you just need more samples. The goal is to balance:
- Computational time
- Number of independent samples needed
- Accuracy required for inference
