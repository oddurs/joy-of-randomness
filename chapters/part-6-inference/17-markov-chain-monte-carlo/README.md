# Chapter 17: Markov Chain Monte Carlo

## Metadata

```yaml
Part: 6 - Inference
Topics: MCMC, Metropolis-Hastings, Gibbs sampling, posterior approximation, intractable models
Key Concepts: Stationary distributions, burn-in, convergence diagnostics, sampling posteriors
```

---

## The Intractable Posterior Problem

You have a Bayesian posterior you can't compute directly. Maybe it's a logistic regression with hundreds of features. Maybe it's a hierarchical model with thousands of parameters. You can evaluate the posterior *density* (up to a constant):

$$P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \times P(\theta)$$

But you can't:
- Integrate it (to compute the normalizing constant)
- Invert it (to transform random samples)
- Sample from it directly

What do you do? You build a Markov chain whose stationary distribution is your posterior. Then you run it. The samples you collect approximate the posterior.

This is **Markov Chain Monte Carlo (MCMC)**: a synthesis of Markov chains (from Chapter 8) and Monte Carlo simulation (from Chapter 10).

---

## First Contact: The Metropolis-Hastings Algorithm

The simplest MCMC algorithm is **Metropolis-Hastings**. Here's the idea:

1. Start at some initial state θ₀
2. Propose a new state θ' from a **proposal distribution** (e.g., normal random walk)
3. Accept the proposal with probability:
   $$\alpha = \min\left(1, \frac{\pi(θ') \, q(θ \mid θ')}{\pi(θ) \, q(θ' \mid θ)}\right)$$
4. If accept: move to θ'. If reject: stay at θ.
5. Repeat steps 2-4 many times

The remarkable fact: **the distribution of visited states converges to the posterior π(θ | data).**

### Why This Works

The key insight is **detailed balance**:

$$\pi(θ) P(θ → θ') = \pi(θ') P(θ' → θ)$$

This condition ensures the chain has π as its stationary distribution. Metropolis-Hastings satisfies detailed balance by construction.

### Visualizing the Chain

Imagine a target distribution (e.g., a mixture of two normals). Run Metropolis-Hastings:

- Early on, the chain bounces around, exploring the space
- It visits high-density regions more often than low-density regions (because rejection keeps it in high-density)
- A histogram of visited states matches the target distribution
- But the samples are **correlated**: consecutive states are similar

![Figure 17.1: Metropolis-Hastings convergence to target distribution. Left: trace plot during burn-in (red shading) shows initial wandering. Center-left: full chain trace shows settling behavior. Center-right: histogram of post-burn-in samples closely matches the target mixture distribution. Right: autocorrelation decays as lag increases, indicating dependent but mixing samples.](src/figures/17.1.png)

---

## Patterns Emerge

### The Chain Wanders in High-Density Regions

The acceptance probability favors high-density regions but doesn't exclude low-density ones. The chain explores the entire distribution, but spends more time where π is large.

This is the magic: without explicitly computing π, the chain naturally weights regions proportionally to their probability.

### The Proposal Distribution Matters

**Too narrow** (σ_proposal too small):
- High acceptance rate (easy to find similar states with high density)
- But slow exploration (tiny steps, takes forever to cover the space)
- High autocorrelation between samples

**Too wide** (σ_proposal too large):
- Low acceptance rate (proposals land in low-density regions)
- Fewer distinct samples collected
- Wasted computation

**Just right** (Goldilocks zone):
- Acceptance rate around 20-50%
- Good mixing (chain explores efficiently)
- Lower autocorrelation

![Figure 17.2: Proposal distribution tuning effects. Top-left: narrow proposal (SD=0.3) has high acceptance but explores slowly, capturing only one mode. Top-right: Goldilocks proposal (SD=1.0) with ~30% acceptance efficiently samples both modes. Bottom-left: wide proposal (SD=2.5) has low acceptance (~10%) and sparse samples. Bottom-right: very wide proposal (SD=5.0) is inefficient with poor exploration.](src/figures/17.2.png)

### Multimodality: The Chain Gets Stuck

If the posterior has multiple modes (peaks), Metropolis-Hastings struggles. The chain gets stuck in one mode, rarely jumping to another.

Example: mixture of two gaussians separated by a low-density valley. A local proposal can't jump across. The chain explores one mode thoroughly but misses the other.

This is a **fundamental challenge** in MCMC: multimodal posteriors are hard.

![Figure 17.4: Multimodality challenge illustrated with a bimodal target (two equal-weight Gaussian modes separated by a valley). Left: narrow proposal (SD=0.5) starting at mode 1 never jumps to mode 2—histogram shows only mode 1 captured. Right: wide proposal (SD=3) can jump between modes and captures both, though with lower acceptance rates. This demonstrates the "local trap" problem: proposals must be wide enough to escape local modes.](src/figures/17.4.png)

---

## The Theory

### Detailed Balance and Stationarity

A Markov chain has stationary distribution π if:

$$\pi(θ) P(θ → θ') = \pi(θ') P(θ' → θ)$$

for all θ, θ'.

This is **detailed balance**: the probability flow from θ to θ' equals the flow back. If a chain satisfies detailed balance with respect to π, then π is its stationary distribution.

Metropolis-Hastings constructs a chain that satisfies detailed balance with respect to the target posterior.

### Metropolis-Hastings Acceptance Probability

Given a proposal distribution q(θ' | θ), the acceptance probability is:

$$\alpha(θ \to θ') = \min\left(1, \frac{\pi(θ') q(θ \mid θ')}{\pi(θ) q(θ' \mid θ)}\right)$$

The numerator is the "posterior odds × proposal ratio" in favor of θ'. If this exceeds the current state, we always accept. Otherwise, we accept with probability α.

### Burn-in: Discarding the Early Samples

The chain starts from an arbitrary initial state and takes time to reach stationarity. Early samples reflect the initial condition more than the posterior.

Solution: **burn-in**. Run the chain for some number of iterations (e.g., 1000) without recording samples. Then start collecting.

How long to burn in? Varies. Diagnose with trace plots: look for the first time the chain "settles down" and stops drifting.

![Figure 17.3: Convergence diagnostics for multiple chains. Top-left: four independent chains started from different initial states (−4, 0, 3, 5) all converge to the same distribution. Top-right: R-hat diagnostic drops below 1.1, indicating convergence. Bottom-left: post-burn-in posterior histograms from all chains overlay perfectly. Bottom-right: effective sample size after accounting for autocorrelation is ~60% of raw samples across all chains.](src/figures/17.3.png)

### Thinning: Reducing Autocorrelation

MCMC samples are correlated: θ_t and θ_{t+1} are usually similar.

Solution: **thinning**. Keep every k-th sample, discard the rest.

If the effective sample size is only 10% of the raw samples (due to correlation), keeping every 10th sample gives you independent-like samples.

---

## Going Deeper

### Gibbs Sampling

When the full posterior is intractable but **conditional distributions** are easy, use **Gibbs sampling**:

For a 2D problem with parameters (θ₁, θ₂):

1. Initialize θ₁⁽⁰⁾, θ₂⁽⁰⁾
2. Iterate:
   - Sample θ₁⁽ᵗ⁾ from P(θ₁ | θ₂⁽ᵗ⁻¹⁾, data)
   - Sample θ₂⁽ᵗ⁾ from P(θ₂ | θ₁⁽ᵗ⁾, data)

The conditional distributions are often simpler than the joint. Gibbs sampling is elegant: no rejection, no tuning of proposal variances, no acceptance rates to worry about.

The downside: you need to derive the conditional distributions. Sometimes they're not tractable.

### Diagnosing Convergence

How do you know the chain has converged?

- **Trace plot**: plot θ_t over iterations. Look for stationarity (no trend)
- **R-hat** (Gelman-Rubin diagnostic): run multiple chains from different starting points. If they've converged to the same distribution, R-hat ≈ 1.0
- **Effective Sample Size (ESS)**: accounting for autocorrelation, how many independent samples did you really get?
- **Autocorrelation function**: plot correlation between samples as a function of lag

### Modern MCMC: Hamiltonian Monte Carlo

Metropolis-Hastings proposes random walk steps, which are inefficient in high dimensions. **Hamiltonian Monte Carlo (HMC)** uses the *gradient* of the posterior to propose smarter moves.

Imagine a particle rolling down the gradient of the posterior, like a ball rolling downhill. HMC proposes moves that follow the geometry of the posterior, leading to better exploration and lower rejection rates.

HMC is powerful but requires computing gradients (often automatic).

**NUTS** (No-U-Turn Sampler) is an adaptive variant that automatically tunes the trajectory length.

### When MCMC Fails

- **Multimodal posteriors**: chain gets stuck
- **High dimensions**: proposal exploration becomes harder (curse of dimensionality)
- **Poor geometry**: posteriors that are very elongated or have tight correlations
- **Rare events**: if the region you care about has low probability, MCMC spends most time elsewhere

Solutions: reparameterize, use better proposals, use gradient-based methods, or re-express the problem.

---

## Real Data: Applications

### Bayesian Linear Regression

Fit a regression model: $y = β₀ + β₁ x + ε$

Posterior: P(β₀, β₁, σ | data)

With normal priors on coefficients and a weak prior on σ, the posterior is a 3D distribution over (β₀, β₁, σ).

Run MCMC to sample from the posterior. Result: a cloud of (β₀, β₁, σ) samples that represents your uncertainty about the coefficients.

### Mixture Model Inference

You observe data that looks like it comes from k different groups, but group membership is unknown.

Model: 
- Each observation comes from group z_i ∈ {1, ..., k}
- Each group has its own mean and variance
- Unknown: group means, variances, and which group each observation belongs to

MCMC alternates:
- Sample group assignments given current parameters
- Sample parameters given current assignments

By the end, the posterior tells you both the group structure and the parameter uncertainty.

---

## Rabbit Holes

### The Metropolis Algorithm's Origins

The Metropolis algorithm was developed in 1953 by Metropolis, Rosenbluth, Rosenbluth, Teller, and Teller while working on simulating liquids. They ran the algorithm on MANIAC (Mathematical Analyzer, Numerical Integrator, and Computer), one of the first computers.

The algorithm was motivated by statistical mechanics: simulating particles in a box, balancing energy states. It remained largely unknown outside physics until the 1990s, when Bayesian statisticians realized its power.

### The Ising Model and Phase Transitions

The Ising model is a grid of "spins" (each +1 or -1) interacting with neighbors. The energy is:

$$E = -\sum_{neighbors} S_i S_j$$

At low temperature, spins align (ordered phase). At high temperature, they're random (disordered). In between, a phase transition occurs.

MCMC (particularly Gibbs sampling) can simulate the Ising model efficiently. This connects to statistical mechanics, critical phenomena, and modern machine learning (Boltzmann machines).

### Probabilistic Programming Languages

Modern frameworks like **Stan**, **PyMC**, and **Pyro** automate MCMC. You specify the model; the software runs MCMC for you, often using HMC or NUTS.

This democratizes MCMC: complex models that were once the realm of experts are now accessible.

---

## Summary

MCMC is the bridge between elegant Bayesian theory and practical computation.

**Key insights:**

1. **Metropolis-Hastings constructs a Markov chain with the posterior as its stationary distribution.** We don't need to compute the normalizing constant or sample directly.

2. **The chain wanders more in high-density regions**, exploring the posterior proportionally to its probability.

3. **The proposal distribution affects efficiency**. Too narrow = slow, too wide = wasted. Finding the right variance requires tuning.

4. **Multimodality is hard**. If the posterior has isolated peaks, the chain may get stuck exploring one and missing others.

5. **Diagnostics matter**. Trace plots, R-hat, effective sample size—these tell you if the chain has converged.

6. **Modern variants like HMC are more efficient** in high dimensions by using gradient information.

This technique has revolutionized statistics, physics, and machine learning. It's the engine powering modern Bayesian data analysis.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Implement Metropolis-Hastings for simple distributions, verify convergence
- Exploration: Proposal tuning, multimodal distributions, mixing time
- Challenge: Gibbs sampling, Bayesian regression via MCMC, mixture models
- Thought experiments: Autocorrelation, convergence diagnostics, when MCMC fails
