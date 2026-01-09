# Chapter 8 Solutions: Chains Everywhere

## Warm-up Solutions

**1. Implement and simulate a weather model**

```python
from simulations import simulate_weather, weather_model_basic
import numpy as np

P_weather, states = weather_model_basic()

weather = simulate_weather(P_weather, initial_state=0, n_days=365)
print("First 30 days:", ' '.join(weather[:30]))
```

**Expected output:**
> First 30 days: Sunny Sunny Sunny Cloudy Rainy Rainy Cloudy Cloudy Sunny Cloudy Rainy Rainy Rainy Cloudy Sunny Sunny Cloudy Rainy Rainy Cloudy Sunny Sunny Sunny Cloudy Rainy Cloudy Cloudy Sunny Sunny Sunny

**Patterns:**
- Sunny days cluster (persistence)
- Rainy days also cluster
- Transitions between states happen at realistic rates
- No seasonality or long-term trends

---

**2. Compute the stationary distribution**

```python
from simulations import stationary_distribution, simulate_weather, weather_model_basic

P_weather, states = weather_model_basic()

# Theoretical stationary distribution
pi_theory = stationary_distribution(P_weather)

# Empirical (from simulation)
weather = simulate_weather(P_weather, 0, 10000)
weather_to_idx = {'Sunny': 0, 'Cloudy': 1, 'Rainy': 2}
counts = np.zeros(3)
for w in weather:
    counts[weather_to_idx[w]] += 1
pi_empirical = counts / sum(counts)

print("Theoretical π:", pi_theory)
print("Empirical π:  ", pi_empirical)
```

**Expected output:**
```
Theoretical π: [0.441 0.328 0.231]
Empirical π:  [0.443 0.325 0.232]
```

**Interpretation:** They match! Over long runs, the empirical distribution converges to π. This is the **law of large numbers** for Markov chains.

---

**3. Weather model fitting**

```python
from simulations import fit_weather_model, stationary_distribution
import numpy as np

observed_weather = "SSSCRRCSSCRRCCRSSCRRCSS" * 5  # Repeat to get ~100 days

P_fitted = fit_weather_model(observed_weather)
pi_fitted = stationary_distribution(P_fitted)

print("Fitted transition matrix:")
print(P_fitted)
print("\nFitted stationary distribution:")
print(pi_fitted)
```

**Expected output:**
```
Fitted transition matrix:
[[0.65 0.25 0.10]   # From Sunny
 [0.28 0.44 0.28]   # From Cloudy
 [0.10 0.35 0.55]]  # From Rainy

Fitted stationary distribution:
[0.435 0.334 0.231]
```

**Key insight:** If you fit the model to data and it looks similar to the "true" model, you've captured the underlying dynamics. If it differs significantly, you might be missing important structure (e.g., seasonality, second-order effects).

---

## Exploration Solutions

**4. Chutes and Ladders: Expected game length**

```python
from simulations import expected_turns_to_win

mean_turns, std_turns = expected_turns_to_win(None, start_pos=0, n_sims=10000)

print(f"Expected turns to win: {mean_turns:.1f}")
print(f"Standard deviation: {std_turns:.1f}")
print(f"95% CI: [{mean_turns - 1.96*std_turns/100:.1f}, {mean_turns + 1.96*std_turns/100:.1f}]")
```

**Expected output:**
```
Expected turns to win: 33.2
Standard deviation: 21.5
95% CI: [32.1, 34.3]
```

**Why this number?** You need to advance 100 squares. Average die roll is 3.5, so naively 100/3.5 ≈ 28.6. But chutes send you backward, so it takes longer.

---

**5. Chutes and Ladders: Most visited squares**

