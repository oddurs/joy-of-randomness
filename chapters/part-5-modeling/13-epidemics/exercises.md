# Chapter 13 Exercises: Epidemics

## Warm-up Exercises

**1. Implement stochastic SIR**

Use the code from `simulations.py` to implement a stochastic SIR model with:
- N = 1000 (population)
- β = 0.3 (transmission rate)
- γ = 0.1 (recovery rate)
- I₀ = 1 (initial infection)
- t_max = 100 (days)

Run the model 50 times. Plot all 50 epidemic curves on a single graph.

Also plot the deterministic SIR solution on the same graph. How do the stochastic runs compare?

---

**2. Early extinction probability**

For the parameters above (R₀ = 3), compute:

- What fraction of 1000 stochastic runs go extinct (I = 0) before day 20?
- For those that don't go extinct by day 20, what fraction end up with major outbreaks (>10% infected)?

This shows how early randomness is critical.

---

**3. Compare population sizes**

Run stochastic SIR with β = 0.3, γ = 0.1 for populations N = 100, 500, 1000, 5000.

For each, run 100 simulations and compute:
- Average final size (R/N at the end)
- Fraction with "major outbreak" (final R > 10% of N)
- Variability (std dev of final R across runs)

Plot these quantities vs. N. What pattern do you see?

---

**4. Extinction and R₀**

For fixed N = 1000, vary R₀ and compute extinction probability:

```python
R0_values = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]
```

For each R₀:
- Run 100 stochastic simulations
- Fraction of runs with major outbreak

Plot the results. Is there a sharp threshold at R₀ = 1? How sharp?

---

## Exploration Exercises

**5. Deterministic vs. stochastic comparison**

For a given β and γ, solve the deterministic SIR and plot the I(t) trajectory.

Then run the stochastic model 100 times on the same graph.

Observations:
- Do the stochastic runs have higher or lower peak than deterministic?
- Do they converge as N increases?
- Why would they diverge?

---

**6. Branching process approximation**

The branching process is a good model for early outbreak dynamics.

In a branching process, each infected person infects 0, 1, 2, ... others, with mean R₀.

Theory: extinction probability from a single person ≈ 1/R₀ (if R₀ > 1).

**Test this:**
1. Run SIR starting from I=1 for various R₀
2. Record: fraction that go extinct before reaching I=100
3. Compare to 1/R₀

How good is the approximation?

---

**7. Seasonality and recurrent outbreaks**

Add seasonality to the transmission rate: β(t) = β₀(1 + α sin(2πt/365)).

Run the SIR model with different amplitude α. Observe:
- Do outbreaks become more regular?
- Does the variation between years decrease?
- How does this compare to data?

---

**8. Effect of initial condition**

Fix β, γ, N. Vary I₀ (initial infections) from 1 to 10.

For each:
- Run 100 stochastic simulations
- Record P(major outbreak)

Does P(major outbreak) increase with I₀? By how much?

This tests: how many initial infections are needed to reliably seed a pandemic?

---

## Challenge Exercises

**9. Superspreaders: impact on outbreak probability**

Implement the superspreader version: 10% of infected cause 80% of transmissions.

For a given β and γ:
- Run 100 simulations without superspreaders
- Run 100 simulations with superspreaders
- Compare P(major outbreak) in both cases

Does superspreading increase or decrease outbreak probability? Why?

---

**10. Heterogeneity in transmission**

Generalize: let transmission rate β vary between infected individuals, drawn from a distribution.

Examples:
- β ~ exponential (most infect few, some infect many)
- β ~ normal (most infect average amount)
- β ~ bimodal (distinct "superspreader" and "normal" groups)

For each distribution, run 100 simulations and compare P(major outbreak).

How sensitive is the result to the distribution of β?

---

**11. SEIR model (with exposed period)**

Add an **E** (Exposed) compartment:

$$S \to E \to I \to R$$

with:
- σ: rate of progression E → I (incubation period ~ 1/σ)
- γ: recovery rate I → R

Implement stochastic SEIR. Compare to SIR with the same effective R₀.

How does the extra compartment change epidemic dynamics?

---

**12. Network effects**

Build a contact network:
- N = 1000 individuals
- Each individual has k = 5 contacts on average
- Edges: random or clustered (friends of friends)

Simulate disease spread on the network:
- Disease transmits along edges only
- Compare to well-mixed SIR

How much does network structure slow down epidemics?

---

## Thought Experiments

**13. Branching process extinction**

A branching process starts with 1 infected. Each infected person infects X others, where X ~ Poisson(R₀).

Theory: extinction probability = (smallest root of generating function) ≈ 1/R₀.

**Verify this:** 
- Simulate the branching process for various R₀
- Estimate extinction probability
- Compare to 1/R₀

---

**14. Critical community size**

Measles has R₀ ≈ 15 (highly contagious). A vaccine prevents measles.

In an island community with N = 5,000 people, suppose vaccination covers 95% of children.

What's the R₀ in the vaccinated population? Will measles persist or go extinct?

(Hint: vaccinated people are effectively removed from the susceptible pool.)

---

**15. Public health policy dilemma**

You're a public health official. Two policies:

**Policy A:** Reduce transmission by 30% (e.g., hand hygiene campaign)
- Cost: $1 million
- Effect: β → 0.7β

**Policy B:** Increase testing and isolation; remove infecteds faster
- Cost: $1 million  
- Effect: γ → 2γ (faster recovery / removal)

Which policy reduces P(major outbreak) more? Which is more cost-effective?

Simulate both scenarios with baseline (β, γ) and measure the impact on R₀ and outbreak probability.

---

## Open-Ended Exploration

**Fitting real epidemic data**

Find a real epidemic dataset (e.g., measles in a country, COVID-19 data, historical flu).

1. Estimate β and γ by fitting the SIR model to data
2. Compute R₀
3. Run stochastic simulations with your fitted parameters
4. Compare simulated outbreaks to real data

What aspects of the data does SIR capture? What does it miss?

---

**Agent-based model**

Build an agent-based model:
- N individuals, each with a location (x, y)
- Disease transmits between nearby individuals
- Individuals move randomly

Compare to well-mixed SIR. How much do spatial effects matter?

---

**Multi-strain dynamics**

Suppose two strains of a disease coexist: Strain A (R₀ = 2) and Strain B (R₀ = 3).

- Recovering from A confers immunity to A but not B (and vice versa)
- Cross-immunity: partial (50%)

How do the two strains interact? Does one exclude the other?

This connects to real scenarios: flu strains, COVID variants, etc.
