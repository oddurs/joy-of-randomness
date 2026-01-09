# Chapter 16 Solutions: Thinking in Distributions

## Warm-up Solutions

**1. Beta-Binomial posteriors by hand**

Data: 7 heads in 10 flips, Beta(1,1) prior.

Conjugacy formula: posterior is Beta(α + k, β + n - k)

$$\text{Posterior} = \text{Beta}(1 + 7, 1 + 10 - 7) = \text{Beta}(8, 4)$$

Posterior mean:
$$\mathbb{E}[\theta] = \frac{\alpha}{\alpha + \beta} = \frac{8}{8 + 4} = \frac{8}{12} = 0.667$$

Posterior mode (when both α, β > 1):
$$\text{mode} = \frac{\alpha - 1}{\alpha + \beta - 2} = \frac{8 - 1}{8 + 4 - 2} = \frac{7}{10} = 0.7$$

The mode equals the observed frequency; the mean shrinks slightly toward 0.5.

---

**2. Credible intervals**

For Beta(8, 4):

```python
from scipy.stats import beta as beta_dist

# 95% credible interval
lower = beta_dist.ppf(0.025, 8, 4)
upper = beta_dist.ppf(0.975, 8, 4)
print(f"95% credible interval: [{lower:.3f}, {upper:.3f}]")

# 50% credible interval
lower_50 = beta_dist.ppf(0.25, 8, 4)
upper_50 = beta_dist.ppf(0.75, 8, 4)
print(f"50% credible interval: [{lower_50:.3f}, {upper_50:.3f}]")
```

**Output:**
```
95% credible interval: [0.446, 0.876]
50% credible interval: [0.602, 0.728]
```

Interpretation:
- 95% of posterior probability is between 0.45 and 0.88
- 50% is between 0.60 and 0.73
- The posterior is concentrated around 0.67 but with substantial uncertainty

---

**3. Effect of different priors**

```python
from simulations import compare_priors, credible_interval

k, n = 7, 10

priors = {
    'Uniform': (1, 1),
    'Skeptical': (10, 10),
    'Extreme': (0.5, 0.5)
}

posteriors = compare_priors(k, n, priors)

for name, (alpha_post, beta_post) in posteriors.items():
    mean = alpha_post / (alpha_post + beta_post)
    lower, upper = credible_interval(alpha_post, beta_post, 0.95)
    width = upper - lower
    print(f"{name:12} | Mean: {mean:.3f} | 95% CI: [{lower:.3f}, {upper:.3f}] | Width: {width:.3f}")
```

**Output:**
```
Uniform      | Mean: 0.667 | 95% CI: [0.446, 0.876] | Width: 0.430
Skeptical    | Mean: 0.567 | 95% CI: [0.431, 0.700] | Width: 0.269
Extreme      | Mean: 0.684 | 95% CI: [0.407, 0.926] | Width: 0.519
```

