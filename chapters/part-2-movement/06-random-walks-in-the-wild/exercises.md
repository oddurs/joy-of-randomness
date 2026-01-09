# Chapter 6 Exercises: Random Walks in the Wild

## Warm-up Exercises

**1. Visualize step-length distributions**

Load or simulate animal tracking data (you can use the `simulate_realistic_animal_track()` function from simulations.py). Extract the step-length distribution and plot a histogram. Describe: Is it exponential, power-law, or something else?

**Hint:** Use `np.histogram()` or `plt.hist()`. Try both linear and log-log scales.

---

**2. Compare two trajectory types**

Simulate two paths:
- An ideal random walk (fixed step size 1.0, 5000 steps)
- A Lévy flight (power-law exponent α = 1.5, 5000 steps)

Plot both paths on the same axes (or side by side). Compute:
- Final distance from origin for each
- Maximum distance reached
- Total path length

Compare these metrics. Which walk covers more ground?

**Hint:** Use the visualization functions in simulations.py as a starting point.

---

**3. Power-law exponent estimation**

Generate synthetic data from a Lévy flight with α = 1.8. Extract step lengths. Use the `fit_power_law_exponent()` function to estimate α from the data. How close is your estimate to the true value?

Repeat this 10 times and report the mean and standard deviation of your estimates.

**Hint:** The estimate will be better if you use a longer walk (more steps).

---

## Exploration Exercises

**4. Return probability in 2D**

Simulate many random walks in 2D (use the ideal random walk, fixed step size 1.0). Track whether each walk returns to within distance 0.1 of the origin within 10,000 steps.

Estimate the return probability empirically. Does this match Pólya's theorem (probability = 1 in 2D)?

**Hint:** For each walk, check if `min(distance_to_origin)` is ever less than 0.1.

---

**5. Spread comparison: Step size effects**

Simulate 10 walks of 5000 steps each using three different step distributions:
1. Fixed size (size = 1)
2. Exponential (mean = 1)
3. Power-law (α = 1.5)

Plot the mean final distance vs. number of steps for each. On a log-log plot, which one is closest to √n? Which is fastest?

**Hint:** Use `plot_spread_comparison()` in simulations.py.

---

**6. Direction persistence**

Simulate two correlated random walks:
- Low persistence (standard deviation of angle change = 0.1)
- High persistence (standard deviation of angle change = 0.5)

Plot both paths. Measure the "straightness" of each path by computing:
$$\text{Straightness} = \frac{\text{Final distance}}{\text{Path length}}$$

Does higher persistence lead to straighter paths?

**Hint:** The path length is the sum of all step lengths.

---

**7. The Lévy hypothesis in action**

Simulate a foraging scenario: food patches are scattered randomly in a 2D plane. A walker uses a Lévy flight strategy (mostly small steps, occasional large jumps).

Compare to a walker using fixed-step random walks. Which finds food faster (fewer steps to reach a target)?

**Hint:** You'll need to place "food" locations randomly and measure steps until first encounter.

---

## Challenge Exercises

**8. Multi-species analysis**

The `simulate_realistic_animal_track()` function has species-specific parameters. Simulate walks for 'albatross', 'turtle', 'bacterium', and 'default'. Extract step lengths for each.

Fit power-law exponents and compare across species. Discuss: Do these parameter choices make biological sense?

**Hint:** Check the parameters in the function definition.

---

**9. Anomalous diffusion**

Define "effective diffusion" as the mean squared distance after n steps. For random walks with different step-size distributions, plot $\langle r^2 \rangle$ vs. $n$ on a log-log scale.

Compute the exponent β such that $\langle r^2 \rangle \sim n^{\beta}$. You should see β ≈ 1 for fixed steps, β ≈ 1.33 for Lévy (α = 1.5).

**Hint:** Use `np.polyfit()` on the log-log data to find the slope.

---

**10. Power-law fitting with noise**

Generate synthetic data from a power-law distribution with α = 1.6, but add 20% noise (multiplicative random error). Fit the exponent using `fit_power_law_exponent()`.

Repeat 50 times and plot a histogram of estimates. How much bias is introduced by noise?

**Hint:** Noise can be added by multiplying step sizes by `1 + 0.2 * np.random.randn()`.

---

**11. Optimal search strategy**

You're a forager in a sparse environment. Food is found randomly, with an average of 1 food item per 100 square units. You have 10,000 energy units; each step costs 1 unit.

Compare success rates (food found before energy exhausted) for walkers using:
- Fixed steps (size 1)
- Exponential steps (mean 1)
- Lévy flights (α = 1.5, 1.7, 1.9)

Which strategy finds the most food? Does α matter?

**Hint:** Model food locations as Poisson points in space.

---

## Thought Experiments

**12. Why not always Lévy?**

If Lévy flights are optimal for sparse environments, why don't all animals use them? Brainstorm at least three biological or ecological constraints that might favor other strategies.

---

**13. Brownian vs. Lévy**

Lévy flights have diverging variance, causing "superdiffusion" (spreading faster than √n). What are the practical consequences of this for an animal?

For example: What if the environment has obstacles, walls, or predators at the boundary?

---

**14. From discrete to continuous**

We've modeled movement as discrete steps. Real movement is continuous. How would the analysis change if we allowed:
- Variable waiting times between steps (continuous-time random walks)?
- Drift (a preferred direction, like migration)?
- Obstacles or terrain features?

---

**15. Biological reality check**

Find a real dataset of animal movement (e.g., from Movebank, a public repository of GPS tracks). Fit a power-law exponent to it. Does the Lévy hypothesis hold? If not, what might explain the discrepancy?

---

## Open-Ended Exploration

**Design your own experiment:**

Pick a phenomenon that involves movement or search: bird migration, foraging insects, human wandering, disease spread, etc.

Model it as a random walk variant. What assumptions are reasonable? Where might the model break down? Would Lévy flights, correlated walks, or another variant fit better?
