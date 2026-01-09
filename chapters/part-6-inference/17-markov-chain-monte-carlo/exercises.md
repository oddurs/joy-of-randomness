# Chapter 17 Exercises: Markov Chain Monte Carlo

## Warm-up Exercises

**1. Implement Metropolis-Hastings**

Implement your own Metropolis-Hastings sampler from scratch. Target distribution: standard normal N(0,1).

Test with proposal scale σ = 0.5. Run 5000 iterations.

Verify:
- Mean of samples (post burn-in) ≈ 0
- Std dev ≈ 1
- Acceptance rate is reasonable (10-50%)

---

**2. Diagnose convergence with trace plots**

Run your MCMC sampler from Exercise 1, but start from an extreme initial state (e.g., θ₀ = 10).

Plot the trace:
- x-axis: iteration
- y-axis: θ value

When does the chain "settle down"? How long is the burn-in period?

Compare starting points: θ₀ = 0 vs. θ₀ = 10 vs. θ₀ = -20. Do they all converge?

---

**3. Effect of proposal scale**

Target: N(0, 1). Run Metropolis-Hastings with different proposal scales:
- σ = 0.1 (too narrow)
- σ = 0.5 (good)
- σ = 2.0 (too wide)

For each:
- Record acceptance rate
- Plot trace and posterior histogram
- Count how many distinct values you see

Which proposal scale produces the best samples? Why?

---

**4. Autocorrelation**

Run MCMC on N(0,1) with σ = 0.5. Compute autocorrelation:

$$\text{ACF}(\text{lag}) = \text{corr}(θ_t, θ_{t+\text{lag}})$$

Plot autocorrelation as a function of lag. At what lag does it drop below 0.05?

---

## Exploration Exercises

**5. Bimodal distribution**

Target: mixture of two normals: 0.5 × N(-3, 1) + 0.5 × N(3, 1).

Use Metropolis-Hastings with σ = 1.0. Run 10,000 iterations.

Questions:
- Does the chain visit both modes?
- How often does it switch between modes?
- Plot: are there gaps in the trace where the chain jumps from -3 to +3?

This demonstrates the **multimodality problem**: the chain struggles to jump between isolated peaks.

---

**6. Proposal tuning**

For the bimodal distribution, try different proposal scales. Which one allows the chain to switch between modes most frequently?

Compute: time between mode switches (chain is in mode 1, then switches to mode 2, then back).

Insight: smaller proposals are more likely to explore locally, while larger proposals might jump between modes.

---

**7. Multiple chains and R-hat**

Run 4 independent MCMC chains on N(0,1), each starting from different initial states:
- Chain 1: θ₀ = 0
- Chain 2: θ₀ = 5
- Chain 3: θ₀ = -5
- Chain 4: θ₀ = 2

Compute the Gelman-Rubin diagnostic (R-hat). This compares within-chain variance to between-chain variance.

If R-hat ≈ 1.0, the chains have converged to the same distribution. If R-hat > 1.05, keep running.

---

**8. Effective sample size**

Run 10,000 iterations of MCMC (any target). Compute ESS (Effective Sample Size) accounting for autocorrelation.

Compare:
- Raw sample size: 10,000
- ESS: fewer, due to correlation

Ratio: ESS / N tells you the "efficiency" of your sampling.

If ESS is much smaller than N, you have high autocorrelation and should either thin or improve the proposal.

---

## Challenge Exercises

**9. Gibbs sampling for 2D Gaussian**

Implement Gibbs sampling for a 2D bivariate normal with correlation ρ = 0.9.

Conditional distributions:
- x | y ~ N(ρy, 1 - ρ²)
- y | x ~ N(ρx, 1 - ρ²)

Compare to Metropolis-Hastings on the same target:
- Acceptance rate
- Autocorrelation
- Effective sample size

Which is more efficient?

---

**10. Bayesian linear regression via MCMC**

Fit a simple linear regression using MCMC.

Model:
- y_i = β₀ + β₁ x_i + ε_i where ε_i ~ N(0, σ²)
- Priors: β₀, β₁ ~ N(0, 10) and σ ~ Exponential(1)

Generate synthetic data: y = 2 + 3x + noise.

Use MCMC (Metropolis-Hastings or Gibbs) to sample from the posterior of (β₀, β₁, σ).