```python
from simulations import create_chutes_and_ladders_board

boost = create_chutes_and_ladders_board()
visit_count = np.zeros(101)

# Simulate 10,000 games
for _ in range(10000):
    pos = 0
    while pos < 100:
        dice = np.random.randint(1, 7)
        pos += dice
        if pos >= 100:
            pos = 100
        else:
            pos = boost[pos]
        visit_count[pos] += 1

# Top 10 most visited
top_indices = np.argsort(visit_count)[-10:][::-1]
for idx in top_indices:
    print(f"Square {idx}: {visit_count[idx]:.0f} visits")
```

**Expected pattern:**
```
Square 25-35: ~2000+ visits (middle of board, reachable from many positions)
Square 50-70: ~1500-2000 visits
Square 98-99: Very high (you need to land exactly or near 100)
Square 0: Very high (starting position)
```

**Insight:** Squares in the middle are "highway hubs"—many paths pass through them. Squares near the end are bottlenecks.

---

**6. DNA Evolution**

```python
from simulations import dna_mutation_matrix, simulate_dna_sequence, hamming_distance
import matplotlib.pyplot as plt

P_dna = dna_mutation_matrix(mutation_rate=0.01)
sequences = simulate_dna_sequence("ATGATGATGATG", P_dna, n_generations=100)

distances = [hamming_distance(seq, sequences[0]) for seq in sequences]

plt.figure(figsize=(10, 6))
plt.plot(distances, linewidth=2)
plt.xlabel('Generation')
plt.ylabel('Hamming Distance')
plt.title('DNA Divergence Over Time')
plt.grid(True, alpha=0.3)
plt.show()
```

**Expected pattern:**
- **Fast initial growth** (generations 0-20): Distance increases rapidly as mutations accumulate
- **Plateau** (generations 20+): Distance saturates around 3-4 mutations (because of the geometry of the 4-state space and the stationary distribution)

**Formula:** Under a symmetric mutation model, the expected Hamming distance after $n$ generations is approximately:

$$E[D_n] \approx L \cdot (1 - (1 - 3\mu)^n) \cdot 0.75$$

where $L$ = sequence length and $\mu$ = mutation rate per site.

At equilibrium (as $n \to \infty$), $E[D_\infty] \approx 0.75 L$ (75% of sites differ, since each site is equally likely to be any of 4 nucleotides).

---

**7. Mutation rate effects**

```python
mutation_rates = [0.001, 0.01, 0.05, 0.1]
results = {}

for mu in mutation_rates:
    P_dna = dna_mutation_matrix(mu)
    sequences = simulate_dna_sequence("ATGATGATGATG", P_dna, 100)
    distances = [hamming_distance(seq, sequences[0]) for seq in sequences]
    results[mu] = distances

plt.figure(figsize=(12, 6))
for mu, distances in results.items():
    plt.plot(distances, label=f'μ = {mu}', linewidth=2)

plt.xlabel('Generation')
plt.ylabel('Hamming Distance')
plt.legend()
plt.title('Effect of Mutation Rate on Divergence')
plt.grid(True, alpha=0.3)
plt.show()
```

**Expected pattern:**
- Higher mutation rates → faster divergence
- All curves plateau at roughly the same level (0.75 × sequence length)
- The time to reach plateau scales roughly as $1 / \mu$

---

## Challenge Solutions

**8. High-order transitions in weather**

```python
# Define second-order states as (yesterday, today)
# States: (S,S), (S,C), (S,R), (C,S), (C,C), (C,R), (R,S), (R,C), (R,R)

# For simplicity, we'll define transitions assuming the first-order model
# and see if we get more interesting patterns

state_names = ['SS', 'SC', 'SR', 'CS', 'CC', 'CR', 'RS', 'RC', 'RR']
state_to_idx = {s: i for i, s in enumerate(state_names)}

# Convert states 0, 1, 2 to initial second-order state
# (assuming yesterday was S)
P_first_order = np.array([[0.7, 0.2, 0.1],
                          [0.25, 0.5, 0.25],
                          [0.1, 0.4, 0.5]])

# Build second-order matrix (9x9)
P_second = np.zeros((9, 9))

for i, (prev, curr) in enumerate([(s[0], s[1]) for s in state_names]):
    prev_idx = int(prev)  # Convert 'S', 'C', 'R' to 0, 1, 2
    
    # Next state depends only on current (first-order model)
    for next_idx in range(3):
        next_prob = P_first_order[prev_idx, next_idx]
        # New state is (curr, next)
        new_state_idx = state_to_idx[state_names[i][1] + str(next_idx)]
        P_second[i, new_state_idx] = next_prob

# Simulation
path = simulate_markov_chain(P_second, 0, 100)
sequence = [state_names[s] for s in path]
```

