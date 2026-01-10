# Part 4: Simulation

## When Exact Answers Are Impossible, Simulate

So far we've built intuition and theory. Now we turn to computation. Many real-world problems have no closed-form solution—no formula you can write down and solve. When math fails, simulation steps in.

Monte Carlo simulation means "if you can't compute it exactly, run many random trials and average the results." This section shows how to generate random samples, how to use them to estimate anything, and how to sample from tricky distributions that don't have simple formulas.

You'll see why simulation is so powerful: it converts hard math problems into easy coding problems. And you'll learn the surprising varieties of sampling methods available when nature (or your model) generates data in unexpected ways.

---

## Chapters in Part 4

1. **[Chapter 10: Throwing Darts at Pi](10-throwing-darts-at-pi/README.md)**
   - Monte Carlo estimation: the simplest method
   - How random sampling approximates integrals and probabilities
   - Accuracy and the law of large numbers

2. **[Chapter 11: When Exact Is Impossible](11-when-exact-is-impossible/README.md)**
   - Why simulation matters: practical problems with no closed form
   - Integration in high dimensions
   - The curse of dimensionality and why we need simulation

3. **[Chapter 12: Sampling from Strange Distributions](12-sampling-from-strange-distributions/README.md)**
   - Inverse transform sampling
   - Rejection sampling and adaptive methods
   - The ziggurat algorithm and efficient sampling

---

**Previous:** [← Part 3: Memory](../part-3-memory/README.md) | **Next:** [Part 5: Modeling →](../part-5-modeling/README.md)
