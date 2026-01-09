# Chapter 15: Populations

## Why Small Populations Face Extinction Through Bad Luck

A species has 10 individuals left. Each year, each individual has a 60% chance of reproducing and a 40% chance of dying.

On average, each individual produces 1.5 offspring and dies at rate 0.4. The population should grow.

But run the simulation: extinction is common. Small populations live and die by luck.

This chapter explores stochastic population models—how randomness determines survival or extinction in growing, shrinking, and sometimes doomed populations.

---

## First Contact: The Birth-Death Process

The simplest population model has:
- **Birth**: each individual reproduces with probability λ per time unit
- **Death**: each individual dies with probability μ per time unit
- **Population size**: n individuals

At each time step:
- Each individual may be born (with probability λ)
- Each individual may die (with probability μ)

The population changes by: Δn = (births) - (deaths)

### Simulate It

```python
def birth_death_process(n0, lambda_birth, mu_death, t_max=100):
    n = n0
    time = 0
    history = [n]
    
    while time < t_max and n > 0:
        # Each individual has chance to reproduce or die
        births = binomial(n, lambda_birth)
        deaths = binomial(n, mu_death)
        
        n = n + births - deaths
        history.append(n)
        time += 1
    
    return history
```

Run this 100 times with n₀=10, λ=0.6, μ=0.4. Plot all trajectories:
- Some populations explode (reach 1000+)
- Most go extinct before time 100
- The distribution is highly skewed: survivors dominate; extinctions are common

### The Key Parameters

**Net growth rate per individual**: g = λ - μ

If g > 0, the population should grow (on average). If g < 0, it should shrink.

But individual randomness means:
- Even with g > 0, extinction is possible (and likely for small populations)
- Even with g < 0, the population might survive for a while (luck)

---

## Patterns Emerge

### Extinction Is Likely from Small Populations

For a population starting at n₀ individuals:
- If n₀ = 1: High extinction probability (unless birth rate >> death rate)
- If n₀ = 5: Still substantial extinction risk
- If n₀ = 50: Extinction becomes rarer
- If n₀ = 500: Extinction probability approaches deterministic prediction

**The smaller the initial population, the more likely it goes extinct.**

This is true even with positive expected growth (λ > μ).

### The Variance Matters

Two scenarios with the same average growth:
1. **Low variance**: λ = 0.5, μ = 0.49 (growth = 0.01, but stable)
2. **High variance**: λ = 0.8, μ = 0.79 (growth = 0.01, but volatile)

Both have expected growth 0.01 per individual. But:
- Low variance: steady growth, rarely goes extinct
- High variance: explosive growth OR crash and extinction

**Variability increases extinction risk.**

### Distribution of Final Population Is Skewed

Among survivors, populations often grow large. The distribution has:
- Many small populations
- Few large populations
- The distribution is not symmetric

This matters for conservation: protecting the "average" population may not protect the diversity.

---

## The Theory

### Birth-Death Process as Markov Chain

A **birth-death process** is a continuous-time Markov chain on population size:
- At each instant, the population can increase by 1 (birth), decrease by 1 (death), or stay the same
- Transition rates:
  - From n to n+1: rate λn (each of n individuals births at rate λ)
  - From n to n-1: rate μn (each of n individuals dies at rate μ)
  - From n to n: rate -(λ+μ)n (total exit rate)

### Expected Growth and Extinction

The expected change per individual per unit time is:

$$\mathbb{E}[\Delta n | n] = (λ - μ) \cdot n$$

If λ > μ, expected growth is positive. If λ < μ, expected decline.

But expected values mislead in stochastic systems. The question is: **what's the probability of extinction?**

### Extinction Probability

For a birth-death process starting from state n = 1, define:

$$p(\text{extinction}) = \text{probability that population eventually reaches 0}$$

**Key result** (from branching process theory):

If λ > μ:
$$p(\text{extinction} \mid n=1) = \left(\frac{\mu}{\lambda}\right)^n$$

And for larger initial populations:
$$p(\text{extinction} \mid n=n_0) = \left(\frac{\mu}{\lambda}\right)^{n_0}$$

**Example**: λ = 1.2, μ = 1.0:
$$p(\text{extinction} \mid n=1) = \left(\frac{1.0}{1.2}\right)^1 = 0.833$$

Even with 20% expected growth per individual, the probability of extinction from a single individual is 83%!

$$p(\text{extinction} \mid n=5) = 0.833^5 ≈ 0.41$$

Starting from 5 individuals, extinction probability is 41%.

### Branching Processes

A **branching process** is the discrete-time analog: at each generation, each individual produces offspring according to a fixed distribution.

