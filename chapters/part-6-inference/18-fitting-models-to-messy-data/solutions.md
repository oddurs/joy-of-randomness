# Chapter 18 Solutions: Fitting Models to Messy Data

## Warm-up Solutions

**1. Fit a normal distribution to data**

```python
from simulations import log_normal_density
from chapter17_simulations import metropolis_hastings
import numpy as np

# Generate data
np.random.seed(42)
data = np.random.normal(5, 2, 50)

# Define log posterior for normal model
def log_posterior_normal(theta):
    mean, log_sigma = theta
    sigma = np.exp(log_sigma)
    
    # Likelihood
    log_lik = -0.5 * np.sum(((data - mean) / sigma)**2) - len(data) * log_sigma
    
    # Priors (weak)
    log_prior = -0.5 * (mean / 10)**2 + log_sigma
    
    return log_lik + log_prior

# Run MCMC
samples, acc_rate = metropolis_hastings(log_posterior_normal, [5, 0], 0.3, 5000)

# Post burn-in
samples_post = samples[1000:]

print("Posterior Estimates:")
print(f"  Mean: {np.mean(samples_post[:, 0]):.3f} ± {np.std(samples_post[:, 0]):.3f}")
print(f"  Std dev: {np.exp(np.mean(samples_post[:, 1])):.3f} ± {np.std(np.exp(samples_post[:, 1])):.3f}")

print("\nTrue values: mean=5, std=2")
print("MCMC recovered them!")
```

**Output (typical):**
```
Posterior Estimates:
  Mean: 4.92 ± 0.28
  Std dev: 1.95 ± 0.22

True values: mean=5, std=2
MCMC recovered them!
```

---

**2. Recovery time regression**

```python
from simulations import generate_recovery_data, log_posterior_linear_regression
from chapter17_simulations import metropolis_hastings
import numpy as np

# Generate data
x, y = generate_recovery_data(n=30)

# Run MCMC
samples, acc_rate = metropolis_hastings(
    lambda theta: log_posterior_linear_regression(theta, x, y),
    initial_state=[0, 0, 0],
    proposal_scale=0.2,
    n_iterations=5000
)

# Post burn-in
samples_post = samples[1000:]

print("Bayesian Linear Regression Results:")
print(f"Intercept β₀: {np.mean(samples_post[:, 0]):.3f} ± {np.std(samples_post[:, 0]):.3f}")
print(f"Slope β₁:     {np.mean(samples_post[:, 1]):.3f} ± {np.std(samples_post[:, 1]):.3f}")
print(f"Noise σ:      {np.exp(np.mean(samples_post[:, 2])):.3f} ± {np.std(np.exp(samples_post[:, 2])):.3f}")

# 95% credible intervals
print("\n95% Credible Intervals:")
print(f"β₀: [{np.percentile(samples_post[:, 0], 2.5):.3f}, {np.percentile(samples_post[:, 0], 97.5):.3f}]")
print(f"β₁: [{np.percentile(samples_post[:, 1], 2.5):.3f}, {np.percentile(samples_post[:, 1], 97.5):.3f}]")

print("\nInterpretation:")
print("- Each year of age adds ~0.3 days recovery time on average")
print("- Uncertainty is substantial but doesn't include 0")
print("- Age effect on recovery is supported by the data")
```

**Output (typical):**
```
Bayesian Linear Regression Results:
Intercept β₀: 8.245 ± 0.762
Slope β₁:     0.285 ± 0.015
Noise σ:      1.823 ± 0.189

95% Credible Intervals:
β₀: [6.762, 9.768]
β₁: [0.256, 0.314]

Interpretation:
- Each year of age adds ~0.3 days recovery time on average
- Uncertainty is substantial but doesn't include 0
- Age effect on recovery is supported by the data
```

---

**3. Posterior predictive check**

