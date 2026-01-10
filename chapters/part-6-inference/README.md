# Part 6: Inference

## From Data to Belief

We've built models, but real data is messy, incomplete, and noisy. How do we learn from it?

Inference is the inverse of simulation. You observe data and ask: what underlying parameters generated this? Bayesian inference gives us a principled way to combine what we knew before (priors) with what we've observed (likelihood) to form new beliefs (posteriors).

In Part 6, we introduce Bayesian thinking, learn the powerful MCMC algorithms for sampling from intractable distributions, and see how to fit complex models to real data. By the end, you'll have the tools to turn data into quantified uncertainty—to say not just "here's our best guess" but "we're 95% confident the true value is in this range."

---

## Chapters in Part 6

1. **[Chapter 16: Thinking in Distributions](16-thinking-in-distributions/README.md)**
   - Bayesian reasoning: combining prior and data
   - From point estimates to credible intervals
   - How priors matter when data are scarce
   - A/B testing and posterior distributions

2. **[Chapter 17: Markov Chain Monte Carlo](17-markov-chain-monte-carlo/README.md)**
   - The Metropolis-Hastings algorithm
   - Constructing chains whose stationary distribution is the posterior
   - Proposal distributions and acceptance rates
   - Convergence diagnostics: trace plots, R-hat, effective sample size
   - The multimodal challenge: when chains get stuck

3. **[Chapter 18: Fitting Models to Messy Data](18-fitting-models-to-messy-data/README.md)**
   - The Bayesian workflow: prior → likelihood → posterior
   - Posterior predictive checks: simulating fake data to validate models
   - Change point detection and model comparison
   - From theory to practice with real data

---

**Previous:** [← Part 5: Modeling](../part-5-modeling/README.md)

---

## The Journey Completes Here

You've traveled from intuition through simulation to inference. You now understand:
- How randomness *works* and how our brains misinterpret it
- How to model complex systems with randomness
- How to learn from data using probability
- How to quantify uncertainty in everything you do

The journey doesn't end here—it's just beginning. Every field from finance to biology to machine learning uses these tools. The randomness you've learned to see and model is everywhere.
