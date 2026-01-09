# Chapter 15 Exercises: Populations

## Warm-up Exercises

**1. Simulate a birth-death process**

Use `simulations.py` to simulate a birth-death process with:
- n₀ = 5 (initial population)
- λ = 1.2 (birth rate)
- μ = 1.0 (death rate)
- t_max = 100 (time steps)

Run the simulation 1000 times. Count:
- How many runs go extinct (final population = 0)?
- What fraction go extinct?

Compare to the theoretical extinction probability: $p(\text{extinct}) = (\mu/\lambda)^{n_0}$

---

**2. Verify the branching process formula**

For λ = 1.2, μ = 1.0, the extinction probability from one individual is:

$$p_1 = \left(\frac{\mu}{\lambda}\right)^1 = \frac{1.0}{1.2} ≈ 0.833$$

For n₀ individuals, extinction probability is: $p_{n_0} = p_1^{n_0}$

Test this formula:
- Run 200 simulations for each n₀ ∈ {1, 5, 10, 20}
- Plot simulated extinction probability vs. theoretical

Does the formula work?

---

**3. Explore population trajectories**

Plot 50 trajectories of the same population with n₀=5, λ=1.2, μ=1.0, t_max=100.

Observe:
- What fraction go extinct before time 100?
- Among survivors, what's the range of final population sizes?
- Is the distribution of survivors skewed (few very large, many medium-sized)?

---

**4. Extinction vs. initial population size**

For λ = 1.2, μ = 1.0, compute extinction probability for:

$$n_0 \in \{1, 2, 5, 10, 20, 50\}$$

For each, run 100 simulations. Plot extinction probability vs. n₀.

Describe the relationship. How fast does extinction probability decrease as n₀ increases?

---

## Exploration Exercises

**5. Survival time distribution**

Among populations that eventually go extinct, how long do they typically survive?

For n₀=5, λ=1.2, μ=1.0:
- Run 100 simulations
- For each run that goes extinct, record the time to extinction
- Histogram the extinction times

Is extinction sudden or gradual? What does this tell you about management?

---

**6. Variance matters as much as mean**

Compare two scenarios with the same expected growth:

**Scenario A**: λ = 0.55, μ = 0.50 (low variance, growth = 0.05)
**Scenario B**: λ = 0.80, μ = 0.75 (high variance, growth = 0.05)

For each, compute extinction probability with n₀ = 5 and n₀ = 50.

Which has higher extinction probability? Why does variance matter?

---

**7. Environmental stochasticity**

Modify the simulation to include environmental variation:
- Some years, λ = 0.7, μ = 0.3 (good years)
- Other years, λ = 0.3, μ = 0.7 (bad years)
- Average: λ = 0.5, μ = 0.5 (neutral)

Compare extinction probability to a deterministic model where λ = μ = 0.5 always.

Does environmental variation increase extinction risk?

---

**8. Density-dependent population**

Implement logistic growth: as population n approaches carrying capacity K, growth slows.

Model: per-capita growth rate = r(1 - n/K)

With n₀ = 10, r = 0.5, K = 100:
- Run many simulations
- Plot final population distribution
- Compare to exponential growth (no density dependence)

How does density-dependence change outcomes?

---

## Challenge Exercises

**9. Allee effect**

An Allee effect means small populations have reduced birth and increased death:
- When n < n_critical, birth rate decreases, death rate increases
- Example: hard to find mates when rare

Simulate with and without Allee effect (critical size = 10):

For n₀ = 5, 10, 20, compute extinction probability in both cases.

How much does the Allee effect increase extinction risk?

---

**10. Metapopulation structure**

Simulate 5 patches, each with local dynamics (λ=0.6, μ=0.4, n₀=10).

Add migration: individuals move between patches with probability 0.05 per time step.

Measure:
- What fraction of patches go extinct?
- Does the total metapopulation persist even if individual patches die?
- How does migration rate affect persistence?

---

**11. Genetic drift**

Model a gene with two alleles: A and a. Each has frequency in [0,1].

At each generation, sample new allele frequencies from binomial:
- Allele A: $f'_A = \text{Binomial}(N, f_A) / N$

Start with $f_A = 0.5$. Run many simulations:
- Frequency of A over time (some rise to 100%, some drop to 0%)
- What fraction fix at each allele?

This is genetic drift: random changes in allele frequency in small populations.

---

**12. Minimum viable population (MVP)**

You want to ensure a population persists with probability > 95% for 100 generations.

Given λ = 1.2, μ = 1.0, what's the minimum initial population?

Run simulations for n₀ = 1, 2, 5, 10, 20 and measure:
- P(population exists at t=100)
- P(population > 50 at t=100)
- P(population > 100 at t=100)

What's the MVP for different target thresholds?

---

## Thought Experiments

**13. One large or many small?**

You have resources to protect either:
- **Option A**: One large population of 100 individuals
- **Option B**: Five populations of 20 individuals each

Same total (100 individuals), different structure.

Which strategy reduces overall extinction risk?

Simulate both with λ = 1.2, μ = 1.0 for 100 time steps.

---

**14. The passenger pigeon problem**

The passenger pigeon went from billions (1800s) to zero (1914).

Model: λ = 1.5 (high birth rate), but due to hunting, population crashes to n = 1000.

Suddenly, Allee effect becomes important: with so few birds, mating becomes hard.

Simulate with Allee effect (critical size = 10,000). What's the probability of recovery?

---

**15. Conservation triage**

You manage multiple endangered populations:
- Species A: n = 50, λ = 1.1, μ = 1.0
- Species B: n = 5, λ = 1.5, μ = 1.0 (higher growth but smaller)
- Species C: n = 10, λ = 0.9, μ = 1.0 (declining)

You can help one species. Which should you prioritize?

Compute 100-year extinction probability for each. Base your decision on probability of persistence vs. difficulty of intervention.

---

## Open-Ended Exploration

**Wright-Fisher model**

The Wright-Fisher model is the standard model in population genetics. In a population of size N:
- Random mating
- Discrete generations
- Each individual samples parent alleles from the population

Implement the Wright-Fisher model for a two-allele system. Track:
- Allele frequency over time
- Time to fixation (one allele reaches 100%)
- Compare theoretical results to simulation

---

**Stochastic logistic equation**

The stochastic analog of the logistic equation adds noise:

$$dn = r n (1 - n/K) dt + \sigma n dW$$

where dW is a Wiener process (continuous-time random walk).

This is a stochastic differential equation (SDE). Explore:
- How noise affects the stationary distribution
- Critical population size for extinction
- Relationship to the discrete birth-death model

---

**Spatial structure and dispersal**

Real populations are spread across space. Individuals move (disperse) to new locations.

Build a spatial model:
- 2D grid with patches
- Local birth-death dynamics in each patch
- Dispersal to neighboring patches

How does spatial structure affect extinction risk?
