# Exercises for Chapter 5: Wandering in Two Dimensions

These exercises build intuition for how dimension affects random walk behavior. You'll discover Pólya's recurrence theorem empirically and understand why dimension 2 is a critical threshold.

---

## Warm-up: Visualizing 2D Walks

**Goal:** Get comfortable with 2D simulation and visualization.

### Exercise 5.1: Plot a Single 2D Walk

Generate and plot a 2D random walk of 5000 steps.

**What to do:**
1. Simulate a 2D walk where each step is up, down, left, or right with equal probability
2. Plot the path with the starting point in red and ending point in green
3. Record: final distance from origin, maximum distance reached

**Questions:**
- What does the path look like visually?
- Does it stay near the origin or wander far?
- How often does it cross itself?

---

### Exercise 5.2: Multiple 2D Walks

Generate and overlay 8 different 2D walks (5000 steps each).

**What to do:**
1. Create 8 independent 2D walks
2. Plot them all on the same figure with different colors
3. Mark the origin with a star or similar

**Questions:**
- How do the paths differ from each other?
- Do they all seem to cluster around the origin?
- Can you spot any walk that strays far from others?

---

### Exercise 5.3: Compare Distances in 1D, 2D, 3D

Generate 1000 walks in each dimension (1000 steps each) and compare final distances.

**What to do:**
1. For 1D: run 1000 walks, record final position |x|
2. For 2D: run 1000 walks, record final distance √(x² + y²)
3. For 3D: run 1000 walks, record final distance √(x² + y² + z²)
4. Plot histograms side by side
5. Calculate mean distance for each dimension

**Questions:**
- How do the average distances compare?
- Are they all roughly equal? Or does dimension affect it?
- What's the ratio of 2D distance to 1D distance?

---

## Exploration: Understanding Dimension

**Goal:** Discover how dimension changes walk behavior in surprising ways.

### Exercise 5.4: Return Probability in 2D

Track how often 2D walkers return to the origin.

**What to do:**
1. Run 500 walks, each up to 100,000 steps
2. For each walk, record whether it returns to origin (0,0) and after how many steps
3. Calculate: what fraction returned?
4. Plot a histogram of return times (use log scale)