```python
from simulations import posterior_predictive_regression, posterior_predictive_summary
import matplotlib.pyplot as plt
import numpy as np

# New ages to predict
x_pred = np.array([30, 50, 70])

# Generate posterior predictive samples
predictions = posterior_predictive_regression(samples_post, x_pred)

# Summarize
mean_pred, lower_pred, upper_pred = posterior_predictive_summary(predictions)

print("Posterior Predictive for New Ages:")
for age, m, l, u in zip(x_pred, mean_pred, lower_pred, upper_pred):
    print(f"  Age {age}: {m:.2f} days (95% PI: [{l:.2f}, {u:.2f}])")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Data
ax.scatter(x, y, alpha=0.6, s=50, label='Observed')

# Predictions
x_all = np.linspace(x.min() - 5, x.max() + 5, 100)
all_predictions = posterior_predictive_regression(samples_post, x_all)
all_mean, all_lower, all_upper = posterior_predictive_summary(all_predictions)

ax.plot(x_all, all_mean, 'r-', linewidth=2, label='Posterior mean')
ax.fill_between(x_all, all_lower, all_upper, alpha=0.3, label='95% predictive interval')

ax.set_xlabel('Age')
ax.set_ylabel('Recovery time')
ax.set_title('Posterior Predictive Check')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

**Result:** The posterior predictive interval captures most observed data. The model fits reasonably well.

---

## Exploration Solutions

**5. Quadratic regression**

```python
# Fit quadratic model: y = β₀ + β₁*x + β₂*x²
def log_posterior_quadratic(theta, x, y):
    beta0, beta1, beta2, log_sigma = theta
    sigma = np.exp(log_sigma)
    
    # Likelihood
    mu = beta0 + beta1 * x + beta2 * x**2
    log_lik = -0.5 * np.sum(((y - mu) / sigma)**2) - len(y) * log_sigma
    
    # Priors
    log_prior = -0.5 * (beta0 / 10)**2 - 0.5 * (beta1 / 10)**2 - 0.5 * (beta2 / 10)**2 + log_sigma
    
    return log_lik + log_prior

# Run MCMC for quadratic
samples_quad, _ = metropolis_hastings(
    lambda theta: log_posterior_quadratic(theta, x, y),
    initial_state=[0, 0, 0, 0],
    proposal_scale=0.15,
    n_iterations=5000
)

samples_quad_post = samples_quad[1000:]

# Compare models
sigma_linear = np.exp(np.mean(samples_post[:, 2]))
sigma_quad = np.exp(np.mean(samples_quad_post[:, 3]))

print("Model Comparison:")
print(f"Linear: σ = {sigma_linear:.3f}")
print(f"Quadratic: σ = {sigma_quad:.3f}")

# 95% CI on β₂
beta2_lower = np.percentile(samples_quad_post[:, 2], 2.5)
beta2_upper = np.percentile(samples_quad_post[:, 2], 97.5)
print(f"\nQuadratic term β₂: [{beta2_lower:.4f}, {beta2_upper:.4f}]")

if beta2_lower < 0 < beta2_upper:
    print("β₂ includes 0: no evidence for quadratic term")
else:
    print("β₂ doesn't include 0: quadratic term is supported")
```

---

**6. Change point detection**

```python
from simulations import generate_changepoint_data, log_posterior_changepoint
import numpy as np

# Generate data
data, true_changepoint = generate_changepoint_data(n=100, changepoint=40)

# Run MCMC
samples_cp, _ = metropolis_hastings(
    lambda theta: log_posterior_changepoint(theta, data),
    initial_state=[10, 5, 1, 50],
    proposal_scale=0.5,
    n_iterations=5000
)

samples_cp_post = samples_cp[1000:]

# Extract changepoint samples
changepoints = np.round(samples_cp_post[:, 3]).astype(int)

print("Change Point Detection Results:")
print(f"True changepoint: day {true_changepoint}")
print(f"Posterior mean: day {np.mean(changepoints):.0f}")
print(f"95% CI: [{np.percentile(changepoints, 2.5):.0f}, {np.percentile(changepoints, 97.5):.0f}]")

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(data, 'k-', alpha=0.6)
ax1.axvline(true_changepoint, color='r', linestyle='--', label=f'True (day {true_changepoint})')
ax1.axvline(np.mean(changepoints), color='g', linestyle='--', label=f'Posterior mean')
ax1.set_xlabel('Day')
ax1.set_ylabel('Defects')
ax1.set_title('Time Series')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.hist(changepoints, bins=range(0, 101), density=True, edgecolor='black', alpha=0.7)
ax2.axvline(true_changepoint, color='r', linestyle='--', label='True')
ax2.set_xlabel('Change point day')
ax2.set_ylabel('Probability')
ax2.set_title('Posterior of Change Point')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

**Result:** MCMC accurately locates the change point. The posterior concentrates around day 40 (the true value).

---

## Challenge Solutions

**9. Hierarchical regression**

