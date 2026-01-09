# Chapter 8: Chains Everywhere

## The Surprising Ubiquity of Memoryless Transitions

The same mathematics that generates fake Shakespeare can predict tomorrow's weather, model the evolution of DNA, and tell you how long you'll wait in line at the coffee shop. This chapter explores the breadth of Markov chains—showing that this simple idea (the future depends only on the present, not the past) shows up everywhere.

---

## First Contact: A Weather Model

Let's start simple. Imagine three weather states: **Sunny**, **Cloudy**, **Rainy**.

On a sunny day:
- 70% chance it stays sunny tomorrow
- 20% chance it becomes cloudy
- 10% chance it rains

On a cloudy day:
- 25% chance it clears to sunny
- 50% chance it stays cloudy
- 25% chance it rains

On a rainy day:
- 10% chance it clears directly to sunny
- 40% chance it becomes cloudy
- 50% chance it stays rainy

This is a **transition matrix** P:

```
       Tomorrow's State
       Sunny  Cloudy  Rainy
Today
Sunny   0.7    0.2     0.1
Cloudy  0.25   0.5     0.25
Rainy   0.1    0.4     0.5
```

To simulate weather, you just follow the rows:

```python
import numpy as np

P = np.array([[0.7, 0.2, 0.1],
              [0.25, 0.5, 0.25],
              [0.1, 0.4, 0.5]])

states = ['Sunny', 'Cloudy', 'Rainy']
current_state = 0  # Start sunny

weather_sequence = [current_state]
for day in range(365):
    # Sample the next state
    next_state = np.random.choice(3, p=P[current_state])
    weather_sequence.append(next_state)
    current_state = next_state

# Print a month
print(' '.join(states[i] for i in weather_sequence[:30]))
```

Output might be:
> Sunny Sunny Sunny Cloudy Rainy Rainy Cloudy Sunny Sunny Cloudy Rainy Cloudy Cloudy Sunny...

This looks vaguely like real weather: sunny days cluster together, rain comes and goes, there's a natural rhythm.

---

## Patterns Emerge: The Markov Tradeoff

The weather model is powerful—it captures a few important patterns:

1. **Persistence**: Sunny days tend to follow sunny days (0.7 → 0.7 is high)
2. **Typical proportions**: Over a long time, we see roughly the right fraction of each state
3. **Transitions**: We see weather changes at realistic frequencies

But it misses just as much:

1. **Seasonality**: In reality, summer is sunnier, winter is rainier—but our model has fixed transition probabilities
2. **Autocorrelation**: Rainy periods cluster (heavy rain systems), but our model doesn't capture multi-day memory
3. **Extreme events**: Rare events (snow, hurricanes) aren't in the model
4. **Causation**: The model ignores pressure systems, jet streams, and all the physics

This is the fundamental **Markov tradeoff**: you get simplicity (a single matrix), but you lose fidelity. The question is always: is it worth it?

---

## The Theory: Transition Matrices and Stationary Distributions

Let's formalize this. A **Markov chain** on a finite state space has:

- **States**: S = {s₁, s₂, ..., sₖ}
- **Transition matrix**: P where Pᵢⱼ = P(next state = sⱼ | current state = sᵢ)
- **Constraint**: Each row sums to 1 (probabilities from each state sum to 1)

Starting from state $i$, the probability of reaching state $j$ in exactly $n$ steps is given by the $(i, j)$ entry of $P^n$.

For example, with the weather matrix:

```python
P2 = P @ P  # Matrix multiplication

# P2[0, 0] = P(Sunny → Sunny in 2 steps)
#          = P(S→S→S) + P(S→C→S) + P(S→R→S)
#          = (0.7)(0.7) + (0.2)(0.25) + (0.1)(0.1)
#          = 0.49 + 0.05 + 0.01
#          = 0.55
```

### Stationary Distribution

As time goes on, something interesting happens. Compute $P^{100}$, then $P^{1000}$. Every row converges to the same vector:

```
π ≈ [0.44, 0.33, 0.23]
```

This is the **stationary distribution**. It has a magical property: $πP = π$.

What does this mean? If today's weather follows the stationary distribution (44% sunny, 33% cloudy, 23% rainy), then tomorrow's weather will *also* follow the same distribution.

