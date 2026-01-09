# Chapter 16: Thinking in Distributions

## From Certainty to Uncertainty

A coin lands heads 7 out of 10 times. Is it fair?

Your gut says "maybe biased," but the answer isn't a single number. The Bayesian answer is a whole distribution of possibilities: the coin might be slightly biased toward heads, or heavily biased, or fair by coincidence. Each possibility has some plausibility.

Instead of asking "what's the true value?" we ask "what values are plausible, and how plausible?" This shift—from point estimates to distributions—is the essence of Bayesian thinking.

---

## First Contact: The Prior and the Posterior

Before seeing any data, you have a **prior belief** about the coin. Let's say any bias from 0 to 1 is equally likely:

$$P(\theta) = \text{Uniform}(0, 1)$$

where $\theta$ is the probability of heads.

Now you observe data: 7 heads in 10 flips. This data has some likelihood given different values of $\theta$:

$$P(\text{7 heads in 10} \mid \theta) = \binom{10}{7} \theta^7 (1-\theta)^3$$

Bayes' theorem combines prior and likelihood to give the **posterior**—your updated belief after seeing data:

$$P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \times P(\theta)$$

With a Uniform(0,1) prior, the posterior is:

$$P(\theta \mid \text{data}) \propto \theta^7 (1-\theta)^3$$

This is a **Beta(8, 4) distribution**.

### What's a Beta Distribution?

The Beta distribution is defined on [0,1] and parameterized by two shape parameters (α, β):

$$P(\theta) = \text{Beta}(\alpha, \beta)$$

The mean is $\alpha / (\alpha + \beta)$. For Beta(8, 4), the mean is 8/12 ≈ 0.67.

The key insight: **the posterior is shifted toward 0.7 (the observed frequency) but with uncertainty.** It's not a single point; it's a distribution.

---

## Patterns Emerge

### The Posterior Combines Prior and Data

Three priors, one dataset:

1. **Uniform prior**: Beta(1,1) → posterior Beta(8, 4)
   - Mode: 7/10 = 0.70
   - Credible interval: ~[0.45, 0.88]

2. **Skeptical prior**: Beta(10, 10) → posterior Beta(17, 13)
   - Mode: 17/30 ≈ 0.57
   - Credible interval: ~[0.43, 0.70]
   - Pulls toward 0.5 because prior said "coin is fair"

3. **Biased toward tails**: Beta(0.5, 0.5) → posterior Beta(7.5, 3.5)
   - Mode: 7.5/11 ≈ 0.68
   - Credible interval: ~[0.40, 0.92]
   - Wider uncertainty due to diffuse prior

**The prior matters when data is scarce.** With 7 heads in 10 flips, the prior still influences the posterior. But with 700 heads in 1000 flips, all three priors converge to essentially the same posterior.

### More Data → Narrower Posterior

Observe 70 heads in 100 flips (same frequency, more data):

- Uniform prior → posterior Beta(71, 31)
- Credible interval: ~[0.59, 0.79]

The posterior is sharper. The uncertainty shrinks as we collect more evidence.

### The Prior Washes Out

With enough data, the posterior becomes insensitive to the prior. The data dominates. This is **Bayesian consistency**: given enough evidence, different starting beliefs converge.

---

## The Theory

### Bayes' Theorem

At the heart of Bayesian inference is Bayes' theorem:

$$P(\theta \mid \text{data}) = \frac{P(\text{data} \mid \theta) \times P(\theta)}{P(\text{data})}$$

Breaking this down:

- **P(θ)**: Prior — your belief before seeing data
- **P(data | θ)**: Likelihood — probability of data given parameters
- **P(data)**: Marginal likelihood — probability of data averaged over all θ
- **P(θ | data)**: Posterior — your updated belief after data

Often we ignore the denominator (it's just a normalizing constant):

$$P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \times P(\theta)$$

### Conjugate Priors: When the Math Works Out

Some priors are **conjugate** to certain likelihoods: the posterior is the same family as the prior.

**Beta-Binomial conjugacy**: If you use a Beta prior and observe binomial data, the posterior is also Beta.

Specifically:
- Prior: Beta(α, β)
- Data: k successes in n trials
- Posterior: Beta(α + k, β + n - k)

This is magical: the posterior has a closed form. You can compute it exactly, no integration required.

### Point Estimates from the Posterior

The posterior is a full distribution, but sometimes you need a single number:

- **Posterior mean**: $\mathbb{E}[\theta \mid \text{data}]$
- **Posterior median**: 50th percentile
- **Maximum a posteriori (MAP)**: mode of the posterior

For Beta(8, 4), the mean is 8/12 ≈ 0.667.

### Credible Intervals

Frequentist 95% confidence intervals have a weird interpretation: "95% of hypothetical experiments would produce intervals containing the true parameter."

Bayesian **credible intervals** are more intuitive: "95% of the posterior probability is in this interval."

For the posterior, the 95% credible interval is simply the range containing 95% of the probability mass.

---

## Going Deeper

### Bayesian vs. Frequentist Thinking

These frameworks answer different questions:

**Frequentist**: "If the null hypothesis were true, what's the probability of seeing data this extreme?"
- Works with long-run frequencies
- Doesn't assign probability to fixed parameters (they're either true or not)
- Confidence intervals have awkward interpretation

