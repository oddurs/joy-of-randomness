# Chapter 16 Exercises: Thinking in Distributions

## Warm-up Exercises

**1. Beta-Binomial posteriors by hand**

A coin lands heads 7 out of 10 times. Use a Beta(1,1) prior.

- What's the posterior distribution?
- Compute the posterior mean
- Compute the posterior mode

Remember: Beta-Binomial conjugacy means posterior is Beta(α + k, β + n - k).

---

**2. Credible intervals**

For the same coin (7 heads in 10 flips, Beta(1,1) prior):

- Compute the 95% credible interval
- Compute the 50% credible interval (interval containing 50% of the posterior mass)

Use the cumulative distribution function or numerical methods. Compare to the theoretical values.

---

**3. Effect of different priors**

Same data (7 heads in 10 flips), three different priors:

1. **Uniform**: Beta(1, 1)
2. **Skeptical**: Beta(10, 10) (strong prior toward heads = tails)
3. **Extreme**: Beta(0.5, 0.5) (concentrated at extremes)

For each prior:
- Compute the posterior distribution
- Compute the posterior mean
- Compare the 95% credible intervals

How much do the posteriors differ? Which prior pulls the most toward 0.5?

---

**4. More data, less uncertainty**

With the Uniform prior:

Scenario A: 7 heads in 10 flips
Scenario B: 70 heads in 100 flips (same frequency, more data)

For each:
- Compute posterior mean
- Compute posterior variance
- Compute credible interval width

How does the posterior narrow as we accumulate data?

---

## Exploration Exercises

**5. Sequential Bayesian updating**

Use `simulations.py` to implement sequential updating. Start with Beta(1,1) prior. Then observe a sequence of coin flips: H, T, H, H, T, H, H, H, H, T.

- Plot the posterior after each flip
- Show how the posterior evolves from the prior to final posterior
- Compare to updating all at once

