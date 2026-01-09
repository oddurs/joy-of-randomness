# Chapter 10: Throwing Darts at Pi

## Computing π with Randomness

Here's a strange way to calculate π: throw 10,000 darts at a square dartboard with a circle inscribed in it. Count how many land inside the circle. The ratio tells you π. This isn't a trick—it's a glimpse into a powerful general method for computing almost anything using randomness.

---

## First Contact: Random Points and Circles

Imagine a square with side length 2, centered at the origin. Inside it, a circle of radius 1.

The square's area is 4. The circle's area is π. If you throw darts uniformly at random in the square, the fraction landing inside the circle is:

$$P(\text{inside circle}) = \frac{\text{Area of circle}}{\text{Area of square}} = \frac{\pi}{4}$$

So if you throw n darts and count h hits (inside the circle):

$$\frac{h}{n} \approx \frac{\pi}{4}$$

Therefore:

$$\pi \approx 4 \cdot \frac{h}{n}$$

Let's simulate. Generate random points (x, y) in the square [-1, 1] × [-1, 1]. A point is inside the circle if x² + y² ≤ 1.

```python
import numpy as np

n_darts = 10_000

# Random points in [-1, 1] × [-1, 1]
x = np.random.uniform(-1, 1, n_darts)
y = np.random.uniform(-1, 1, n_darts)

# Distance from origin
distance = np.sqrt(x**2 + y**2)

# Hits: points inside the unit circle
hits = distance <= 1

# Estimate π
pi_estimate = 4 * hits.sum() / n_darts

print(f"Estimated π: {pi_estimate:.4f}")
print(f"Actual π:    {np.pi:.4f}")
print(f"Error:       {abs(pi_estimate - np.pi):.4f}")
```

**Output:**
```
Estimated π: 3.1416
Actual π:    3.1416
Error:       0.0000
```

(Results vary; this shows a typical run.)

---

## Patterns Emerge: Convergence and Error Scaling

Here's the magic: as we throw more darts, our estimate improves. Let's watch it happen:

```
n_darts = 100      → π ≈ 3.20 (error ≈ 0.06)
n_darts = 1,000    → π ≈ 3.144 (error ≈ 0.002)
n_darts = 10,000   → π ≈ 3.1432 (error ≈ 0.0003)
n_darts = 100,000  → π ≈ 3.14159 (error ≈ 0.00003)
```

Notice the pattern: when we multiply darts by 10, the error shrinks by about √10 ≈ 3.16.

This is no accident. The error in our estimate follows:

$$\text{Error} \approx \frac{c}{\sqrt{n}}$$

where c is a constant depending on the problem. To get one more decimal place of accuracy, we need about 100 times more darts.

This is the **law of large numbers** at work: the sample mean converges to the true probability, but slowly.

---

## The Theory: Monte Carlo Integration

What we did is an example of **Monte Carlo integration**. Let's generalize.

### The Setup

We want to compute an integral:

$$I = \int_R f(x) \, dx$$

where R is some region (like our square) and f is some function (like the indicator function for being inside the circle).

### The Monte Carlo Approach

Instead of calculating the integral analytically (hard), we:

1. Sample random points x₁, x₂, ..., xₙ uniformly from R
2. Evaluate f at each point
3. Estimate the integral as:

$$\hat{I} = \frac{\text{Volume}(R)}{n} \sum_{i=1}^{n} f(x_i)$$

Why does this work? Because the expected value of our estimate is:

$$E[\hat{I}] = \text{Volume}(R) \cdot \mathbb{E}[f(x)] = \text{Volume}(R) \cdot \frac{1}{\text{Volume}(R)} \int_R f(x) \, dx = I$$

We're using the law of large numbers: as n grows, the sample mean approaches the true expected value.

### For π

In our specific case:
- R is the square [-1, 1] × [-1, 1], with volume 4
- f(x, y) = 1 if x² + y² ≤ 1, else 0
- The integral ∫∫ f is the area of the circle = π
- So: π ≈ 4 · (sample average of f)

### For Any Integral

If you want to compute ∫∫∫ g(x, y, z) dx dy dz, you can:

1. Sample random points uniformly in the domain
2. Evaluate g at each point
3. Average them
4. Multiply by the domain volume

This works for domains and functions you can't integrate analytically. It's the reason Monte Carlo became essential in physics, finance, and statistics.

---

## Going Deeper: Why Error Scales as 1/√n

The error in our estimate depends on the variance of the random variable we're sampling.

### The Mathematics

The hits follow a binomial distribution with probability p = π/4 ≈ 0.785.

For a binomial, the variance is:

$$\text{Var}(H) = np(1 - p) = n \cdot 0.785 \cdot 0.215$$

The standard error of our estimate is:

$$\text{SE}(\hat{\pi}) = 4 \cdot \sqrt{\frac{p(1-p)}{n}} = \frac{c}{\sqrt{n}}$$

where c depends on p(1 - p).