Report:
- Posterior means and credible intervals for β₀, β₁
- Compare to OLS estimates
- Plot trace plots for diagnostics

---

**11. Mixture model inference**

Generate data from a mixture of two normals:
- Half the points from N(-2, 1)
- Half from N(2, 1)

But you don't know the mixing proportions, means, or variances. Use MCMC to infer them.

Model:
- z_i ∈ {1, 2} (unknown group assignment)
- Each group has mean μ_j and variance σ_j²
- P(z_i = 1) = p (mixing proportion)

Unknowns: (p, μ₁, μ₂, σ₁, σ₂, z_1, ..., z_n)

Run MCMC (alternating between group assignments and parameters).

Result: posterior over cluster structure and parameters.

---

**12. Rosenbrock function challenge**

The Rosenbrock function is notoriously difficult:

$$f(x,y) = (1-x)^2 + 100(y-x^2)^2$$

Use MCMC to sample from exp(-f/T) (a density concentrated at the minimum).

Use Metropolis-Hastings with various proposal scales. Does it find the minimum at (1,1)?

Try:
- Standard random walk proposal
- Adaptive proposal (adjust scale based on acceptance rate)
- Hamiltonian-inspired proposal (if you're ambitious)

This is a classic test case for MCMC algorithms.

---

## Thought Experiments

**13. Why thinning?**

MCMC samples are correlated. If lag-1 autocorrelation is 0.9, consecutive samples are very similar.

Thinning: keep every k-th sample.

Questions:
- If you have 10,000 highly correlated samples, how much do you need to thin?
- What's the tradeoff between computational cost and independence?
- When is thinning helpful? When is it wasteful?

---

**14. The multimodality nightmare**

Suppose your posterior has 10 distinct modes (peaks) separated by low-density valleys.

Standard MCMC with random walk proposals will:
- Get stuck in one mode
- Rarely jump to another
- Provide biased estimates (overweighting whichever mode the chain explores)

How would you address this? Consider:
- Better proposals (what would help?)
- Reparameterization
- Tempering or annealing
- Running independent chains for each mode

---

**15. Autocorrelation and independence**

MCMC samples are correlated. But correlation isn't always bad.

Questions:
- If you need 1,000 independent samples and your ESS is 100, how many raw samples do you need?
- What's the cost of autocorrelation: computational time vs. number of samples?
- When is autocorrelation unavoidable?

Example: for a process with ACF that decays exponentially with time scale τ, what's the autocorrelation time?

---

## Open-Ended Exploration

**Hamiltonian Monte Carlo (Advanced)**

Standard Metropolis-Hastings uses random walk proposals. HMC uses *gradient* information.

Imagine the posterior as a landscape. HMC simulates a particle rolling down the landscape (following the gradient), then jumps to a point along its trajectory.

Implement a simplified HMC (or study an existing implementation):
- Compute gradients of the log-posterior
- Simulate particle motion (leapfrog integrator)
- Accept/reject based on energy conservation

Compare HMC to Metropolis-Hastings on a high-dimensional posterior. HMC should be more efficient (fewer rejections, better exploration).

---

**Adaptive MCMC**

Standard Metropolis-Hastings requires tuning the proposal scale σ.

Adaptive MCMC tunes σ online:
- If acceptance rate is too high, increase σ
- If too low, decrease σ
- Aim for acceptance rate ≈ 0.234 (optimal for random walk in high dimensions)

Implement adaptive MCMC and test on different targets. Does it automatically find good proposal scales?

---

**Convergence diagnostics beyond R-hat**

Besides R-hat, there are other convergence diagnostics:
- **Trace plot visual inspection**: does the chain look stationary?
- **Effective sample size**: is ESS sufficient relative to runtime?
- **Spectral density at zero**: another measure of autocorrelation
- **Geweke test**: compare early vs. late samples (should be similar if converged)

Implement one or more of these. Apply them to chains you know have converged and chains that haven't. Can you reliably detect convergence?

---

**Custom MCMC for your problem**

Choose a problem you care about (scientific, business, personal):
- Specify a generative model
- Write the likelihood and priors
- Implement MCMC (or use Stan/PyMC)
- Infer the posterior

Document the workflow:
1. Prior predictive simulation: does your prior make sense?
2. MCMC sampling: convergence diagnostics
3. Posterior analysis: what did you learn?
4. Posterior predictive check: do simulations from the posterior match the data?