Does the order of observations matter? (No, Bayes' theorem is order-invariant.)

---

**6. Prior convergence with data**

Use three very different priors:
- Beta(1, 1) (uniform)
- Beta(100, 1) (strong bias toward heads)
- Beta(1, 100) (strong bias toward tails)

For each, observe data: 50 heads in 100 flips.

Plot the three posteriors on the same graph. How close are they? Now observe 500 heads in 1000 flips. Are they converging?

This demonstrates **Bayesian consistency**: given enough data, the prior washes out.

---

**7. Credible intervals vs. confidence intervals**

A frequentist 95% confidence interval is awkward: "if we repeated the experiment infinitely, 95% of hypothetical intervals would contain the true parameter."

A Bayesian 95% credible interval is intuitive: "95% of the posterior probability is in this interval."

For the coin (7 heads in 10):
- Compute the 95% Bayesian credible interval
- Compare to a frequentist confidence interval (use binomial.interval or scipy)

Do they agree? Why or why not?

---

**8. Posterior predictive distribution**

After observing data, you want to predict the next flip.

The **posterior predictive distribution** is the probability of future observations, averaging over uncertainty in the parameter:

$$P(\text{next flip = heads} \mid \text{data}) = \int P(\text{heads} \mid \theta) P(\theta \mid \text{data}) d\theta$$

For Beta posterior, this has a closed form: (α_posterior) / (α_posterior + β_posterior).

For 7 heads in 10 flips (Beta(1,1) prior → Beta(8,4) posterior):
- Compute P(next flip = heads)
- Compare to the MLE (0.7) and the posterior mean (0.67)

---

## Challenge Exercises

**9. Bayesian A/B testing**

You run an A/B test:
- Variant A: 150 visitors, 18 conversions
- Variant B: 150 visitors, 24 conversions

Use Beta(1,1) priors for both conversion rates.

Compute:
1. The posterior distribution for each variant
2. P(conversion_B > conversion_A) — probability that B is better
3. 95% credible interval on the difference

Is the difference "significant"? Why is this cleaner than a frequentist p-value?

---

**10. Medical diagnosis Bayes**

A disease has base rate 1%. A test has 95% sensitivity (catches 95% of diseased) and 90% specificity (correctly identifies 90% of healthy).

You test positive. What's P(disease | positive)?

Now compute this for different base rates (0.1%, 1%, 5%, 10%) and plot how the posterior probability varies with prevalence.

Key insight: Low base rates make positive tests less informative.

---

**11. Hierarchical Bayesian model**

You measure the bias of 10 coins. Each coin has its own θ_i, but they're related:

$$\theta_i \sim \text{Beta}(\alpha, \beta)$$

All coins share hyperparameters (α, β), which are uncertain.

Observe:
- Coin 1: 8 heads, 10 flips
- Coin 2: 2 heads, 10 flips
- Coins 3-10: 5 heads, 10 flips each

Without hierarchical structure, you'd estimate each coin independently. But the hierarchical model lets coins share information: knowing Coin 2 is biased toward tails informs the prior for Coin 1.

Implement a simple version:
- Use a fixed hyperprior on (α, β)
- Compute posteriors for each coin
- Compare to independent posteriors

Do the coins influence each other?

---

**12. Updating with outliers**

You measure the height of 100 people. Most data is "reasonable" (150-190 cm), but one measurement is 250 cm (outlier).

With a Bayesian model:
- Normal likelihood with unknown mean and variance
- Priors on mean and variance

How much does the outlier affect the posterior mean? Compare to frequentist methods (e.g., flagging outliers).

---

## Thought Experiments

**13. Objective priors?**

Some argue for "objective" priors that are "uninformative" or "neutral."

Examples:
- Uniform prior: all parameter values equally likely
- Jeffreys prior: scale-invariant, doesn't depend on parameterization

But is any prior truly uninformative? A uniform prior on [0,1] is different from a uniform prior on log-odds.

Think about:
- Is the Uniform prior really uninformative?
- Should different coin bias values have different prior probability?
- How would you define "objective"?

---

**14. Laplace's sunrise problem**

Laplace asked: "Given that the sun has risen for ~5000 years, what's the probability it rises tomorrow?"

With a Beta(1,1) prior and 1.8 million successes (days the sun rose):

$$P(\text{tomorrow}) = \frac{1.8M + 1}{1.8M + 2} ≈ 0.9999994$$

High but not 1. This is actually sensible:
- It accounts for unknown unknowns
- As evidence accumulates, probability approaches 1

What would Laplace say about modern concerns (e.g., asteroid impacts)?

---

**15. Bayes in daily life**

Your brain continuously updates beliefs:

1. **Weather**: You see dark clouds → update P(rain) from prior to posterior
2. **Social**: Friend is late → update belief about their reliability
3. **Health**: You feel a symptom → update P(sick) using base rate

For one scenario (your choice):
- State the prior (your initial belief)
- Identify the data (new information)
- Estimate the posterior (updated belief)
- Use Bayes' theorem to quantify the update

How does this formalize intuitive reasoning?

---

## Open-Ended Exploration

**Empirical Bayes**

Instead of choosing a prior, let the data inform it. **Empirical Bayes** estimates the prior (hyperparameters) from observed data.

Example: You measure 10 coins. Instead of assuming all come from Beta(10,10), estimate the (α, β) that best explains the observed frequencies.

Implement:
1. Observe coin biases (e.g., frequencies for 10 coins)
2. Fit Beta hyperparameters using maximum likelihood
3. Use fitted Beta as prior for a new coin

How does this compare to a fixed hierarchical prior?

---

**Information content**

The **entropy** of a distribution measures how much uncertainty it contains:

$$H[P] = -\int P(x) \log P(x) dx$$

For a Beta distribution, entropy can be computed in closed form.

Explore:
- How does entropy change as you update from prior to posterior?
- Compare entropy across different priors
- Interpret entropy as "information gained" by the data

---

**Bayes factor**

Instead of computing posteriors, sometimes you compare models. The **Bayes factor** is the ratio of likelihoods:

$$\frac{P(\text{data} \mid \text{model A})}{P(\text{data} \mid \text{model B})}$$

For the coin problem:
- Model A: θ ~ Beta(1,1) (coin can be any bias)
- Model B: θ = 0.5 (coin is fair)

Compute the Bayes factor for 7 heads in 10 flips. Does the data favor A or B?