Key theorem: A branching process goes extinct with probability 1 if and only if the expected number of offspring per individual is ≤ 1.

---

## Going Deeper

### Environmental Stochasticity vs. Demographic Stochasticity

**Demographic stochasticity**: randomness at the individual level. Each person independently reproduces or dies.

**Environmental stochasticity**: randomness in the environment. A drought or disease reduces birth rates or increases death rates for all individuals.

Example:
- Demographic: λ = 0.6 always, but births/deaths vary randomly
- Environmental: λ varies (0.4 some years, 0.8 others), same average

Environmental stochasticity is often more important for real populations and increases extinction risk.

### Density Dependence and Carrying Capacity

Real populations can't grow forever. They have a **carrying capacity** K:
- When population is small (n << K), growth is fast
- As population approaches K, growth slows
- Logistic growth: $dn/dt = r \cdot n \cdot (1 - n/K)$

In stochastic form, birth and death rates depend on population size:
- Birth rate decreases as n increases
- Death rate increases as n increases

This creates stable populations instead of unbounded growth.

### Allee Effects

In some populations, individuals do worse when rare. This is an **Allee effect**:
- At very small n, birth rate is low (hard to find mates, reduced cooperation)
- At very small n, death rate is high (vulnerable, inbreeding)

Allee effects dramatically increase extinction risk for small populations.

### Metapopulations

Many species exist as multiple populations (patches) connected by migration:
- Patch A: 50 individuals
- Patch B: 30 individuals
- Migration between patches

Each patch may go extinct, but others may recolonize:
- Equilibrium: some patches occupied, some empty
- Overall species persists even if individual patches go extinct

The question becomes: **which patches are critical to preserve?**

---

## Real Data: Conservation and Extinction

### Endangered Species Recovery

Modern conservation programs use population models to decide:
- How many individuals needed to ensure survival?
- Which populations are most important to protect?
- Should we prioritize one large population or multiple small ones?

Example: California condor (critically endangered)
- Minimum viable population (MVP): 500+ individuals
- Genetic diversity required: need to avoid inbreeding
- Breeding programs estimate extinction risk vs. time horizon

### Historical Extinctions

The **passenger pigeon**: from billions (19th century) to 0 (extinct 1914).
- Overhunting reduced population from ~3 billion to <1 million
- Once rare (< a few thousand), extinction became inevitable (Allee effect)
- Last bird died in captivity

The **Thylacine** (Tasmanian tiger): hunted to extinction by 1936.
- Very small final population (< 100) had high extinction risk
- Once extinct, no recovery possible

### Experimental Populations

Lab experiments on bacteria, yeast, and small animals (drosophila, mice) confirm theory:
- Small populations go extinct more often
- Extinction risk follows predicted branching process probabilities
- Environmental variation increases extinction risk

---

## Rabbit Holes

### Minimum Viable Population (MVP)

Conservation biologists ask: **how many individuals do we need to ensure long-term survival?**

Typical answers: 500-1000+ individuals, depending on:
- Birth and death rates
- Environmental variation
- Genetic factors (inbreeding depression)

This is controversial: MVP estimates often underestimate extinction risk.

### Genetic Drift: Evolution as a Branching Process

Each gene variant (allele) in a population is like a branching process:
- Chance mutations introduce new alleles
- Drift: random changes in allele frequency
- Eventually, drift leads to fixation (allele goes to 100%) or extinction (0%)

Even beneficial mutations can go extinct by drift if population is small. This is **the efficacy of selection vs. drift**.

### The Tragedy of the Commons

Population dynamics underlie resource management:
- Fishing: harvest rate vs. fish population growth
- Forestry: cut rate vs. forest regrowth
- Water: extraction vs. aquifer recharge

If harvest exceeds birth rate, population crashes.

---

## Summary

Stochastic population models reveal that **survival is not just about average growth rates**.

**Key insights:**

1. **Extinction is likely from small populations**: even with positive expected growth, small populations have substantial extinction probability.

2. **Variance matters**: high variability in birth/death rates increases extinction risk, independent of mean growth.

3. **Initial conditions determine outcome**: populations starting from 5 vs. 50 individuals have vastly different extinction probabilities.

4. **Luck dominates early dynamics**: early generations are critical. By luck, the population may be wiped out before it grows large.

5. **Structure shapes persistence**: metapopulations, connectivity, and environmental heterogeneity all affect long-term survival.

This is why conservation biologists care about more than just reproduction rates. They care about population size, variability, and structure.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Simulate birth-death process, estimate extinction probability
- Exploration: How extinction probability varies with initial population size and birth/death rates
- Challenge: Environmental stochasticity, density dependence, Allee effects
- Thought experiments: Conservation strategy tradeoffs, metapopulation management