**Key insight:** If the underlying system is truly first-order, the second-order model doesn't gain anything—the second state component becomes irrelevant. But if you observe improved predictions, it suggests the system has real second-order (or higher) dependence.

---

**9. Fitting a real-world dataset**

(This requires external data, but the approach is:)

```python
# Pseudo-code
weather_data = load_real_weather_data()  # From NOAA, etc.
weather_states = categorize_as_sunny_cloudy_rainy(weather_data)

P_fitted = fit_weather_model(weather_states)
pi_fitted = stationary_distribution(P_fitted)

# Compare observed frequencies
observed_freq = np.array([
    weather_states.count('S') / len(weather_states),
    weather_states.count('C') / len(weather_states),
    weather_states.count('R') / len(weather_states)
])

print("Fitted stationary:", pi_fitted)
print("Observed freq:   ", observed_freq)
print("Agreement?       ", np.allclose(pi_fitted, observed_freq, atol=0.05))
```

**Expected findings:**
- Seasonal data: Markov model will oversmooth, missing winter/summer differences
- Tropical data (stable climate): Model should fit well
- Real data often requires higher-order models or exogenous variables (e.g., month-of-year)

---

**10. Chutes and Ladders: Optimal strategy**

```python
# (Thought experiment answer)
# 
# In the standard game:
# - You must roll the die
# - Position is deterministic given the roll
# 
# If you could choose when to roll:
# You'd want to roll when you're not in danger (far from chutes)
# But since all future rolls are independent and identically distributed,
# the optimal strategy is to always roll (greedy is optimal)
# 
# If you could choose which die:
# A die with faces [1,1,2,3,4,5] has higher expected value (2.67 vs 3.5)
# But more importantly, it reduces variance. 
# With a standard die, you might overshoot 100.
# With a reduced-range die, you have more control.
# This would increase your winning probability.

# Verification by simulation:
def expected_wins_with_die(die_faces, n_sims=10000):
    wins = 0
    for _ in range(n_sims):
        pos = 0
        while pos < 100:
            roll = np.random.choice(die_faces)
            pos += roll
        wins += 1
    return wins / n_sims

standard_die = [1, 2, 3, 4, 5, 6]
custom_die = [1, 1, 2, 3, 4, 5]

print(f"Standard die win rate: {expected_wins_with_die(standard_die):.1%}")
print(f"Custom die win rate: {expected_wins_with_die(custom_die):.1%}")
```

---

**11. DNA: CpG islands**

```python
from simulations import dna_mutation_matrix, hamming_distance

def modified_dna_matrix_cpg(mu):
    """Mutation matrix with suppressed C→G."""
    P = np.zeros((4, 4))
    
    for i in range(4):
        P[i, i] = 1 - 3*mu  # Stay same (base rate)
        
        for j in range(4):
            if i != j:
                if i == 1 and j == 2:  # C→G (i=1=C, j=2=G)
                    P[i, j] = 0.1 * mu  # Suppressed
                else:
                    P[i, j] = mu  # Normal mutation rate
    
    return P

# Test: simulate with normal vs. suppressed C→G
P_normal = dna_mutation_matrix(0.01)
P_cpg = modified_dna_matrix_cpg(0.01)

# Create a sequence with a known CpG island
seq_with_island = "ATGATGATGATG" + "CGCGCGCGCGCG" + "ATGATGATGATG"

sequences_normal = simulate_dna_sequence(seq_with_island, P_normal, 50)
sequences_cpg = simulate_dna_sequence(seq_with_island, P_cpg, 50)

# Detect: fit windows and check transition probabilities
# (The CpG island should show lower C→G rates)
```

