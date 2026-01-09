# Chapter 12: Sampling from Strange Distributions

## The Problem: Going Beyond Uniform

You know how to generate uniform random numbers—computers are very good at that. But what if you need an exponential? A normal? A distribution defined by a complicated formula you can barely evaluate?

This is the fundamental problem of sampling: **How do you generate randomness with a specific shape?**

The answer turns out to be surprisingly clever and surprisingly tricky.

---

## First Contact: Inverse Transform Sampling

Start with something simple. You have uniform random numbers U ~ Uniform(0, 1). You want samples from an exponential distribution with rate λ.

Here's the magic:

$$X = -\frac{1}{\lambda} \ln(1 - U)$$

That's it. If U is uniform on [0, 1], then X follows an exponential distribution with rate λ.

Let's see why. The exponential CDF is:

$$F(x) = 1 - e^{-\lambda x}$$

Solving for x:

$$F^{-1}(u) = -\frac{1}{\lambda} \ln(1 - u)$$

Since U is uniform, 1 - U is also uniform. So:

$$X = -\frac{1}{\lambda} \ln(U)$$

is the inverse transform.

### Why This Works: The Probability Integral Transform

**Theorem:** If U ~ Uniform(0, 1) and F is a continuous CDF, then $X = F^{-1}(U)$ has CDF F.

**Proof:** 
$$P(X \leq x) = P(F^{-1}(U) \leq x) = P(U \leq F(x)) = F(x)$$

It's almost magical: take uniform samples, apply the inverse CDF, and you get samples from any distribution!

### But There's a Catch

This is elegant, but it requires knowing F and its inverse. For some distributions, this is easy:
- Exponential: CDF has a closed form, inverse is simple
- Uniform: trivial
- Weibull: similar to exponential

For others, it's hard:
- Normal distribution: CDF is Φ, which has no closed form
- Beta distribution: no simple inverse
- Arbitrary distributions defined by evaluating a PDF at a point

For the normal, you could numerically invert the CDF, but that's slow. We need a better approach.

---

## Patterns Emerge: Rejection Sampling

Here's another idea. Suppose you want to sample from a distribution with PDF f(x). You don't know the CDF, but you can *evaluate* f(x).

**Rejection sampling:**

1. Pick an easy distribution g(x) (the "proposal") where you can sample cheaply
2. Find a constant M such that f(x) ≤ M·g(x) for all x
3. Repeat:
   - Sample X from g
   - Sample U ~ Uniform(0, 1)
   - If U ≤ f(X) / (M·g(X)), accept X
   - Otherwise, reject and try again

The accepted samples follow f(x).

### Why It Works

Think geometrically. You're sampling uniformly under the curve y = M·g(x). The region below the curve y = f(x) is the "acceptance region." Uniform sampling in this region, projected onto the x-axis, gives samples from f(x).

### Example: Sampling from a Normal

You want samples from N(0, 1). One proposal: g(x) = Exponential(1).

The PDF of N(0, 1) is:

$$f(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$$

We only need to sample the positive half (by symmetry). For x ≥ 0:

$$f(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2} \leq \sqrt{\frac{2}{\pi}} e^{-x}$$

So the envelope is g(x) = Exponential(1) with M = √(2/π) ≈ 0.798.

The acceptance rate is roughly 80%. Not bad!

### The High-Dimensional Problem

But here's the catch: **rejection sampling scales catastrophically in high dimensions.**

Consider sampling from a d-dimensional normal. The mode (center) is where the PDF is largest. But in high dimensions, the volume is concentrated far from the center.

If your proposal g is centered near the mode, most of the probability mass of g is in the "wrong place" (near the mode). Your acceptance rate becomes exponentially small in d.

For d = 10, the acceptance rate might drop to 1%. For d = 50, it could be 10^(-10). You'd need trillions of proposals to get a single accepted sample.

**This is the curse of dimensionality again.** Our simple sampling methods fail in high dimensions.

---

## The Theory

### Inverse Transform Sampling: Formal Statement

**Algorithm:**
1. Compute the CDF F(x) = P(X ≤ x)
2. Compute the inverse F^(-1)
3. Sample U ~ Uniform(0, 1)
4. Return X = F^(-1)(U)

**Pros:**
- Simple, elegant, no waste
- One sample of U gives one sample of X
- Exact (no approximation error)

**Cons:**
- Requires closed-form F and F^(-1)
- If inverting the CDF is slow, this becomes expensive

### Rejection Sampling: Formal Statement

**Algorithm:**
1. Choose proposal g(x) and constant M such that f(x) ≤ M·g(x)
2. Repeat:
   - Sample X ~ g
   - Sample U ~ Uniform(0, 1)
   - If U ≤ f(X) / (M·g(X)), return X

**Efficiency:**
- Acceptance rate = 1/M
- Expected number of proposals per accepted sample = M
- Want M as small as possible (tightest envelope)

**Pros:**
- Works for any distribution you can evaluate
- No need to invert anything

**Cons:**
- Need to find a good proposal and compute M
- Rejection rate increases with dimension

---

## Going Deeper: Special Cases and Advanced Methods

### Box-Muller Transform: An Exact Method for Normals

One elegant way to sample from N(0, 1) is the Box-Muller transform:

1. Sample U₁, U₂ ~ Uniform(0, 1) independently
2. Let R = √(-2 ln U₁)) and Θ = 2π U₂
3. Return X = R cos(Θ) and Y = R sin(Θ)

