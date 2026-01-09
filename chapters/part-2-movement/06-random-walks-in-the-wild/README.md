# Chapter 6: Random Walks in the Wild

## Hook

An albatross flies 10,000 kilometers across the Pacific. A bacterium tumbles through a water droplet. A shopper wanders through a mall. Are they all doing the same thing?

If you watched them from high above, they might all look like random walks. But zoom in, and they're not all equivalent. The albatross makes a few big sweeping journeys across vast stretches, with occasional smaller local searches near productive fishing grounds. The bacterium performs a different dance—short tumbles interrupted by long, smooth runs. The shopper starts in a store with no plan, picks things up and puts them back, then suddenly heads decisively toward the exit.

In the chapters so far, we've studied the *idealized* random walk: fixed step size, no memory, purely random direction at each step. This is beautifully simple, and it captures something true about movement in nature. But real walkers are more complex. They have momentum, they adapt to their environment, and their step sizes vary wildly.

This chapter is about what happens when you take the random walk seriously as a model for real movement, and then ask: where does our simple model break down? We'll see that sometimes the breakdown isn't a bug—it's a feature. Some of nature's most successful foragers use step distributions that look *nothing* like the bell curves we've been studying. Instead, they follow power laws: a few enormous leaps punctuate a background of tiny steps.

These are called Lévy flights, and they might be optimal strategies for finding food in a sparse world.

## First Contact

Let's start by looking at real movement data. Here's animal tracking from GPS loggers:

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulated animal track (you could load real GPS data here)
# Animals move in 2D space, so position = (x, y)

def load_animal_track(num_steps=5000):
    """
    Simulate a realistic animal track with some directional persistence
    and variable step sizes.
    """
    x, y = [0], [0]
    angle = np.random.uniform(0, 2 * np.pi)
    
    for _ in range(num_steps):
        # Step size: mostly short, occasional long jumps
        step_size = np.random.exponential(scale=1.0)
        
        # Direction persists (correlated walk)
        angle += np.random.normal(loc=0, scale=0.3)
        
        x.append(x[-1] + step_size * np.cos(angle))
        y.append(y[-1] + step_size * np.sin(angle))
    
    return np.array(x), np.array(y)

x, y = load_animal_track()
plt.figure(figsize=(10, 5))
plt.plot(x, y, linewidth=0.5, alpha=0.7)
plt.scatter([0], [0], color='red', s=100, label='Start')
plt.scatter([x[-1]], [y[-1]], color='green', s=100, label='End')
plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.title('Animal Movement Track')
plt.legend()
plt.gca().set_aspect('equal')
plt.show()
```

Look at this track. Does it look random? It has structure: areas where the animal lingers, moments where it commits to a direction, some long rapid transits. But there's no master plan, no obvious strategy—it's more like a wandering with some built-in rules.

This is what animal movement looks like in the wild. Now let's ask: how does it compare to our theoretical random walks?

## Patterns Emerge

Let's extract the step lengths from a real-looking track and from a simple random walk, and compare them:

```python
def step_lengths(x, y):
    """Extract distances between consecutive positions."""
    dx = np.diff(x)
    dy = np.diff(y)
    return np.sqrt(dx**2 + dy**2)

# Compare three types of movement
np.random.seed(42)

# 1. Ideal random walk (fixed steps)
ideal_x, ideal_y = [0], [0]
for _ in range(5000):
    angle = np.random.uniform(0, 2 * np.pi)
    ideal_x.append(ideal_x[-1] + np.cos(angle))
    ideal_y.append(ideal_y[-1] + np.sin(angle))
ideal_x, ideal_y = np.array(ideal_x), np.array(ideal_y)

# 2. Realistic animal track
animal_x, animal_y = load_animal_track(5000)