Over the long run, the weather settles into this distribution regardless of where you started. Started on a rainy day? After 1000 days, you'll see roughly 44% sunny, 33% cloudy, 23% rainy. The chain "forgets" where it began.

---

## Going Deeper: The Properties of Markov Chains

### Detailed Balance and Reversibility

Some Markov chains are **reversible**: they look the same forwards and backwards in time.

For a weather chain, detailed balance means:

$$\pi_i P_{ij} = \pi_j P_{ji}$$

In words: the probability of flowing from state $i$ to state $j$ equals the flow from $j$ to $i$ in equilibrium.

This is true for our weather model (you can verify it), which means the chain is reversible. If you ran a video of the weather sequence backwards, the transition frequencies would look the same!

### Absorbing States

Some chains have **absorbing states**—states you can't leave:

```
P = [[1,    0],    # State 0: absorbing (can only loop to itself)
     [0.5,  0.5]]  # State 1: transient (can reach state 0)
```

Starting from state 1, you eventually reach state 0 and get stuck forever. The mean time to absorption is finite, but once absorbed, you're done.

**Real example**: Modeling bankruptcy. States are capital levels, and zero capital is absorbing.

### Periodicity

Some chains **cycle**:

```
P = [[0,    1],
     [1,    0]]
```

State 0 → State 1 → State 0 → State 1 → ... Every other step, you're guaranteed to be in state 0. This chain is **periodic with period 2**.

