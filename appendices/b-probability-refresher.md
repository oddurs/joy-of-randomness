# Appendix B: Probability Refresher

This appendix reviews the foundational probability concepts you'll encounter throughout the course. Think of it as a reference—dip in when you see a term you're unsure about.

We won't derive everything rigorously. The goal is intuition: what does each concept mean, and when do you use it?

## Basic Definitions

### Outcome, Event, Sample Space

- **Outcome**: A single result. Flipping a coin gives heads or tails.
- **Event**: A set of outcomes. "Getting heads in the first two flips" (HH, HT, TH).
- **Sample space**: All possible outcomes. For two coin flips: HH, HT, TH, TT.

### Probability

Probability is the **long-run frequency** of an outcome.

If you flip a fair coin infinitely many times, heads appears 50% of the time. So $P(\text{heads}) = 0.5$.

Mathematically: for an event $A$,

$$P(A) = \frac{\text{number of outcomes in } A}{\text{total number of outcomes}}$$

But this only works for equally likely outcomes. (A coin is fair; the die is fair; the deck is well-shuffled.) If they're not equally likely, we need observed frequencies or other information.

### Complement

The complement of event $A$ is "not $A$". Written $A^c$ or $\neg A$.

$$P(A^c) = 1 - P(A)$$

If $P(\text{rain today}) = 0.3$, then $P(\text{no rain today}) = 0.7$.

## Combining Events

### Union (OR)

The union $A \cup B$ is "event $A$ or event $B$ (or both)".

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

Why subtract $P(A \cap B)$? Because if we just add $P(A) + P(B)$, we count the overlap twice.

**Example:** Drawing a card from a deck.
- $P(\text{red card}) = 26/52$
- $P(\text{face card}) = 12/52$
- $P(\text{red AND face card}) = 6/52$
- $P(\text{red OR face card}) = 26/52 + 12/52 - 6/52 = 32/52$

### Intersection (AND)

The intersection $A \cap B$ is "event $A$ and event $B$ (both occur)".

For *independent* events (one doesn't affect the other):

$$P(A \cap B) = P(A) \cdot P(B)$$

**Example:** Flip two coins.
- $P(\text{first is heads}) = 0.5$
- $P(\text{second is heads}) = 0.5$
- $P(\text{both are heads}) = 0.5 \times 0.5 = 0.25$

But if events are *dependent*, we use conditional probability (see below).

---

### Definition

$P(A | B)$ is "the probability of $A$ given that $B$ has occurred".

$$P(A | B) = \frac{P(A \cap B)}{P(B)}$$

Think of it as restricting the sample space to $B$, then asking what fraction of $B$ also includes $A$.

### Example: Drawing Cards

From a 52-card deck:
- $P(\text{second card is hearts} | \text{first card is hearts})$

After removing one hearts, there are 51 cards left, with 12 hearts.

$$P(\text{second hearts} | \text{first hearts}) = \frac{12}{51} \approx 0.235$$

Compare to $P(\text{second hearts}) = 13/52 = 0.25$ (with replacement).

The events are *dependent*—the first draw affects the second.

### Independence

Events $A$ and $B$ are independent if:

$$P(A | B) = P(A)$$

Knowing $B$ doesn't change the probability of $A$.

Equivalently: $P(A \cap B) = P(A) \cdot P(B)$.

---

## Expected Value

The expected value (or mean) of a random outcome is the long-run average.

$$E[X] = \sum (\text{outcome} \times \text{probability})$$

For a fair die:

$$E[X] = 1 \cdot \frac{1}{6} + 2 \cdot \frac{1}{6} + \ldots + 6 \cdot \frac{1}{6} = 3.5$$

If you roll many times, the average is 3.5.

### Intuition

Expected value isn't necessarily what happens in a single trial. You can't roll a 3.5. But over many trials, it's the center of gravity.

### Properties

- $E[X + Y] = E[X] + E[Y]$ (always true, even if $X$ and $Y$ are dependent)
- $E[cX] = c \cdot E[X]$ (scaling)
- If $X$ and $Y$ are independent: $E[X \cdot Y] = E[X] \cdot E[Y]$

---

## Variance and Standard Deviation

### Definition

$$\text{Var}(X) = E[(X - E[X])^2]$$

Standard deviation is the square root:

$$\text{SD}(X) = \sqrt{\text{Var}(X)}$$

### Intuition

- **Small variance**: outcomes cluster near the mean
- **Large variance**: outcomes are spread out

For a fair die ($E[X] = 3.5$):

$$\text{Var}(X) = \frac{1}{6}(1-3.5)^2 + \frac{1}{6}(2-3.5)^2 + \ldots = 2.917$$

$$\text{SD}(X) = \sqrt{2.917} \approx 1.71$$

So outcomes typically deviate from 3.5 by about 1.7.

### Why Squared Differences?

Why not just $E[|X - E[X]|]$ (absolute deviations)?

Squared differences penalize large deviations more heavily. They're also easier to work with mathematically and have nicer properties.

---

## Distributions

A distribution is a complete description of probabilities for all outcomes.

### Discrete Distributions

## ProbabilityCoin flip: P(H) = P(T) = 0.5
- Fair die: P(1) = ... = P(6) = 1/6

**Binomial Distribution**
Number of successes in $n$ independent trials, each with probability $p$.

Example: Flip a coin 10 times. How many heads?

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

If $n=10$ and $p=0.5$:

$$E[X] = np = 5 \quad \text{(expect 5 heads)}$$
$$\text{Var}(X) = np(1-p) = 2.5$$

**Poisson Distribution**
Number of rare events in a fixed time/space.

Example: Phone calls arriving at a help desk (rare, independent, at constant rate).

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}$$