# 3. Pure Lévy flight (power-law steps)
levy_x, levy_y = [0], [0]
for _ in range(5000):
    angle = np.random.uniform(0, 2 * np.pi)
    step_size = np.random.pareto(a=1.5) + 1  # Power-law distribution
    levy_x.append(levy_x[-1] + step_size * np.cos(angle))
    levy_y.append(levy_y[-1] + step_size * np.sin(angle))
levy_x, levy_y = np.array(levy_x), np.array(levy_y)

# Plot the three types
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].plot(ideal_x, ideal_y, linewidth=0.3, alpha=0.7)
axes[0].set_title('Ideal Random Walk')
axes[0].set_aspect('equal')

axes[1].plot(animal_x, animal_y, linewidth=0.3, alpha=0.7)
axes[1].set_title('Realistic Animal Track')
axes[1].set_aspect('equal')

axes[2].plot(levy_x, levy_y, linewidth=0.3, alpha=0.7)
axes[2].set_title('Lévy Flight')
axes[2].set_aspect('equal')

plt.tight_layout()
plt.show()
```

Notice the differences:
- The ideal random walk fills space fairly uniformly.
- The animal track has clusters—areas where the walker spends time—interspersed with long transits.
- The Lévy flight is extreme: a few enormous jumps define the overall span, with lots of local searching in between.

Now let's look at the step-length distributions:

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

steps_ideal = step_lengths(ideal_x, ideal_y)
steps_animal = step_lengths(animal_x, animal_y)
steps_levy = step_lengths(levy_x, levy_y)

# Linear scale
for ax, steps, title in zip(axes[:2], [steps_ideal, steps_animal], 
                             ['Ideal Random Walk', 'Animal Track']):
    ax.hist(steps, bins=50, density=True, alpha=0.7, edgecolor='black')
    ax.set_xlabel('Step Length')
    ax.set_ylabel('Probability Density')
    ax.set_title(title)

# Log-log scale for Lévy
axes[2].loglog(np.sort(steps_levy), np.arange(1, len(steps_levy) + 1) / len(steps_levy), 
               drawstyle='steps-pre', alpha=0.7)
axes[2].set_xlabel('Step Length')
axes[2].set_ylabel('Cumulative Probability')
axes[2].set_title('Lévy Flight (log-log)')

plt.tight_layout()
plt.show()
```