The weather model has period 1 (it's aperiodic) because from any state, you can reach it again in both even and odd numbers of steps.

### Ergodicity

A chain is **ergodic** if it's:
1. Irreducible (you can reach any state from any other state)
2. Aperiodic (not periodic)

For ergodic chains, a beautiful result holds: the time-average equals the ensemble-average.

That is, if you simulate one long path, the fraction of time spent in state $i$ equals $\pi_i$. And if you simulate 1000 independent starting points and look at the average, you again get $\pi_i$.

---

## Real Data: Four Applications

### 1. Weather Modeling

Real weather data: sunny (S), cloudy (C), rainy (R) for each day in 2023.

Sequence: S S S C C R R C S S C R R R C R C S S ...

You can **fit** a Markov model by counting transitions:
- Count how many times S is followed by S, C, or R
- Divide by total S occurrences

```python
# Real data
weather_data = "SSCCRRCSSCRRRCRCS..."

# Count transitions
transitions = defaultdict(lambda: defaultdict(int))
for i in range(len(weather_data) - 1):
    current = weather_data[i]
    next_state = weather_data[i+1]
    transitions[current][next_state] += 1

# Normalize to get probabilities
P_fitted = {}
for state, counts in transitions.items():
    total = sum(counts.values())
    P_fitted[state] = {s: c/total for s, c in counts.items()}
```

Then **compare**: does the simulated weather match real weather statistics?

### 2. Chutes and Ladders (Snakes and Ladders)

The board game can be modeled as a Markov chain with 100 states (positions on the board). From each position:
- Roll a die (uniformly 1–6)
- Move forward that many squares
- Check for chutes and ladders

The **state space** is positions 0–100, with position 100 as absorbing (you win).

Key questions:
- What's the expected number of rolls to finish? (First passage time)
- Which squares are visited most? (Long-run stationary distribution before reaching 100)
- What's the probability of finishing in exactly 15 rolls? (n-step transition probabilities)

The chain is finite, irreducible (you can reach any square), and absorbing (100 is absorbing). So from any starting position, you eventually reach 100 with probability 1.

### 3. DNA Mutation

DNA sequences consist of four nucleotides: A, T, G, C. Over evolutionary time, mutations cause substitutions.

A simple model: each position mutates independently with some probability per generation, uniformly to one of the other three nucleotides.

Position by position is a 4-state Markov chain:

```
P = [[1-3μ,  μ,    μ,    μ  ],     # From A
     [μ,     1-3μ, μ,    μ  ],     # From T
     [μ,     μ,    1-3μ, μ  ],     # From G
     [μ,     μ,    μ,    1-3μ]]    # From C
```

The stationary distribution is uniform: each nucleotide appears 25% of the time in the long run, regardless of the starting sequence.

This is used to:
- Estimate divergence time between sequences
- Detect CpG islands (regions where C→G mutations are suppressed)
- Build hidden Markov models for gene prediction

### 4. The M/M/1 Queue

A queue with:
- **M**emoryless arrivals (Poisson process): customers arrive at rate λ
- **M**emoryless service (exponential): service takes exponentially distributed time, rate μ
- **1** server

The state is the number of customers in the system. Transitions:
- From state $n$: go to $n+1$ with rate λ (arrival) or $n-1$ with rate μ (service completion)

In discrete time, the transition probabilities depend on λ and μ. The stationary distribution is geometric:

$$\pi_n = (1 - \rho) \rho^n \quad \text{where} \quad \rho = \frac{\lambda}{\mu}$$

- If $\rho < 1$ (arrivals slower than service): the queue stabilizes
- If $\rho ≥ 1$ (arrivals faster than or equal to service): the queue grows without bound

The **average wait time** in an M/M/1 queue is:

$$W = \frac{1}{\mu - \lambda}$$

This is one of the most important formulas in operations research. It tells you how many cashiers you need in a store, how many servers you need in a data center, etc.

---

## Going Deeper: Why Markov Chains Work (and When They Don't)

The Markov property—"the future depends only on the present"—is powerful because:

1. **Tractability**: You only need to store the current state, not history
2. **Scalability**: Matrix operations are fast and parallelizable
3. **Theory**: Stationary distributions, absorption times, and other properties have closed-form formulas
4. **Generality**: The same framework applies to weather, genetics, queues, and more

But the Markov property also has limits. Real systems often have:

- **Long-range dependence**: Tomorrow's weather depends on patterns from weeks ago (El Niño, jet streams)
- **Hidden structure**: You observe outputs but don't fully understand the state space (audio recordings, time series)
- **Nonlinearity**: The rules change (markets crash, diseases spread faster with variant strains)
- **Multiscale dynamics**: Different processes operate at different timescales

When these limitations matter, you need something more powerful. Two extensions:

1. **Higher-order Markov chains**: "The future depends on the present *and* recent past"
2. **Hidden Markov models**: You observe one sequence but a hidden Markov chain generates it

These preview more advanced tools you'll see later.

---

## Rabbit Holes

### The Ehrenfest Urn Model

In 1907, Paul and Tatiana Ehrenfest invented a physical model of Markov chains: two urns with $N$ balls, each labeled 1 to $N$. At each step:
1. Pick a random number from 1 to $N$
2. Move the ball with that number to the other urn

The state is the number of balls in urn 1. This simple model helped them understand diffusion and the second law of thermodynamics.

It's still used in physics simulations today.

### Google's Billions-of-States Markov Chain

In 1998, Google's founders realized that the web is a Markov chain where:
- States are webpages
- Transitions are links
- A random walk explores the web

The long-run frequency distribution is PageRank—the ranking that made Google. Billions of states, one simple principle. See Chapter 9 for the full story.

### Markov Chains in Baseball

Baseball at-bats can be modeled as a Markov chain (or more realistically, a hidden one). States might be:
- Ball count (0–3)
- Strike count (0–2)
- Runners on base (8 combinations)

The transition probabilities depend on the batter and pitcher. By fitting these models to real data, you can:
- Predict the outcome of an at-bat
- Simulate future games
- Understand strategic decisions (when to steal, when to pitch aggressive)

It's a deeper application than most people realize!

---

## Summary

Markov chains are everywhere. Whether modeling weather, games, genetics, or queues, the same framework applies: states, transitions, and a distribution that governs how you move between them.

The power is in the **simplicity and generality**: a single matrix encodes an entire system's dynamics. The cost is in the **loss of fidelity**: real systems often have memory, hidden structure, and properties that a simple Markov chain can't capture.

Understanding when Markov chains apply—and when they fail—is a key skill. You now know the signs: Is the future independent of the distant past? Can you define a clear state space? Are the transition probabilities stationary?

If yes, you have a powerful tool. If no, you'll need something more sophisticated.

---

## Exercises

See [exercises.md](exercises.md) for 15 progressive exercises covering:
- Warm-up: Implement and simulate a weather model
- Exploration: Model board games and genetics
- Challenge: Fit real data and compare to simulations
- Thought experiments: Limits of the Markov assumption
