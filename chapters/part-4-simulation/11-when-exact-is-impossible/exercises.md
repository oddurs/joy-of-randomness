# Chapter 11 Exercises: When Exact Is Impossible

## Warm-up Exercises

**1. Grid vs. Monte Carlo sample complexity**

For dimensions d = 1, 2, 5, 10, compute:
- Number of grid points for 10 bins per dimension
- Number of Monte Carlo samples for 1% error (assume variance ≈ 1)

Create a table. At what dimension does Monte Carlo need fewer samples?

---

**2. Volume concentration**

Compute the fraction of the unit cube [0, 1]^d that lies in the interior [0.1, 0.9]^d for d = 1, 2, 5, 10, 20.

Plot this as a bar chart or line plot. What pattern do you observe?

---

**3. Interior vs. boundary**

As dimension increases, most volume moves to the boundary. Visualize this:

- For d = 1, 2, 3, compute what fraction of volume lies in the interior [0.2, 0.8]^d
- What does this tell you about where Monte Carlo samples land vs. where a grid places points?

---

**4. Distance from origin**

Generate 1,000 random points in [-1, 1]^d for d = 1, 2, 5, 10, 20.

For each dimension:
- Compute the distance from each point to the origin
- Plot a histogram
- Compare the mean distance to the theoretical expected value √(d/3)

---

## Exploration Exercises

**5. Distance concentration**

Generate 100 random points in [0, 1]^d for d = 1, 2, 5, 10, 20, 50.

For each dimension, compute pairwise distances and report:
- Minimum distance
- Maximum distance
- Ratio (max / min)

How does this ratio change with d? What does it mean?

---

**6. Angle concentration**

Generate 100 pairs of random vectors in R^d for d = 1, 2, 5, 10, 20, 50.

For each pair, compute the angle between the vectors (in degrees).

For each dimension, report:
- Average angle
- Standard deviation

As d increases, what happens to the average angle?

---

**7. High-dimensional geometry exploration**

Pick dimension d = 10. Generate 1,000 random points in [0, 1]^d.

Compute:
- Average distance to origin
- Average distance to nearest neighbor
- Average distance to furthest neighbor
- Ratio (furthest / nearest)

Repeat for d = 20 and d = 50. What changes?

---

**8. Monte Carlo in high dimensions**

Estimate the volume of a unit hypersphere in various dimensions using Monte Carlo (from Chapter 10).

For d = 2, 5, 10, 20, 30:
- Use 100,000 samples
- Report estimated volume
- Compare to exact formula

For very high d, the volume becomes tiny. Why?

---

## Challenge Exercises

**9. Grid vs. Monte Carlo for integration**

Define a function f(x) = exp(-||x||²/2) (unnormalized normal distribution).

Estimate ∫∫∫...∫ f(x) dx over [0, 1]^d using:
1. Grid method with 10 bins per dimension
2. Monte Carlo with 100,000 samples

Compare the computational time and accuracy for d = 2, 5, 10.

---

**10. Variance reduction in high dimensions**

Chapter 10 showed that stratified sampling reduces variance in 2D π estimation.

Try stratified sampling in high dimensions:
- Dimension d = 10
- Sample from [0, 1]^d using stratified approach (divide into 2^d cells)
- Compare to uniform Monte Carlo

Does stratification still help? Why or why not?

---

**11. The exponential wall**

For the function f(x) = 1 if ||x|| ≤ 1, else 0 (indicator for unit ball):

Compute: ∫...∫ f(x) dx over [-1, 1]^d (this is the volume of the unit ball)

Using Monte Carlo with 1,000,000 samples, estimate for d = 1, 2, 5, 10, 20, 50.

Compare to the exact formula. What happens as d increases?

---

**12. Sparse grid exploration**

Read about Smolyak sparse grids. They use O(n·log(n)^d) points instead of O(n^d).

Implement a simple sparse grid for d dimensions or use a library (like Tasmanian).

Compare to:
- Full grid
- Monte Carlo

For what dimensions is sparse grid better than Monte Carlo?

---

## Thought Experiments

**13. Why grids fail**

Consider a grid with one point per dimension (= 1^d = 1 point, regardless of d).

Locations: the center of [0, 1]^d.

The volume of [0, 1]^d is 1. But a single point can't represent the whole volume.

Now, as you add more points, the grid exponentially scales (in d) while the volume stays constant.

Why is this a fundamental problem?

---

**14. Why Monte Carlo scales**

Monte Carlo samples uniformly from [0, 1]^d. In high dimensions, most of the volume is near the boundary.

Does uniform sampling automatically concentrate where the volume is?

If f is roughly constant over [0, 1]^d, does it matter whether samples land in "empty" corners or near the boundary?

---

**15. Machine learning and dimensionality**

You have data in 1,000 dimensions. You expect the curse of dimensionality to make learning exponentially hard.

Yet deep neural networks (which learn in high dimensions) work well in practice.

Hypotheses:
1. **Manifold hypothesis**: Real data concentrates on a low-dimensional manifold
2. **Geometry hypothesis**: High-dimensional geometry is actually favorable for learning
3. **Approximation hypothesis**: Massive amounts of data compensate for dimension

Which hypotheses seem plausible to you? What evidence would you look for?

---

## Open-Ended Exploration

**Comparing sampling methods in high dimensions**

Implement and compare:
- Uniform Monte Carlo
- Stratified sampling (divide into cells, sample from each)
- Latin hypercube sampling
- Quasi-random sequences (Sobol)

For a fixed computational budget (e.g., 10,000 samples in 50 dimensions):
1. Estimate the integral of f(x) = exp(-||x||²/2) over [0, 1]^d
2. Measure computational time
3. Measure error (compare to true integral via numerical integration in lower dimensions)

Which method wins? Does it depend on d?

---

**The practical curse of dimensionality**

Find a real-world high-dimensional problem:
- Machine learning dataset (images, text embeddings)
- Physics simulation (molecular dynamics)
- Finance (portfolio optimization)
- Bayesian inference (posterior distribution)

1. Describe the dimensionality
2. Explain why the curse of dimensionality is relevant
3. Discuss what methods are used in practice (why not grids?)
4. Assess: is Monte Carlo or an alternative used?

---

**High-dimensional geometry visualization**

Visualize high-dimensional properties by projecting to 2D or 3D:

1. Generate 1,000 random points in d = 50 dimensions
2. Project to 2D using PCA or random projection
3. Plot the projection
4. Compute distances in original space; color points by distance to origin
5. Observe: do points concentrate in a shell? Do they fill the domain uniformly?

Repeat for different projection methods. What do you learn?

---

**Theoretical exploration**

Prove or disprove:

1. In d dimensions, most pairwise distances are within a constant factor of each other (O(√d))
2. The average angle between random vectors approaches 90° as d → ∞
3. Volume in the interior [ε, 1-ε]^d shrinks as (1-2ε)^d

Write up formal statements and proofs (or counterexamples).