**Bayesian**: "Given the data I observed, what posterior distribution should I have over parameters?"
- Works with prior knowledge + data
- Assigns probability to parameters as expressions of uncertainty
- Credible intervals are intuitive

Both are valid. Bayesian thinking is often more natural for updating beliefs with evidence.

### Hierarchical Models

Sometimes the prior itself is uncertain. This leads to **hierarchical models**:

$$P(\text{data} \mid \theta)$$
$$P(\theta \mid \phi)$$
$$P(\phi)$$

Example: You're measuring the bias of 10 coins. Each coin has its own θ_i, but they're not independent. They're drawn from a common prior:

$$\theta_i \sim \text{Beta}(\alpha, \beta)$$

And the hyperparameters (α, β) have their own prior:

$$\alpha, \beta \sim \text{some prior}$$

This allows the model to learn that some coins are fair (θ near 0.5) while others are biased, and to share information across coins.

---

## Real Data: Applications

### A/B Testing

You have two website designs (A and B). You measure conversion rates:

- Design A: 100 visitors, 12 conversions → 12%
- Design B: 100 visitors, 18 conversions → 18%

Is B better? By how much?

Bayesian approach:
1. Use a Beta(1,1) prior for each conversion rate
2. Update with data → posteriors for θ_A and θ_B
3. Estimate P(θ_B > θ_A) by sampling or integration
4. Also estimate the credible interval for the difference

The result is a full distribution of plausible differences, not just a p-value.

### Medical Diagnosis

You have a disease with base rate 1% and a test with 95% accuracy (both sensitivity and specificity).

You test positive. What's the probability you have the disease?

Bayes' theorem:

$$P(\text{disease} \mid \text{positive}) = \frac{P(\text{positive} \mid \text{disease}) \times P(\text{disease})}{P(\text{positive})}$$

$$= \frac{0.95 \times 0.01}{0.95 \times 0.01 + 0.05 \times 0.99} ≈ 0.16$$

Only 16%! The base rate is so low that even a "positive" test doesn't strongly indicate disease.

### Laplace and the Sun

Pierre-Simon Laplace (1749-1827) asked: "What's the probability the sun rises tomorrow?"

Given that the sun has risen for ~5000 years (roughly 1.8 million days), what's the posterior probability it rises tomorrow?

Using a Beta(1,1) prior:

$$P(\text{rises tomorrow}) = \frac{\text{successes} + 1}{\text{trials} + 2} = \frac{1.8M + 1}{1.8M + 2} ≈ 0.9999994$$

Extremely high, but not 1. There's a tiny but nonzero chance it doesn't (accounting for scientific uncertainty about stellar physics).

---

## Rabbit Holes

### Thomas Bayes and Richard Price

Thomas Bayes (1702-1761) was an English clergyman who developed a theorem about conditional probability. He never published it; his friend Richard Price edited and published it posthumously.

Bayes' work was largely forgotten until the 20th century. The "Bayesian" approach wasn't popular until computers made it practical.

### The Bayesian-Frequentist Wars

Throughout the 20th century, statisticians debated which framework was "correct." Frequentists dominated academic statistics for decades. The argument:
- Frequentist: "You can't assign probability to unknown parameters; parameters are fixed."
- Bayesian: "You must incorporate prior knowledge; ignoring it is pretending to be ignorant."

This wasn't just academic. It affected how research was conducted, how medical trials were designed, and which conclusions were publishable.

Modern trend: Both are tools. Use what makes sense for the problem.

### Bayesian Reasoning in Everyday Life

Your brain is a Bayesian inference engine:

- **Weather forecast**: You see dark clouds (data) and update your prior "sunny day" to "rain likely"
- **Spam filters**: Each word in an email (data) updates the filter's posterior "is this spam?"
- **Social reasoning**: You update your belief about someone's competence based on their actions

We constantly combine prior knowledge with observations. Bayes' theorem formalizes this.

---

## Summary

Bayesian thinking represents uncertainty as probability distributions.

**Key insights:**

1. **Before seeing data, you have a prior**: your starting belief encoded as a probability distribution.

2. **Data updates your belief**: use Bayes' theorem to combine prior and likelihood.

3. **The posterior is a distribution**: it expresses both the most plausible values and the remaining uncertainty.

4. **The prior matters when data is scarce**: with little evidence, your starting belief dominates. With lots of data, the posterior converges regardless of prior.

5. **Conjugate priors are convenient**: some prior-likelihood pairs have closed-form posteriors (like Beta-Binomial).

6. **Credible intervals are intuitive**: "95% of the posterior is in this interval" is what we actually mean.

This framework is powerful: it handles uncertainty naturally, incorporates prior knowledge, and updates gracefully with new evidence.

But there's a catch: computing posteriors is often intractable. With complex models and high-dimensional parameters, you can't integrate the likelihood function. You can evaluate it, but you can't compute the denominator in Bayes' theorem.

The solution is **Markov chain Monte Carlo**: a way to sample from intractable distributions. This is the bridge from elegant theory to practical computation.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Beta-Binomial posteriors, credible intervals, effect of priors
- Exploration: Sequential Bayesian updating, convergence with data
- Challenge: Medical diagnosis, A/B testing, hierarchical models
- Thought experiments: Objective priors, Bayesian reasoning in daily life