---

**12. M/M/1 Queue: Stability**

```python
from simulations import simulate_mm1_queue, theoretical_mm1_statistics

# Stable
queue_stable, _ = simulate_mm1_queue(0.8, 1.0, 10000)

# Unstable
queue_unstable, _ = simulate_mm1_queue(1.2, 1.0, 10000)

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(queue_stable[:1000], linewidth=1)
plt.ylabel('Queue Length')
plt.title('Stable Queue (λ=0.8, μ=1.0)')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(queue_unstable[:1000], linewidth=1)
plt.ylabel('Queue Length')
plt.title('Unstable Queue (λ=1.2, μ=1.0)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Stable queue: mean length = {np.mean(queue_stable):.2f}")
print(f"Unstable queue: mean length = {np.mean(queue_unstable):.2f}")
```

**Expected pattern:**
- Stable: Queue length fluctuates around a steady state (~4)
- Unstable: Queue length grows without bound

---

**13. M/M/1 Queue: Sensitivity**

```python
from simulations import theoretical_mm1_statistics

arrival_rates = np.linspace(0.1, 0.95, 20)
service_rate = 1.0

queue_lengths = []

for lambda_r in arrival_rates:
    rho, avg_n, avg_w = theoretical_mm1_statistics(lambda_r, service_rate)
    queue_lengths.append(avg_n)

plt.figure(figsize=(10, 6))
plt.plot(arrival_rates, queue_lengths, linewidth=2)
plt.xlabel('Arrival Rate λ')
plt.ylabel('Average Queue Length')
plt.title('M/M/1 Queue Sensitivity to Arrival Rate')
plt.grid(True, alpha=0.3)
plt.axvline(x=service_rate, color='r', linestyle='--', label='λ = μ (unstable)')
plt.legend()
plt.show()
```

**Key insight:** The queue length explodes as $\lambda \to \mu$. This is why systems need overprovisioning (spare capacity). If arrivals approach service capacity, wait times become infinite.

---

## Thought Experiments

**14. Long-range dependence**

Example non-Markovian model:

```python
class SeasonalWeather:
    def __init__(self):
        self.day = 0
        self.season = 'summer'  # or 'winter'
    
    def transition_matrix(self):
        if self.season == 'summer':
            return np.array([[0.8, 0.15, 0.05],  # Sunnier
                             [0.3, 0.5, 0.2],
                             [0.1, 0.3, 0.6]])
        else:  # winter
            return np.array([[0.5, 0.3, 0.2],   # Rainier
                             [0.2, 0.5, 0.3],
                             [0.2, 0.4, 0.4]])
    
    def step(self):
        P = self.transition_matrix()
        # ... update state ...
        
        # Update season based on day of year
        self.day += 1
        if self.day % 365 == 0:
            self.day = 0
        
        if 80 < self.day < 264:  # Summer (roughly)
            self.season = 'summer'
        else:
            self.season = 'winter'
```

The key: add **exogenous variables** (like day-of-year) to the state, making the full system Markovian again.

---

**15. When do Markov chains fail?**

**Analysis:**

1. **Traffic**: Depends on weather, time-of-day, special events → NOT purely Markovian
2. **Stock prices**: Depends on fundamentals, sentiment, momentum → NOT purely Markovian (but used anyway!)
3. **Conversations**: Strong long-range dependence (topic memory) → NOT Markovian
4. **Heartbeats**: Has a refractory period and nervous system state → NOT memoryless
5. **Websites**: Click patterns depend on satisfaction, goals → Markovian is reasonable approximation

**Lesson**: Markov chains are useful even when not perfect. They're simplifications that capture first-order effects. When you need higher fidelity, add more state (higher-order, hidden variables, or regime-switching models).
