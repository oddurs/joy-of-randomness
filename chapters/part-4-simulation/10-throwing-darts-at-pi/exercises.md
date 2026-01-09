# Chapter 10 Exercises: Throwing Darts at Pi

## Warm-up Exercises

**1. Estimate π with increasing samples**

Write code to estimate π with 100, 1,000, 10,000, and 100,000 darts. For each:
- Print the estimate
- Print the error (difference from true π)
- Print the theoretical standard error

Do the observed errors match the theoretical predictions?

---

**2. Visualize convergence**

Plot π estimate vs. number of darts (use log scale for x-axis). What pattern do you see?

Now plot error vs. number of darts on a log-log scale. The error should follow a 1/√n line. Can you see this line?

---

**3. Confidence intervals**

Estimate π with 10,000 darts and compute a 95% confidence interval for the estimate.

Run this 20 times. How many of your 20 confidence intervals contain the true π? (Should be close to 19.)

---

**4. Variance across runs**

Run the π estimation 100 times with n=1,000 darts each. 

- Plot a histogram of the 100 estimates
- Compute the mean and standard deviation
- Compare the observed standard deviation to the theoretical standard error

---

## Exploration Exercises

**5. Hypersphere volumes**

Use Monte Carlo to estimate the volume of a unit hypersphere in dimensions 2, 5, 10, and 20.

For each dimension, compare your estimate to the exact formula:

$$V_d = \frac{\pi^{d/2}}{\Gamma(d/2 + 1)}$$

Which dimension is hardest to estimate accurately? Why?

---

**6. Dimension dependence**

Plot the volume of a unit hypersphere for dimensions 1 through 20 (use the exact formula).

What do you notice?
- When does the volume start to decrease?
- Why does it decrease in high dimensions?
- What does this tell you about the geometry of high-dimensional space?

---

**7. Monte Carlo integration**

Use Monte Carlo to estimate:

$$\int_0^1 \int_0^1 \sin(\pi x) \sin(\pi y) \, dx \, dy$$

Compare your estimate to the exact value (which is 4/π²).

How many samples are needed for 1% accuracy?

---

**8. Higher-dimensional integration**

Estimate the volume of a 10-dimensional unit hypercube with Monte Carlo.

The exact volume is 1. Does your estimate match?

Now estimate the volume of a 10-dimensional unit hypersphere. How many samples are needed for 1% accuracy?

---

## Challenge Exercises

**9. Stratified sampling**

Implement stratified sampling for π estimation: divide the square into an m×m grid, sample uniformly from each cell.

Compare to pure random sampling:
- Same number of darts
- Run 100 times each
- Which has lower variance?

Does stratification help? By how much?

---

**10. Confidence interval width**

For a fixed number of darts (say 10,000), compute the 95% confidence interval for π.

Now repeat for 1,000, 10,000, 100,000 darts.

How does the width of the confidence interval scale with n? Is it consistent with 1/√n theory?

---

**11. Importance sampling challenge**

Implement importance sampling for π estimation. The idea:
- Sample points not uniformly, but from a distribution that concentrates near the circle boundary
- Reweight by the ratio of the target to proposal distribution

Can you reduce the variance below pure random sampling?

---

**12. Two-dimensional integral**

Estimate:

$$\int_0^{2\pi} \int_0^{2\pi} \sqrt{2 + \cos(x) + \cos(y)} \, dx \, dy$$

This doesn't have a closed form, so Monte Carlo is useful!

Use 100,000 samples. Estimate the integral and assess uncertainty.

---

## Thought Experiments

**13. The 1/√n law**

To cut the error in half, you need 4 times more samples. To get 10 times more accuracy, you need 100 times more samples.

Think about this economically: if computing each sample costs the same, why is Monte Carlo still useful despite this slow scaling?

---

**14. Quasi-Monte Carlo**

Read about deterministic low-discrepancy sequences (Sobol, Halton, Latin hypercube). These achieve faster convergence than 1/√n—sometimes approaching 1/n.

The trade-off: they're more complex and less flexible. When might this be worth it?

---

**15. Curse of dimensionality**

In 1 dimension, a grid with 100 points covers the domain densely.

In 2 dimensions, you need 100² = 10,000 grid points for equivalent coverage.

In 10 dimensions, you need 100¹⁰ = 10^20 grid points (impossible).

But Monte Carlo needs only ~100,000 points in 10 dimensions!

Explain why Monte Carlo's sample size is *independent of dimension*, while grid methods scale exponentially worse.

---

## Open-Ended Exploration

**Estimating a complex integral**

Find a real integral from physics, finance, or statistics that doesn't have a closed form. (Examples: option pricing, partition functions, configuration integrals.)

1. Set up the integral formally
2. Use Monte Carlo to estimate it
3. Use stratified sampling or importance sampling to reduce variance
4. Assess the error and confidence interval
5. Write up your findings

---

**High-dimensional exploration**

Choose a dimension d (like 50 or 100).

1. Generate 10,000 random points in a d-dimensional unit cube
2. Compute pairwise distances between all points
3. Compute distances from each point to the origin
4. What's the average distance to origin? To nearest neighbor?
5. How do these compare to your intuition from low dimensions?

This explores the strange geometry of high-dimensional space.

---

**Monte Carlo error analysis**

For the π estimation, the error has both:
- **Bias**: The long-term average error (should be ~0 by LLN)
- **Variance**: The randomness around that average

1. Run π estimation 1,000 times with 1,000 darts each
2. Compute the bias: mean(estimates) - π
3. Compute the variance: std(estimates)²
4. Plot bias and variance vs. number of darts
5. Verify the 1/√n scaling holds

---

**Variance reduction in depth**

Implement and compare:
- Pure random sampling
- Stratified sampling (different grid sizes)
- Importance sampling (different proposal distributions)
- Antithetic sampling (use -x alongside x)

For the same computational budget, which technique wins?
