# Chapter 8 Exercises: Chains Everywhere

## Warm-up Exercises

**1. Implement and simulate a weather model**

Using the weather transition matrix from the chapter (or create your own):

```python
P = np.array([[0.7, 0.2, 0.1],
              [0.25, 0.5, 0.25],
              [0.1, 0.4, 0.5]])
```

Simulate 365 days of weather starting from "Sunny". Print out the first 30 days. What patterns do you notice?

---

**2. Compute the stationary distribution**

Using the same weather model, compute the stationary distribution π such that πP = π.

Compare it to the long-run frequencies from your simulation (simulate 10,000 days and count the fraction of each state). Do they match?

---

**3. Weather model fitting**

Given a sequence of observed weather (as a string: "SSCRRCSS..."), fit a Markov model by counting transitions.

```python
observed_weather = "SSSCRRCSSCRRCCRSSCRRCSS..."  # 100 days or so
```

Extract the transition matrix from this data and compare your fitted model to the "true" model from Exercise 2.

---

## Exploration Exercises

**4. Chutes and Ladders: Expected game length**

Implement the Chutes and Ladders game as a Markov chain (or simulate it directly). Play 10,000 games starting from position 0. What's the average number of turns to reach position 100 (and win)?

Compare this to the theoretical expectation (if you can compute it).

---

**5. Chutes and Ladders: Most visited squares**

In your 10,000 simulations, count how many times you land on each square. Which squares are visited most? Which are visited least?

Plot a histogram of visit frequencies. Do you notice patterns (e.g., do certain squares always cluster)?

---

**6. DNA Evolution**

Start with a DNA sequence "ATGATGATGATG" (12 nucleotides). Apply the mutation Markov chain with mutation_rate = 0.01 for 100 generations.

Plot the **Hamming distance** (number of differing nucleotides) from the initial sequence vs. generation. Does it grow linearly? Logarithmically? Plateau?

---

**7. Mutation rate effects**

Repeat Exercise 6 with mutation rates of 0.001, 0.01, 0.05, and 0.1. How does the mutation rate affect the speed of divergence?

Can you find a formula relating mutation rate to expected Hamming distance after *n* generations?

---

## Challenge Exercises

**8. High-order transitions in weather**

The Markov weather model assumes independence. But what if today's weather depends on *both* yesterday and today?

Build a second-order model where the state is (yesterday's weather, today's weather), and the transition gives tomorrow's weather.

Compare this to the first-order model: does the second-order model capture more realism?

---

**9. Fitting a real-world dataset**

Find a weather dataset (e.g., NOAA, WeatherUnderground, or create synthetic data). Extract the weather states (Sunny/Cloudy/Rainy or more granular).

Fit a Markov model to the data. Compare the stationary distribution to the observed frequencies. How well does the model capture reality?

---

**10. Chutes and Ladders: Optimal strategy?**

The standard game is deterministic (you must roll and move). But imagine you could choose to roll now or later.

Does this change the expected time to win? (Hint: it shouldn't matter because rolls are independent and positions are deterministic.)

Now imagine you could choose which die to roll (a standard die, or a die with faces [1,1,2,3,4,5]). How would this affect your winning probability?

---

**11. DNA: CpG islands**

In many organisms, the transition C→G is suppressed (it's methylated and often mutates to something else). Model this by changing the mutation matrix:

```
From C: [μ, μ, 0.1μ, 1-3μ]  # G is suppressed
```

Fit this model to a sequence with a known CpG island and show that you can detect it by fitting transition matrices to windows of the sequence.

---

**12. M/M/1 Queue: Stability**

Simulate an M/M/1 queue with arrival_rate = 0.8 and service_rate = 1.0 (stable).

Then simulate with arrival_rate = 1.2 and service_rate = 1.0 (unstable—queue grows without bound).

Plot the queue length over time for both. How long before the unstable queue becomes impractical?

---

**13. M/M/1 Queue: Sensitivity**

For an M/M/1 queue with service_rate = 1.0, plot the expected queue length as arrival_rate varies from 0.1 to 0.99.

Notice the asymptote as arrival_rate → service_rate. This is why queuing systems need "spare capacity."

---

## Thought Experiments

**14. Long-range dependence**

The Markov weather model can't capture seasonality (summer ≠ winter).

Design a *non-Markovian* weather model that does capture seasonality. How would you need to change the framework? (Hint: add more state variables, not more history.)

---

**15. When do Markov chains fail?**

For each system below, decide whether a Markov chain is a good model. Explain your reasoning:

1. **Traffic flow on a highway**: Is today's traffic independent of yesterday's traffic?
2. **Stock prices**: Does tomorrow's price depend only on today's price?
3. **Conversations**: Does the next word you say depend only on the last word?
4. **Heartbeats**: Does the interval to the next beat depend only on the last interval?
5. **Websites**: Does the next page a user visits depend only on the current page?

For each "no," describe what additional structure you'd need to add.

---

## Open-Ended Exploration

**Modeling a custom system as a Markov chain**

Pick any system you find interesting:
- A board game
- A biological process (protein folding, gene expression)
- A social system (friend networks, communication patterns)
- A physical system (particle diffusion, molecular dynamics)

1. Define the states
2. Define the transition probabilities (from data, physics, or intuition)
3. Simulate the system
4. Compute the stationary distribution
5. Compare simulations to reality

Write up your findings and explain why (or why not) a Markov chain is appropriate.

---

**Markov chains in your field**

Is there a domain where Markov chains are used (even if you didn't realize it)?

Examples:
- Biology: Hidden Markov models for gene prediction
- Finance: Regime-switching models for market states
- NLP: Markov models for autocomplete and spam detection
- Robotics: Markov decision processes for planning
- Operations: Queuing models for scheduling

Find a paper or resource about Markov chains in your field and explain the application to someone unfamiliar with it.