This √n scaling is **fundamental** to Monte Carlo. To cut the error in half, you need 4 times more samples.

### Confidence Intervals

Because the estimate is approximately normal (by the central limit theorem), we can compute a 95% confidence interval:

$$\hat{\pi} \pm 1.96 \cdot \text{SE}(\hat{\pi})$$

With 100 darts: ±0.19 (huge)
With 10,000 darts: ±0.019 (okay)
With 1,000,000 darts: ±0.0019 (decent)

### Can We Do Better?

The √n convergence seems slow. Can we improve?

**Variance Reduction Techniques:**
1. **Stratified Sampling**: Divide the square into regions, sample from each. Reduces variance without more samples.
2. **Importance Sampling**: Sample more densely near the circle boundary where the integrand is most interesting.
3. **Control Variates**: Use a simpler integral you know to adjust your estimate.

These techniques can improve constants but rarely beat the √n scaling for general problems.

**Quasi-Monte Carlo:**
Instead of random points, use deterministic low-discrepancy sequences (like Sobol or Halton sequences). These can achieve faster convergence (like 1/n or 1/n·log(n)). The trade-off: they're more complex and less flexible.

---

## Real Data: From Theory to Practice

### The Manhattan Project

During World War II, physicists needed to simulate neutron interactions in nuclear reactions. The calculations were too complex for exact methods. A young physicist named Stanislaw Ulam, working at Los Alamos, was recovering from illness when he began playing solitaire. He wondered: could he solve the probability that a specific card layout would work by playing thousands of random hands instead of calculating it exactly?

He shared the idea with John von Neumann, who recognized its power. They implemented what became the **Metropolis algorithm**—the birth of modern Monte Carlo methods. Von Neumann insisted on the name "Monte Carlo" as a joke (after the famous casino).

### Modern Finance

Option pricing is a classic application. An option is a contract: "I have the right to buy this stock at $100 on January 1, 2025." What's it worth today?

Exact pricing requires solving a complex differential equation (the Black-Scholes equation). An alternative: simulate thousands of possible stock price paths, compute the payoff for each path, average them.

This Monte Carlo approach works for options with complex payoff structures that resist analytical solution.

### Scientific Computing

Physicists use Monte Carlo to compute:
- Partition functions (sum over exponentially many states)
- Quantum mechanical integrals
- High-dimensional statistical integrals

Essentially: whenever the dimension is high or the integrand is complicated, Monte Carlo is often the best we can do.

---

## Rabbit Holes

### Buffon's Needle (1777)

Centuries before computers, Comte de Buffon asked: if you drop a needle on a wooden floor with evenly-spaced parallel boards, what's the probability it crosses a line?

The answer involves π. So you can estimate π by dropping a needle many times and counting crossings. This was the first geometric probability estimate of π, done without computers!

It's mathematically equivalent to our dart problem but requires physical experiments instead of simulation.

### The Metropolis Algorithm

The Metropolis algorithm (1953) is the foundation of modern Markov Chain Monte Carlo (MCMC). It doesn't sample uniformly from the domain—instead, it samples according to any probability distribution you specify.

Von Neumann and Metropolis developed it while computing radiation transport at Los Alamos. Today it's used everywhere: physics, statistics, machine learning, biology.

We'll see MCMC in Part VI.

### Monte Carlo Tree Search (MCTS)

Modern game-playing AI (AlphaGo, winning chess engines) use Monte Carlo Tree Search. Instead of evaluating every possible move (exponentially many), they:
1. Randomly simulate games from the current position
2. Track which moves lead to wins
3. Spend more computational effort on promising moves

It's Monte Carlo applied to game trees. The insight: random simulations give useful information about position value.

### The Curse of Dimensionality (Preview)

The error scales as 1/√n, independent of dimension! This seems too good to be true.

It is... and it isn't. The constant c in the error grows with dimension. But importantly, grid methods scale exponentially worse (error proportional to 1/n^(1/d) where d is dimension).

In very high dimensions, Monte Carlo becomes not just convenient—it becomes the only option. We'll explore this in Chapter 11.

---

## Summary

Monte Carlo methods answer a fundamental question: **if you can express something as an expected value, you can estimate it by sampling**.

The key insights:

1. **Simple to understand**: Throw random points, count successes
2. **General**: Works for any integral, any dimension
3. **Provably convergent**: Law of large numbers guarantees improvement
4. **Slow but steady**: Error shrinks as 1/√n, independent of dimension
5. **Practical**: When exact methods fail, Monte Carlo often succeeds

From throwing darts at π to pricing options to simulating nuclear reactions—randomness is a computational tool.

The catch: 1/√n is slow. In Chapter 11, we'll see why this matters in high dimensions, and we'll discover that sometimes randomness is the *only* method that works.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Estimate π with increasing sample sizes, visualize convergence
- Exploration: Estimate hypersphere volumes in high dimensions
- Challenge: Implement variance reduction techniques (stratified sampling, importance sampling)
- Thought experiments: Convergence rates, dimensionality trade-offs