**Hints:**
- Use the `return_to_origin_2d()` function from simulations.py
- Expected: ~95-99% should return (Pólya's theorem says 100%, but with finite max_steps we miss some)
- Return times will have a long tail

**Questions:**
- What fraction returned?
- Is this surprising? Does it match Pólya's prediction?
- What are typical return times?

---

### Exercise 5.5: Return Probability in 3D

Repeat Exercise 5.4 but in 3D.

**What to do:**
1. Run 500 walks in 3D, each up to 100,000 steps
2. Track returns to (0,0,0)
3. Compare the fraction that returned to the 2D case

**Hints:**
- 3D walks should return much less often than 2D
- Expected: around 30-40% (Pólya's theorem says ~34%)
- You might see some never return even in 100,000 steps

**Questions:**
- What fraction returned in 3D?
- How does this compare to 2D?
- Can you explain why dimension matters?

---

### Exercise 5.6: Maximum Distance vs Final Distance

For 2D and 3D walks, compare the maximum distance reached versus the final distance.

**What to do:**
1. Run 500 walks in 2D (5000 steps each)
2. For each, track both the maximum distance from origin and the final distance
3. Create a scatter plot with max distance on x-axis, final distance on y-axis
4. Repeat for 3D

**Questions:**
- Is max distance always larger than final distance? (It should be)
- What's the typical ratio?
- Does it differ between 2D and 3D?

---

## Challenge: Exploring Higher Dimensions

**Goal:** Understand the recurrence-transience threshold and what happens beyond.

### Exercise 5.7: Return Probability by Dimension

Test return probability for dimensions 1 through 10.

**What to do:**
1. For each dimension d = 1, 2, 3, ..., 10:
   - Run 150 walks, each up to 50,000 steps
   - Count how many return to origin
   - Calculate return probability
2. Plot return probability vs dimension

**Hints:**
- Use the `return_probability_nd()` function from simulations.py
- Expect: 1.0 for d=1,2; drops to ~0.34 for d=3; decreases further for d>3
- Higher dimensions will be computationally expensive; reduce walks as d increases if needed

**Questions:**
- Where is the "threshold"? Is it sharp or gradual?
- What happens for d=4, 5, 10?
- Can you sketch what you expect for d=100?

---

### Exercise 5.8: Understanding the Threshold

Create a detailed analysis around the critical dimension (d=2 to d=3).

**What to do:**
1. Run very careful simulations for d = 1.5 (not possible on grid, but think about it conceptually)
2. Focus on d = 2.0 (exact) and d = 3.0 (exact)
3. For each, run many walks (1000) to get good statistics
4. Plot return probability vs dimension with confidence intervals

**Hints:**
- This is computationally intensive; be patient
- Look for the sharpness of the transition
- Consider: why is there a sharp threshold at d=2.5?

**Questions:**
- Is the transition sharp or gradual?
- At what dimension does return probability drop below 50%?
- How would you describe the behavior to someone who doesn't know probability?

---

### Exercise 5.9: Visualize Dimensional Scaling

Compare how spread changes with dimension (beyond just average distance).

**What to do:**
1. For dimensions 1, 2, 3, 4, 5:
   - Run 2000 walks of 1000 steps each
   - Record all final distances
   - Calculate the full distribution (mean, median, quartiles, etc.)
2. Plot all 5 distributions overlaid or side-by-side

**Questions:**
- Do spreads increase with dimension?
- What's the relationship between dimension and distribution width?
- Is the shape (normal distribution) preserved across dimensions?

---

## Thought Experiments

**Goal:** Think deeply about dimension and probability without code.

### Exercise 5.10: The Intuition Problem

Explain in your own words why 2D and 3D are different for random walks.

**Think about:**
1. In 1D, you're on a line. Why must you return?
2. In 2D, you're on a plane. Is it obviously a difference from 1D?
3. In 3D, you're in space. Why does escape become likely?
4. What's the geometric reason for the threshold?

**Challenge:** Can you think of a physical analogy or mental image that explains the difference?

---

### Exercise 5.11: Lattice vs Continuous

Random walks on a grid are different from motion in continuous space. Discuss:

**Questions:**
1. Does our grid-based 2D walk behave the same as a continuous 2D random walk?
2. What differences might there be?
3. Does Pólya's theorem apply to continuous motion too?
4. Real Brownian motion is continuous. Does the recurrence property hold?

---

### Exercise 5.12: Real-World Dimension

Think about real phenomena and their "effective dimension."

**Consider:**
1. A bacterium diffusing through water (3D? or constrained somehow?)
2. A person wandering in a city (2D? constrained to streets?)
3. A molecule in a cell (3D but confined?)
4. Air pollution dispersing (3D)

**Questions:**
- Can you think of a system that's effectively 1D? 2D? 3D?
- Does the dimension determine recurrence?
- How would you test whether a real system is recurrent?

---

### Exercise 5.13: The 3D Bird Problem

You're in a 3D world and you get lost. Does the fact that return is only ~34% probable change how you think about being lost?

**Reflection:**
- In 1D (on a line), getting lost is not permanent—you'll find your way.
- In 2D (on a plane), same thing—recurrence guaranteed.
- In 3D, there's a 2 in 3 chance you wander forever.
- For a "drunk bird" in the sky, this is genuinely different from a "drunk man" on the ground.

**Think about:** What does this tell us about how dimension shapes probability and destiny?

---

## Open-Ended Explorations

### Exploration A: Dimension-Dependent Behavior

- What happens for fractional dimensions? (Theoretically, not on a grid—but what would we expect?)
- Can you find a formula for return probability as a function of dimension?
- Is there a sharp threshold or a smooth transition?

### Exploration B: Speed of Return

- How does the *expected return time* grow with dimension?
- Is the median return time different from the mean?
- Can you predict the distribution of return times?

### Exploration C: Multiple Dimensions

- Simulate walks that start in 3D but are constrained to a 2D plane (like constrained diffusion).
- Does this behave like true 2D or true 3D?
- What about walks in a 3D box with walls?

### Exploration D: Visualizing Recurrence

- Create an animation of a 2D walk, coloring each visited square with the number of times it's been visited.
- Do you see evidence of recurrence (all squares eventually visited)?
- Create the same animation for 3D (harder to visualize, but try!).

### Exploration E: The "Lost Forever" Threshold

- Compute more precisely: at what dimension does escape become likely?
- Is it exactly d=3, or does the transition happen at a different point?
- What's special about the critical dimension?

---

## Hints for Success

- **Visualization is key.** Plots reveal patterns that statistics hide.
- **Dimension matters more than you'd expect.** Small changes in dimension lead to dramatic changes in behavior.
- **Pólya's theorem is surprising.** Take time to let it sink in—the difference between "always return" and "probably escape" is profound.
- **Use simulations to build intuition.** Numbers help, but seeing paths and distributions makes the concepts stick.
- **Compare across dimensions systematically.** Don't jump from 1D to 3D; test 2D carefully to understand the threshold.

---

## Next Steps

Once you've worked through these exercises, you're ready for Chapter 6: **Random Walks in the Wild**. There, you'll leave the idealized grid world and meet random motion in real data: animal tracking, foraging, and complex environments.

See [solutions.md](solutions.md) when you want to compare your approaches or see alternative implementations.
