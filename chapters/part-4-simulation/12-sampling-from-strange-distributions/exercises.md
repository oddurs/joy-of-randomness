# Chapter 12 Exercises: Sampling from Strange Distributions

## Warm-up Exercises

**1. Inverse transform for exponential**

Use the inverse transform method to generate 10,000 samples from an exponential distribution with λ = 2.

Plot a histogram of the samples. Overlay the theoretical PDF: f(x) = 2·e^(-2x).

Compute the sample mean and standard deviation. Compare to theory (mean = 0.5, std = 0.5).

---

**2. Inverse transform for Weibull**

The Weibull distribution has CDF:

$$F(x) = 1 - e^{-(x/\lambda)^k}$$

The inverse is:

$$F^{-1}(u) = \lambda (-\ln(1 - u))^{1/k}$$

Generate 5,000 samples from Weibull(k=2, λ=1) using inverse transform.

Plot a histogram and compare to the theoretical PDF (from scipy.stats).

---

**3. Inverse transform for Pareto**

The Pareto distribution models wealth inequality, power laws, etc.

The inverse CDF is:

$$X = x_m \cdot U^{-1/\alpha}$$

where x_m is the minimum value (location) and α is the shape.

Generate 5,000 samples from Pareto(x_m=1, α=2).

Plot on a log-log scale. Notice the long tail!

---

**4. Comparing proposals for rejection sampling**

Implement rejection sampling for N(0, 1) using two different proposals:

1. **Exponential proposal:** g(x) = e^(-|x|)
2. **Uniform proposal:** g(x) = uniform on [-4, 4]

For each, generate 1,000 samples and report:
- Acceptance rate
- Number of proposals needed per accepted sample
- KS test p-value (goodness of fit)

Which is better?

---

## Exploration Exercises

**5. Optimizing the envelope for rejection sampling**

For the exponential proposal to N(0, 1), we use M = √(2/π) ≈ 0.798.

What if we use a different proposal? Implement:

1. Laplace (double exponential) proposal
2. Student's t proposal (with various df)

For each, compute the optimal envelope M and the resulting acceptance rate.

Which proposal is best?

---

**6. Box-Muller vs. rejection sampling**

Implement both Box-Muller and rejection sampling (exponential proposal) to generate 100,000 normal samples.

Compare:
- Acceptance rate (Box-Muller is exact, so 100%)
- Wall-clock time
- Quality of samples (KS test, Q-Q plot)

Which is faster in practice?

---

**7. Generating from a mixture of normals**

A mixture of normals is:

$$f(x) = 0.3 \cdot N(-2, 1) + 0.7 \cdot N(2, 0.5)$$

(30% weight on N(-2, 1), 70% weight on N(2, 0.5))

You can evaluate f(x) at any point, but no closed-form inverse CDF exists.

Use rejection sampling to generate 5,000 samples. What's the acceptance rate?

Hint: Find an envelope by computing max f(x) / g(x) over a grid.

---

**8. Non-uniform rejection sampling**

Standard rejection sampling uses a uniform proposal. But you can use any proposal!

For sampling from N(0, 1):
- Use a uniform proposal on [-2, 2] (smaller domain)
- What envelope M do you need?
- What acceptance rate?

Compare to a uniform on [-4, 4]. Why is the smaller domain better?

---

## Challenge Exercises

**9. Rejection sampling in high dimensions**

Try rejection sampling to generate samples from a d-dimensional standard normal for various d:

```python
d_values = [1, 2, 3, 5, 10, 15, 20]
```

For each dimension:
- Generate 100 samples using rejection sampling
- Record acceptance rate and number of proposals
- Plot both as functions of d

Does the acceptance rate decay exponentially? Fit: rate ≈ a·exp(-b·d).

---

**10. Understanding the high-dimensional collapse**

In d dimensions, sampling from N(0, I_d) with a uniform proposal on [-c, c]^d:

Why does the acceptance rate decay exponentially?

**Hint:** Think about the volume of the d-dimensional ball vs. the d-dimensional cube.

Compute:
- Volume of unit ball in d dimensions
- Volume of [-1, 1]^d

As d → ∞, what happens to the ratio?

---

**11. Stratified rejection sampling**

One way to improve rejection sampling in high dimensions:

Divide the domain into cells. For each cell, estimate the maximum of f/g.

Use cell-specific envelopes instead of a global M.

Implement this for 10-dimensional normal sampling.

Does stratification improve the acceptance rate?

---

**12. Comparing inverse transform and rejection sampling**

For distributions where both methods are feasible:

1. Generate 100,000 samples via inverse transform
2. Generate 100,000 samples via rejection sampling
3. Compare wall-clock time and memory usage

For which distributions is inverse transform significantly faster?

For which is rejection sampling actually faster (despite rejections)?

---

## Thought Experiments

**13. Universality of sampling**

Theorem: If you can evaluate f(x) (up to a constant), you can sample from f using rejection sampling.

But is there a distribution where this becomes *computationally infeasible*?

What properties of f would make rejection sampling break?

(Hint: Think high-dimensional, multimodal, etc.)

---

**14. Can you sample from any distribution?**

You have a source of uniform random numbers U ~ Uniform(0, 1).

Can you generate samples from *any* continuous distribution?

What's the theorem that guarantees this?

Are there distributions where this becomes impractical?

---

**15. Information-theoretic limits**

Generating a single uniform sample on [0, 1] requires one "bit" of randomness (roughly).

Generating a sample from a distribution with entropy H requires... how many bits?

For a distribution with very high entropy (very spread out), what does this imply about the number of uniform samples needed?

---

## Open-Ended Exploration

**The curse strikes again: Sampling from high-D posteriors**

In Bayesian inference, you observe data y and want to sample from:

$$P(\theta | y) \propto P(y | \theta) \cdot P(\theta)$$

Implement this:
1. Model: y ~ Normal(μ, σ²), with priors μ ~ Normal(0, 10), σ ~ Exp(1)
2. Generate synthetic data: 100 observations with true μ = 5, σ = 2
3. Define the (un-normalized) posterior density
4. Try to sample using rejection sampling

What happens as you add more observations? As dimensionality increases (more parameters)?

This is the motivation for MCMC.

---

**A pathological distribution**

Construct a distribution that breaks rejection sampling:

Design f(x) such that:
- It's easy to evaluate f(x)
- Any reasonable proposal g has acceptance rate < 0.1%
- You can describe why this is hard

Example ideas:
- A distribution with many isolated modes
- A high-dimensional distribution with most volume in a thin shell
- A distribution where f varies wildly

Analyze your pathological case. Why does it fail?

---

**Quasi-random sequences for sampling**

Read about Sobol sequences or Halton sequences (low-discrepancy sequences).

Implement inverse transform sampling using quasi-random uniforms instead of pseudo-random uniforms.

For Monte Carlo integration (Chapter 10), does quasi-random help or hurt?

Why might quasi-random be better for some applications but worse for others?