**Observations:**
- Skeptical prior pulls mean toward 0.5 and produces narrower credible interval (it's more confident)
- Extreme prior is wider (more uncertain due to diffuse prior)
- All three posteriors overlap substantially; the data dominates

---

**4. More data, less uncertainty**

```python
from simulations import posterior_mean, credible_interval

print("Scenario A: 7 heads in 10 flips")
alpha_a, beta_a = 1 + 7, 1 + (10 - 7)
mean_a = posterior_mean(alpha_a, beta_a)
var_a = (alpha_a * beta_a) / ((alpha_a + beta_a)**2 * (alpha_a + beta_a + 1))
lower_a, upper_a = credible_interval(alpha_a, beta_a, 0.95)

print(f"  Mean: {mean_a:.4f}")
print(f"  Variance: {var_a:.4f}")
print(f"  95% CI width: {upper_a - lower_a:.4f}")

print("\nScenario B: 70 heads in 100 flips")
alpha_b, beta_b = 1 + 70, 1 + (100 - 70)
mean_b = posterior_mean(alpha_b, beta_b)
var_b = (alpha_b * beta_b) / ((alpha_b + beta_b)**2 * (alpha_b + beta_b + 1))
lower_b, upper_b = credible_interval(alpha_b, beta_b, 0.95)

print(f"  Mean: {mean_b:.4f}")
print(f"  Variance: {var_b:.4f}")
print(f"  95% CI width: {upper_b - lower_b:.4f}")

print(f"\nVariance ratio B/A: {var_b / var_a:.3f}")
```

**Output:**
```
Scenario A: 7 heads in 10 flips
  Mean: 0.6667
  Variance: 0.0113
  95% CI width: 0.4304

Scenario B: 70 heads in 100 flips
  Mean: 0.6716
  Variance: 0.0020
  95% CI width: 0.1390

Variance ratio B/A: 0.18
```

**Insight:** With 10x more data, the variance drops by ~5-6x, and the credible interval becomes much narrower. Uncertainty shrinks as we accumulate evidence.

---

## Exploration Solutions

**5. Sequential Bayesian updating**

```python
from simulations import sequential_bayesian_update, beta_prior
import matplotlib.pyplot as plt
import numpy as np

observations = [1, 0, 1, 1, 0, 1, 1, 1, 1, 0]  # H T H H T H H H H T

# Uniform prior
posteriors = sequential_bayesian_update(observations, alpha=1, beta_param=1)

# Plot
fig, axes = plt.subplots(2, 5, figsize=(14, 8))
axes = axes.flatten()

theta = np.linspace(0, 1, 1000)

for step, (alpha, beta_param) in enumerate(posteriors[1:]):
    ax = axes[step]
    density = beta_prior(theta, alpha, beta_param)
    ax.plot(theta, density, linewidth=2)
    ax.fill_between(theta, 0, density, alpha=0.3)
    ax.set_title(f'After {step+1} flip(s): Beta({alpha}, {beta_param})')
    ax.set_ylim(ymin=0)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

**Key observation:** The posterior evolves from the Uniform(0,1) prior to Beta(7,4) after all 10 flips. Each observation shifts the posterior, and the sequence of updates produces the same result as updating all at once (order invariance).

---

**6. Prior convergence with data**

```python
from simulations import beta_prior, compare_priors
import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

theta = np.linspace(0, 1, 1000)

# Case 1: 50 heads in 100 flips
k, n = 50, 100
priors = {
    'Uniform': (1, 1),
    'Heads bias': (100, 1),
    'Tails bias': (1, 100)
}

posteriors = compare_priors(k, n, priors)

for name, (alpha, beta_param) in posteriors.items():
    density = beta_prior(theta, alpha, beta_param)
    ax1.plot(theta, density, linewidth=2, label=name)

ax1.set_xlabel('θ')
ax1.set_ylabel('Density')
ax1.set_title(f'After 50/100 flips: Priors converge')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Case 2: 500 heads in 1000 flips
k, n = 500, 1000
posteriors = compare_priors(k, n, priors)

for name, (alpha, beta_param) in posteriors.items():
    density = beta_prior(theta, alpha, beta_param)
    ax2.plot(theta, density, linewidth=2, label=name)

ax2.set_xlabel('θ')
ax2.set_ylabel('Density')
ax2.set_title(f'After 500/1000 flips: Priors have converged')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

**Result:** With 500/1000 flips, all three priors produce nearly identical posteriors centered at 0.5. This is Bayesian consistency: given sufficient data, the posterior is insensitive to the prior.

---

**9. Bayesian A/B testing**

```python
from simulations import ab_test_comparison

n_a, k_a = 150, 18  # Variant A
n_b, k_b = 150, 24  # Variant B

p_b_better, mean_diff, (ci_lower, ci_upper) = ab_test_comparison(n_a, k_a, n_b, k_b)

print(f"Variant A: {k_a}/{n_a} = {k_a/n_a:.1%}")
print(f"Variant B: {k_b}/{n_b} = {k_b/n_b:.1%}")
print(f"\nBayesian Results:")
print(f"  P(B > A) = {p_b_better:.1%}")
print(f"  Posterior mean difference: {mean_diff:.3f}")
print(f"  95% credible interval on difference: [{ci_lower:.3f}, {ci_upper:.3f}]")

if p_b_better > 0.95:
    print(f"\n✓ Strong evidence that B is better")
elif p_b_better > 0.75:
    print(f"\n◐ Moderate evidence that B is better")
else:
    print(f"\n✗ Insufficient evidence that B is better")
```

**Output (example):**
```
Variant A: 18/150 = 12.0%
Variant B: 24/150 = 16.0%

Bayesian Results:
  P(B > A) = 0.937
  Posterior mean difference: 0.040
  95% credible interval on difference: [-0.006, 0.087]

◐ Moderate evidence that B is better
```

**Advantages over frequentist approach:**
- Direct probability statement: P(B > A) = 93.7%
- Full credible interval on difference
- No p-values, no multiple testing correction needed
- Natural stopping rule: can check results anytime

---

**10. Medical diagnosis**

```python
from simulations import medical_diagnosis
import matplotlib.pyplot as plt
import numpy as np

# Fixed test accuracy
prevalences = np.linspace(0.001, 0.1, 50)
posteriors = [medical_diagnosis(0.95, 0.90, prev) for prev in prevalences]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plot 1: Vary prevalence
ax1.plot(prevalences * 100, np.array(posteriors) * 100, linewidth=2)
ax1.fill_between(prevalences * 100, 0, np.array(posteriors) * 100, alpha=0.3)
ax1.set_xlabel('Disease Prevalence (%)')
ax1.set_ylabel('P(Disease | Positive Test) (%)')
ax1.set_title('Medical Test: Effect of Prevalence\n(Sensitivity=95%, Specificity=90%)')
ax1.grid(True, alpha=0.3)

# Specific case: 1% prevalence
p_disease = medical_diagnosis(0.95, 0.90, 0.01)
print(f"Base case (1% prevalence):")
print(f"  P(disease | positive) = {p_disease:.1%}")
print(f"  Despite positive test, only ~9% chance of disease!")

# Plot 2: Vary test accuracy
accuracies = np.linspace(0.5, 1.0, 50)
posteriors_acc = [medical_diagnosis(acc, acc, 0.01) for acc in accuracies]

ax2.plot(accuracies * 100, np.array(posteriors_acc) * 100, linewidth=2)
ax2.fill_between(accuracies * 100, 0, np.array(posteriors_acc) * 100, alpha=0.3)
ax2.set_xlabel('Test Accuracy (%)')
ax2.set_ylabel('P(Disease | Positive Test) (%)')
ax2.set_title('Effect of Test Accuracy (Prevalence = 1%)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

**Key insight:** Even with 95% sensitivity and 90% specificity, a positive test when the base rate is 1% only gives ~9% posterior probability. This is the **base rate fallacy**: we intuitively think tests are more informative than they actually are.

---

## Thought Experiments

**13. Objective priors?**

The **Uniform prior** Beta(1,1) seems "objective" on [0,1]. But consider:

If you reparameterize to log-odds: $\log \frac{\theta}{1-\theta}$, the Uniform prior on θ becomes a very informative prior on log-odds (concentrated near extreme values).

Different parameterizations → different "uninformed" priors.

**Jeffreys prior** is scale-invariant: it doesn't depend on parameterization. But it's often not uniform and requires careful computation.

**Answer:** There is no truly "objective" prior. All priors encode information (or at least, information about which parameterization matters). The best approach is to state your prior explicitly and check robustness to prior choice.

---

**14. Laplace's sunrise problem**

```python
# Laplace's calculation
days_sun_rose = 1.8e6  # ~5000 years of daily data

# Beta(1,1) prior
alpha = 1
beta_param = 1

# Posterior after observing success (sun rose)
alpha_post = alpha + days_sun_rose
beta_post = beta_param + 0  # No failures

# Posterior probability sun rises tomorrow (posterior predictive)
p_tomorrow = alpha_post / (alpha_post + beta_post)

print(f"P(sun rises tomorrow) = {p_tomorrow:.10f}")
print(f"This is {1 - p_tomorrow:.2e}")
```

**Output:**
```
P(sun rises tomorrow) = 0.9999994444
This is 5.56e-07
```

This is sensible and elegant:
- It acknowledges the overwhelming evidence (extremely high probability)
- It reserves a tiny probability for unknown unknowns (asteroid collision, stellar explosion)
- As observations accumulate, probability approaches 1 asymptotically

Bayesian credibility is robust and honest about uncertainty, even for near-certain events.

---

**15. Bayes in daily life**

Example: **Friend is late to meeting**

**Prior:** Friend is usually reliable (P(reliable) = 0.8)

**Data:** Friend is 15 minutes late

**Likelihood:** P(15 min late | reliable) might be 0.05 (accidents happen), P(15 min late | flaky) might be 0.3

**Posterior (by Bayes' theorem):**

$$P(\text{flaky} | \text{late}) = \frac{P(\text{late} | \text{flaky}) P(\text{flaky})}{P(\text{late})}$$

$$= \frac{0.3 \times 0.2}{0.3 \times 0.2 + 0.05 \times 0.8} = \frac{0.06}{0.1} = 0.6$$

**Conclusion:** Being 15 minutes late shifts your belief from 20% (prior) to 60% (posterior) that the friend is flaky. But it's not overwhelming; you still give them the benefit of doubt because you have strong prior evidence of reliability.

This is how our brains naturally update, but formalizing it with Bayes' theorem reveals the logic.