where $\lambda$ is the rate.

- $E[X] = \lambda$
- $\text{Var}(X) = \lambda$ (mean equals variance—a special property)

### Continuous Distributions

**Uniform Distribution**
Equal probability across an interval [a, b].

$$P(X \in [a, b]) = 1$$
$$E[X] = \frac{a+b}{2}$$

**Normal Distribution (Gaussian)**
The bell curve. Defined by mean $\mu$ and standard deviation $\sigma$.

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

Properties:
- Symmetric around $\mu$
- 68% of data within $\mu \pm \sigma$
- 95% within $\mu \pm 2\sigma$
- 99.7% within $\mu \pm 3\sigma$ (the 3-sigma rule)

Most natural phenomena approximately follow normal distributions (heights, test scores, measurement errors).

**Exponential Distribution**
Wait time until next event (if events arrive at constant rate).

Example: Time until the next earthquake, given earthquakes happen at an average rate.

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$
$$E[X] = \frac{1}{\lambda}$$

**Poisson, Exponential, and Rates**
The Poisson distribution counts events in a time interval. The exponential distribution measures time between events. They're related.

---

## Bayes' Theorem

This is central to inference. Here's the formula:

$$P(A | B) = \frac{P(B | A) \cdot P(A)}{P(B)}$$

### Intuition

## Bayes' Theorem: Updating Beliefs with Evidenceior belief (before seeing $B$)
- $P(B | A)$: likelihood (how likely is $B$ if $A$ is true?)
- $P(A | B)$: posterior (your updated belief after seeing $B$)
- $P(B)$: normalizing constant (probability of observing $B$ overall)

### Example: Medical Testing

You take a COVID test. It's 95% accurate (95% of infected people test positive, 95% of uninfected test negative).

You test positive. What's the probability you actually have COVID?

Depends on prevalence! If 1% of people have COVID:

- $P(\text{have COVID}) = 0.01$ (prior)
- $P(\text{positive} | \text{have COVID}) = 0.95$ (true positive rate)
- $P(\text{positive} | \text{don't have COVID}) = 0.05$ (false positive rate)

$$P(\text{positive}) = 0.01 \times 0.95 + 0.99 \times 0.05 = 0.059$$

$$P(\text{have COVID} | \text{positive}) = \frac{0.95 \times 0.01}{0.059} \approx 0.161$$

Only 16% chance you have it, despite the positive test! That's because false positives are common when the disease is rare.

---

## The Law of Large Numbers

If you repeat an experiment many times, the observed frequency approaches the true probability.

Flip a coin 10 times: maybe 7 heads (70%).
Flip it 1000 times: maybe 502 heads (50.2%).
Flip it 1,000,000 times: maybe 500,123 heads (50.01%).

As $n \to \infty$, the observed frequency converges to the true probability.

---

## The Central Limit Theorem

This is one of the most important results in statistics.

**Statement:** The mean of many independent samples is approximately normally distributed, regardless of the underlying distribution.

### Example

Roll one die: outcomes are uniform (each value equally likely, no bell curve).

Roll 10 dice and compute the mean: still not normal, but more bell-shaped.

Roll 1000 dice and compute the mean: perfect bell curve.

### Why It Matters

Many things in nature are sums of many independent effects. Heights = genetics + nutrition + environment + ... → roughly normal.

Test scores = knowledge + luck + fatigue + ... → roughly normal.

This is why the normal distribution appears everywhere.

### Mathematical Statement

For samples $X_1, X_2, \ldots, X_n$ from any distribution with mean $\mu$ and variance $\sigma^2$:

$$\frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \approx N(0, 1)$$

where $\bar{X} = \frac{1}{n}\sum X_i$ and $N(0,1)$ is standard normal.

The key: the denominator has $\sqrt{n}$. So as we collect more data, the standard error shrinks, and we know the mean more precisely.

---

## Correlation and Causation

### Correlation

Two variables are correlated if they tend to move together.

Example: ice cream sales and temperature. High correlation—when it's hot, people buy more ice cream.

Measured by correlation coefficient $r$, ranging from -1 to +1:
- $r = +1$: perfect positive correlation
- $r = 0$: no correlation
- $r = -1$: perfect negative correlation

### Causation

Temperature causes ice cream sales (people buy more when hot).

### The Trap

Correlation doesn't imply causation.

- Ice cream sales and drowning deaths are correlated (both peak in summer)
- But ice cream doesn't cause drowning. Summer weather causes both.

This is a confounding variable: it affects both and creates spurious correlation.

---

## Common Mistakes

### 1. "The streak has to end"

If you flip a fair coin and get 10 heads in a row, the next flip is still 50-50. The past doesn't influence the future (for independent events).

This is called the "gambler's fallacy."

### 2. Misunderstanding probability with small samples

"I flipped a coin 4 times and got 3 heads. The coin is biased."

With small $n$, random variation is large. You need many trials to detect bias.

### 3. Confusing conditional probabilities

Example: $P(\text{test positive} | \text{have disease})$ is not the same as $P(\text{have disease} | \text{test positive})$.

### 4. Ignoring base rates

A test is 99% accurate. You test positive. Are you 99% sure you have the disease?

No! It depends on how common the disease is (base rate). See the medical testing example above.

### 5. Summing probabilities beyond 1

If you have multiple scenarios, they must sum to 1 (if they're exhaustive and mutually exclusive).

Common error: "There's a 60% chance of rain tomorrow and a 60% chance of sunshine." These don't add up. (Tomorrow can't be both rain and sunshine.)

---

## Python Review

### NumPy and Randomness

```python
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Generate random numbers
flips = np.random.randint(0, 2, 1000)  # 1000 coin flips (0=T, 1=H)
heads = np.sum(flips)
print(f"Proportion of heads: {heads / 1000}")

# Generate from distributions
normal_samples = np.random.normal(loc=0, scale=1, size=1000)
print(f"Mean: {np.mean(normal_samples):.3f}")
## Python Reference
### Conditional Probability in Code

```python
# Joint event: both die rolls > 3
both_gt_3 = np.sum((die1 > 3) & (die2 > 3))

# P(both > 3 | first > 3)
first_gt_3 = np.sum(die1 > 3)
conditional = both_gt_3 / first_gt_3

print(f"P(both > 3 | first > 3): {conditional}")
```

### Plotting Distributions

```python
import matplotlib.pyplot as plt

# Histogram of samples
plt.hist(normal_samples, bins=30, density=True, alpha=0.7, label='Samples')

# Overlay theoretical normal
x = np.linspace(-4, 4, 100)
pdf = (1 / np.sqrt(2*np.pi)) * np.exp(-x**2 / 2)
plt.plot(x, pdf, 'r-', label='Theory')

plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.show()
```

---

## When to Use What

| Concept | Use when... |
|---------|-----------|
| Conditional probability | One event depends on another |
| Bayes' theorem | You need to update beliefs with evidence |
| Expected value | You want the long-run average |
| Variance | You want to know how spread out outcomes are |
| Normal distribution | Data is from many independent sources |
| Central limit theorem | You're averaging many samples |
| Law of large numbers | You want empirical frequencies to match theory |

---

## Further Reading

This appendix is a snapshot. Deeper dives:

- **"Thinking, Fast and Slow"** by Daniel Kahneman: biases and probability intuition
- **"Fooled by Randomness"** by Nassim Taleb: common mistakes
## Quick Lookup:
Most importantly: build intuition with simulations. The code in this course is designed to let you *see* probability, not just read about it.

You're ready. Let's go.


---

**Return to:** [Table of Contents](../../README.md)