The ideal random walk has a sharp peak at step size 1 (you either take a step or you don't). The animal track shows an exponential tail: a few very long steps, mostly short ones. And the Lévy flight? Its distribution is a straight line on a log-log plot, which means it follows a power law:

$$P(\text{step} > s) \propto s^{-\alpha}$$

where $\alpha \in (1, 3)$ is the power-law exponent. This says: there are many short steps and occasional enormous jumps.

Here's what makes this interesting: the ideal random walk spreads as $\sqrt{n}$, where $n$ is the number of steps. The power law of a Lévy flight means it spreads *faster*. It's not just a minor variation—it's a fundamentally different scaling regime.

## The Theory

Let's understand what's happening mathematically.

**Fixed step sizes (ideal random walk):**
If each step has length 1, then after $n$ steps, the expected squared distance from the origin is:

$$E[r^2] = n$$

So the typical distance is $r \sim \sqrt{n}$.

**Variable step sizes (Lévy flight):**
Suppose step lengths $s$ follow a power law: $P(s > x) = (x_0 / x)^{\alpha}$ for some $\alpha \in (1, 2)$. 

For a Lévy flight, something remarkable happens: the typical distance grows as

$$r \sim n^{1/\alpha}$$

For instance, if $\alpha = 1.5$, then $r \sim n^{0.67}$—even faster than the square-root law! The walker covers ground more efficiently by occasionally taking enormous leaps.

Why does this happen? The variance of a single step is:

$$\text{Var}(s) = E[s^2] - E[s]^2$$

For a power-law distribution with $\alpha < 2$, the variance *diverges*. There is no finite variance! A few enormous steps dominate everything else. These rare giants do the heavy lifting in covering distance.

**Optimal foraging hypothesis:**
Imagine you're a predator searching for food scattered sparsely in space. The Lévy flight hypothesis suggests: if food is hard to find, use a power-law strategy. Make mostly small steps to search a patch thoroughly, but occasionally leap far away to try a new area.

This was proposed theoretically by Reuben Metzler and others in the 1990s. Remarkably, when people analyzed real GPS data from albatrosses, sea turtles, and other marine animals, they found evidence that their step-length distributions have power-law tails. It seemed nature had discovered this "optimal" strategy independently.

(The debate continues: is this truly optimal, or are other factors at play? But the empirical evidence is striking.)

**Correlated random walks:**
Real animals also show *directional persistence*: if you just took a step northward, you're more likely to continue northward than to suddenly turn south. This is different from a Lévy flight—it's still about the power-law steps, but add memory.

A correlated random walk can be modeled as:

$$\theta_n = \theta_{n-1} + \eta_n$$

where $\theta_n$ is the direction of step $n$ and $\eta_n$ is a small random perturbation. The direction "drifts" rather than jumping.

Combine this with power-law step lengths, and you get a model that looks much more like real animal movement.

## Going Deeper

**Continuous-time random walks:**
In our discrete models, the walker takes steps at regular intervals. But real movement is continuous. A bacterium swims for a while, then pauses and "tumbles" to reorient, then swims in a new direction.

For a continuous-time random walk, the waiting times between jumps can also be random and long-tailed. This introduces *subdiffusive* behavior: the walker spreads even more slowly than a standard random walk because it spends long periods stationary.

**Anomalous diffusion:**
When step sizes and waiting times both have heavy tails, the spreading follows

$$\langle r^2 \rangle \sim t^{\beta}$$

where $\beta \neq 1$. If $\beta < 1$, it's *subdiffusive* (spreading slower than Brownian motion); if $\beta > 1$, it's *superdiffusive* (spreading faster). Lévy flights give $\beta > 1$.

**From discrete to continuous:**
As $n \to \infty$, a random walk with fixed steps converges to Brownian motion. A Lévy flight converges to a *stable process*—a generalization of Brownian motion where the step distribution has heavy tails. These stable processes show up in finance (stock price changes), seismology (earthquake magnitudes), and ecology.

## Real Data

Let's fit a simple model to synthetic data and see how well we can estimate the power-law exponent:

```python
def fit_power_law_exponent(steps, cutoff=1.0):
    """
    Estimate power-law exponent using maximum likelihood on steps above cutoff.
    For P(s > x) ~ x^{-alpha}, the MLE is alpha = 1 + n / sum(log(s_i / s_min))
    """
    steps_above = steps[steps > cutoff]
    if len(steps_above) < 10:
        return None
    
    alpha = 1 + len(steps_above) / np.sum(np.log(steps_above / cutoff))
    return alpha

# Generate synthetic Lévy flight data
np.random.seed(42)
synthetic_steps = np.random.pareto(a=1.5) + 1
for _ in range(4999):
    synthetic_steps = np.append(synthetic_steps, np.random.pareto(a=1.5) + 1)

# Estimate exponent
alpha_est = fit_power_law_exponent(synthetic_steps, cutoff=1.0)
print(f"True exponent: 1.5, Estimated exponent: {alpha_est:.2f}")

# Plot actual vs. fitted
fig, ax = plt.subplots(figsize=(10, 6))

# Empirical cumulative distribution
sorted_steps = np.sort(synthetic_steps)
cdf = np.arange(1, len(sorted_steps) + 1) / len(sorted_steps)
ccdf = 1 - cdf

ax.loglog(sorted_steps, ccdf, 'o', markersize=3, label='Empirical', alpha=0.7)

# Fitted power law
s_range = np.logspace(0, 3, 100)
ax.loglog(s_range, (1.0 / s_range)**alpha_est, '-', linewidth=2, label=f'Fitted (α={alpha_est:.2f})')

ax.set_xlabel('Step Length (s)')
ax.set_ylabel('P(S > s)')
ax.set_title('Fitting Power-Law Exponent')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

In practice, you'd load real GPS data from a dataset like Movebank and repeat this analysis. You'd find that different species have different exponents: albatrosses cluster around $\alpha \approx 1.6$, while some marine microorganisms show $\alpha$ closer to 2.

## Rabbit Holes

**The Lévy flight foraging hypothesis—and the controversy**

The idea that animals use Lévy flights optimally is elegant and intuitive. But does nature actually do it? Starting in the early 2000s, researchers like Gandhimohan Viswanathan analyzed GPS tracks from wandering albatrosses and claimed to find power-law step distributions. The implication: albatrosses have evolved to use optimal search strategies.

The controversy: some later studies questioned whether the data actually supported power laws, or whether simpler explanations (like a mixture of two exponential distributions) fit just as well. The debate continues. The lesson: fitting power laws is harder than it looks, and biology is messier than elegant theory.

**Human mobility and Brockmann's law**

Dirk Brockmann and colleagues studied human movement using the locations of lost dollar bills that people found and mailed back. They tracked how far each bill traveled. The result: human movement follows a power law with exponent around 1.6—similar to migratory birds!

This suggests that we, too, move in a Lévy-like pattern: mostly staying local, with occasional long journeys. This has implications for disease spread, traffic flow, and social networks.

**Random walks in ecology and epidemiology**

Random walk models permeate ecology. How do seeds disperse from a parent plant? How do animals find mates or territories? How does a disease propagate through a population?

In epidemiology, simple random walk models of movement inform predictions about pathogen spread. During COVID-19, understanding human movement patterns became urgent for modeling infection risk. Animals with heavy-tailed step distributions might spread diseases faster and farther than simple exponential models predict.

The common theme: adding realism to random walks—power-law steps, correlated directions, environmental heterogeneity—changes the quantitative predictions in ways that matter for conservation, disease control, and urban planning.

## Summary

Random walks give us a framework for thinking about movement in nature. The simplest version—fixed steps, no memory, purely random direction—is already powerful. But real walkers are more complex:

1. **Step sizes vary**, often following power laws. Rare long jumps combine with frequent short steps.
2. **Steps correlate**, so movement has momentum: you're more likely to continue in your current direction.
3. **The environment matters**, shaping the distribution of available moves.

When these factors combine, we get Lévy flights and correlated walks—models that fit real animal movement data far better than the idealized random walk. And remarkably, these aren't ad-hoc complications. The Lévy flight seems to be an optimal search strategy in sparse environments, and nature has evolved to use it.

This brings us to an important shift. So far, we've treated each walker independently. But what if many walkers interact? What if the "walker" isn't a creature but a disease spreading through a population, or a rumor spreading through a network? That's where we'll go next: to chains of probability, where the future depends not just on your current position, but on what state you're in.

### Exercises

1. **Warm-up:** Download or simulate animal tracking data. Extract the step-length distribution. Compute a histogram. Is it closer to exponential or power-law?

2. **Exploration:** Simulate a Lévy flight with power-law exponent $\alpha = 1.5$. Simulate an ideal random walk with the same number of steps. Compare the final distance from the origin and the path geometry.

3. **Challenge:** Implement a correlated random walk where each step direction is $\theta_n = \theta_{n-1} + \eta_n$ with $\eta_n \sim N(0, 0.3^2)$. Use power-law step sizes. Compare the resulting path to a non-correlated Lévy flight.

4. **Thought experiment:** If Lévy flights are optimal for foraging, why don't all animals use them? What constraints might prevent evolution from adopting this strategy universally?

5. **Open exploration:** Obtain real movement data (e.g., from Movebank). Fit a power-law exponent to several animals in the same species. How variable is the exponent? Does it correlate with environment or diet?