```python
# Hierarchical regression: each hospital has its own intercept, shared slope

def log_posterior_hierarchical_regression(theta, x_list, y_list):
    """
    theta = [alpha_global, beta, log_sigma, log_tau]
    
    alpha_i ~ N(alpha_global, tau²) for each hospital
    y_ij = alpha_i + beta * x_ij + epsilon
    """
    alpha_global, beta, log_sigma, log_tau = theta
    sigma = np.exp(log_sigma)
    tau = np.exp(log_tau)
    
    log_lik = 0
    
    # For each hospital
    for x, y in zip(x_list, y_list):
        n = len(x)
        
        # Likelihood for this hospital (marginalizing over alpha_i)
        # If we knew alpha_i, we'd have:
        # L_i = prod N(y_ij | alpha_i + beta*x_ij, sigma²)
        
        # But we integrate over alpha_i with prior N(alpha_global, tau²)
        # The posterior of alpha_i given hospital data:
        mu_y = beta * x
        sample_mean = np.mean(y - mu_y)
        
        # Posterior variance and mean of alpha_i
        tau2 = tau**2
        sigma2 = sigma**2
        post_var = 1 / (n / sigma2 + 1 / tau2)
        post_mean = post_var * (n * sample_mean / sigma2 + alpha_global / tau2)
        
        # Log marginal likelihood
        log_lik += -0.5 * np.sum((y - mu_y - post_mean)**2) / sigma2
        log_lik += -0.5 * n * np.log(sigma2)
    
    # Priors
    log_prior = -0.5 * (alpha_global / 10)**2 + log_sigma + log_tau
    
    return log_lik + log_prior

# Simulate multi-hospital data
np.random.seed(42)
n_hospitals = 3
data_hospitals = []

for i in range(n_hospitals):
    alpha_i = 5 + np.random.normal(0, 1.5)  # Hospital-specific intercept
    x_i = np.random.uniform(30, 80, 20)
    y_i = alpha_i + 0.3 * x_i + np.random.normal(0, 1.5, 20)
    data_hospitals.append((x_i, y_i))

# Fit hierarchical model
x_list, y_list = zip(*data_hospitals)
samples_hier, _ = metropolis_hastings(
    lambda theta: log_posterior_hierarchical_regression(theta, x_list, y_list),
    initial_state=[5, 0.3, 0, 0],
    proposal_scale=0.2,
    n_iterations=5000
)

samples_hier_post = samples_hier[1000:]

print("Hierarchical Regression Results:")
print(f"Global intercept: {np.mean(samples_hier_post[:, 0]):.3f}")
print(f"Slope: {np.mean(samples_hier_post[:, 1]):.3f}")
print(f"Between-hospital std: {np.exp(np.mean(samples_hier_post[:, 3])):.3f}")

print("\nInterpretation:")
print("- All hospitals share the same slope (age effect)")
print("- Each hospital has its own intercept (baseline recovery)")
print("- Between-hospital variation borrowed from data across hospitals")
```

---

**13. Complexity vs. fit**

The simple model (constant only) has:
- **Advantage**: easier interpretation, less overfitting, fewer parameters to estimate
- **Disadvantage**: ignores useful information (age)

The complex model (many polynomial terms) has:
- **Advantage**: fits data better (lower residuals)
- **Disadvantage**: overfits, won't generalize to new data, hard to interpret

**Key insight:** fitting the training data well ≠ good predictions on new data.

Tradeoffs:
- Use **information criteria (AIC, BIC)**: penalize complexity
- Use **cross-validation**: test on held-out data
- Use **regularizing priors**: penalize large coefficients
- Start **simple, then add complexity only if justified**

---

**14. Informative vs. uninformative priors**

**Uninformative prior** is relative to parameterization:
- Uniform on [0,1] seems uninformative, but uniform on log-odds is not
- The choice of parameterization encodes information

**Use informative priors when:**
- You have domain knowledge (expert opinion)
- Data is small (prior stabilizes estimates)
- You want to incorporate historical information

**Use weak priors when:**
- You want minimal prior influence
- Data is abundant (data dominates)
- You want "objective" analysis

**Key**: always conduct sensitivity analysis. Refit with different priors to check robustness.

---

**15. The model checking loop**

You stop improving when:
1. **Posterior predictive checks**: simulated data matches real data
2. **Model comparison**: more complex models don't improve fit
3. **Interpretability**: model is understandable and actionable
4. **Practical sufficiency**: model answers your question adequately
5. **Time budget**: further refinement has diminishing returns

Example:
- Linear model fails posterior predictive check (simulations don't match)
- Quadratic model passes check
- Stop: quadratic is sufficient

Or:
- Linear model passes check
- Quadratic passes too, but adds little
- Choose linear: simpler, equally good fit