Both X and Y are independent N(0, 1).

This is exact, no rejection waste, and quite efficient.

**Why it works:** Sampling uniformly in a circle in Cartesian coordinates is equivalent to the correct PDF in polar coordinates. A bit of calculus shows the result is normally distributed.

### Ziggurat Algorithm: Fast Rejection for Common Distributions

The Ziggurat is a clever way to implement rejection sampling for the normal (and exponential) with minimal overhead.

The idea: stack horizontal strips of decreasing width, like a ziggurat.

- For most proposals (the larger strips), acceptance is almost certain
- Only occasionally do you need the full rejection test
- Result: very fast, efficient sampling

This is widely used in practice (e.g., in NumPy's normal sampling).

### Why Rejection Sampling Fails in High Dimensions

In d dimensions, if f is a d-dimensional normal and g is another d-dimensional normal (both standard), you might expect the rejection test to be easy.

But here's the problem: the ratio f(x) / g(x) varies wildly with x. Near the mode, it's nearly 1. But as you move away from the mode, the geometry becomes favorable for g but not f.

In fact, rejection rates scale as exp(-c·d) for some constant c > 0. With d = 50, you're looking at 10^(-10) rejection rates.

The fundamental issue: you need M ≥ sup_x [f(x) / g(x)]. In high dimensions, this supremum is exponentially large.

---

## Real Data: Practical Sampling

### Generating Variates for Simulations

When you build a simulation (epidemic model, queuing system, etc.), you often need to generate random events with specific distributions.

- Time until next customer arrival? Exponential.
- Service time at the checkout? Could be normal, exponential, or lognormal.
- Life spans in a population model? Gamma or Weibull.

Efficient sampling is crucial for large-scale simulations. A 1% slowdown in sampling translates to measurable runtime costs.

### Bayesian Inference: Sampling from Posteriors

In Bayesian statistics, you observe data and want to sample from the posterior distribution:

$$P(\theta | \text{data}) \propto P(\text{data} | \theta) \cdot P(\theta)$$

Often, the posterior has no closed-form distribution. You can evaluate it (multiply the likelihood and prior), but you can't sample directly.

This is where the challenge becomes acute. Simple methods like rejection sampling fail. More sophisticated methods (Markov chain Monte Carlo) are needed.

---

## Rabbit Holes

### A Brief History of Random Number Generation

For centuries, randomness was a mathematical curiosity. Then, around WWII, physicists needed random numbers for the Manhattan Project.

Early methods used physical devices (roulette wheels, dice, radioactive decay). Then came software: linear congruential generators (LCGs), which were simple but flawed.

The late 20th century saw an explosion of methods: Mersenne Twister (fast, good quality), cryptographic generators (secure but slow), quasi-random sequences (low-discrepancy but not truly random).

Each has trade-offs: speed vs. quality, simplicity vs. rigor.

### Quasi-Random Sequences vs. True Randomness

Quasi-random sequences (like Sobol sequences or Halton sequences) are *deterministic* but *low-discrepancy*. They spread out evenly, avoiding clumps.

For Monte Carlo integration, they can be faster than true random sampling because they avoid lucky or unlucky concentrations.

But they lack the independence property of true randomness, so they don't work for all applications (e.g., cryptography).

### Cryptographically Secure Random Number Generation

For security applications, randomness must be unpredictable. Standard PRNGs (pseudorandom number generators) are deterministic—if someone knows the seed, they can predict all future numbers.

Cryptographic generators use OS-level randomness (/dev/urandom on Linux, CryptGenRandom on Windows) seeded by physical unpredictability.

The cost: they're slower. But they're essential for anything involving secrets.

---

## Summary

The simple question—"How do I sample from a non-uniform distribution?"—has beautiful answers for easy cases and reveals fundamental challenges for hard cases.

**Inverse transform sampling** is elegant: use the probability integral transform. But it requires knowing the inverse CDF, which is often impractical.

**Rejection sampling** is flexible: you only need to evaluate the PDF. But it scales catastrophically with dimension.

For simple, low-dimensional distributions, these methods suffice. For high-dimensional distributions (like Bayesian posteriors), they fail spectacularly.

The solution, which we'll explore in Part VI, is to avoid sampling the entire distribution at once. Instead, **build a Markov chain that explores the distribution** gradually. The chain doesn't need to know the full distribution; it just needs to move in directions that increase probability.

This is the power of Markov chain Monte Carlo—and it works in any dimension.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Inverse transform for exponential, verify the results
- Exploration: Rejection sampling with different proposals and envelopes
- Challenge: High-dimensional rejection sampling, observe acceptance rate collapse
- Thought experiments: Universality of sampling, computational limits, connections to other fields
