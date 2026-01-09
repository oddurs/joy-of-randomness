# Exercises for Chapter 4: The Drunkard's Walk

These exercises guide you through progressively deeper exploration of random walks. Start with the warm-up, then move through exploration, challenge, and thought experiments at your own pace.

---

## Warm-up: Generate and Analyze

**Goal:** Build confidence with basic simulation and observe the data.

### Exercise 4.1: Plot a Single Walk

Generate a random walk of 1000 steps and plot it. 

**What to do:**
1. Use the `simulate_random_walk()` function from `simulations.py` (or write your own)
2. Plot the position history
3. Record: final position, maximum distance from origin, minimum distance

**Questions:**
- How far did the walker end up from the starting point?
- Did the walker ever return to zero? If so, how many times?
- What was the farthest point reached?

---

### Exercise 4.2: Repeat the Experiment

Run the same simulation (1000 steps) five times.

**What to do:**
1. Generate five separate walks, each 1000 steps
2. Plot all five walks on the same figure with different colors
3. Record the final position for each walk

**Questions:**
- How different are the final positions?
- What's the range of values you see?
- If you ran 100 more walks, what would you expect the final positions to look like?

---

### Exercise 4.3: The Distribution

Generate 10,000 random walks of 100 steps each and look at the distribution of final positions.

**What to do:**
1. Run 10,000 walks, each 100 steps
2. Collect the final position from each walk
3. Plot a histogram of final positions
4. Calculate: mean, median, standard deviation

**Questions:**
- What's the center of the distribution?
- What's the spread (standard deviation)?
- How does the spread compare to √100 = 10?
- Is the distribution symmetric?

---

## Exploration: Dig Deeper

**Goal:** Discover relationships and patterns. Expect to write more code here.

### Exercise 4.4: The √n Relationship

Test whether the standard deviation truly scales as √n.

**What to do:**
1. For each of these step counts: [10, 50, 100, 500, 1000, 5000], run 5000 walks
2. For each, calculate the standard deviation of final positions
3. Calculate √n for each step count
4. Plot both observed and theoretical on the same graph (try log-log scale)

**Hints:**
- Use the `test_sqrt_n_scaling()` function from simulations.py, or compute it yourself
- A log-log plot will show if they follow a power law
- If they match, the ratio should be close to 1

**Questions:**
- How well does √n predict the observed standard deviation?
- What's the ratio between observed and theoretical at each step count?
- Does the agreement improve, stay the same, or worsen as you increase n?

---

### Exercise 4.5: First Returns

Track when walkers return to the origin.

**What to do:**
1. Run 1000 walks, each until the walker returns to position 0 (set a maximum like 100,000 steps)
2. Record how many steps it took for each return
3. Plot a histogram of return times (use log scale on both axes)
4. Report: minimum, median, mean, maximum

**Hints:**
- Every walk should return eventually in 1D (with very high probability)
- Use the `first_return_time()` function from simulations.py
- The distribution will have a long tail (some very late returns)

**Questions:**
- What's the typical return time?
- How rare are very late returns?
- Do any walks not return within 100,000 steps? How many?
- Can you explain why some returns are so fast (near 2)?

---

### Exercise 4.6: Maximum Distance

Does the walker's maximum distance from origin relate to the number of steps?

**What to do:**
1. Run 1000 walks, each 1000 steps
2. For each walk, track the maximum distance from origin reached (not just final position)
3. Compute statistics: mean, median, standard deviation of max distances
4. Compare to the standard deviation of final positions

**Hints:**
- Use the `maximum_distance_reached()` function from simulations.py
- Both final position and max distance are random, but they may have different scales

**Questions:**
- On average, how far does the walker drift?
- Is the max distance always larger than the final position? (It should be.)
- How do the standard deviations compare?

---

## Challenge: Deep Understanding

**Goal:** Apply multiple concepts and discover new insights.

### Exercise 4.7: Step Size Variations

What happens if the step size isn't always ±1?

**What to do:**
1. Run 5000 walks of 1000 steps each with steps of ±2 (double the usual size)
2. Run 5000 walks of 1000 steps with the custom steps: [-1 (probability 0.5), +3 (probability 0.5)]
3. Compare the resulting distributions to the baseline (±1 steps)
4. Plot histograms side by side

**Hints:**
- Use `simulate_random_walk_custom_steps()` from simulations.py
- The spread should scale with the step size
- The shape should still be roughly normal (Central Limit Theorem)

**Questions:**
- How does doubling the step size affect the spread of final positions?
- How does using steps [-1, +3] instead of [-1, +1] change the distribution?
- Is the mean still at zero? Why or why not?
- Can you predict the new standard deviations based on variance calculations?

---

### Exercise 4.8: Biased Walks

What happens when the walk is biased (more likely to go in one direction)?

**What to do:**
1. Run 10,000 walks of 1000 steps each where P(+1) = 0.6 and P(-1) = 0.4
2. Run another 10,000 with P(+1) = 0.7 and P(-1) = 0.3
3. Also run a fair walk (P(+1) = 0.5) for comparison
4. Plot all three distributions

**Hints:**
- Use `simulate_biased_random_walk()` from simulations.py
- The mean will shift away from zero
- The spread might change too (think about variance)

**Questions:**
- Where is the center of each distribution?
- What's the relationship between the bias (p_forward) and the mean final position?
- How does the standard deviation change with bias?
- Can you predict both the mean and standard deviation for a given bias?

---

### Exercise 4.9: Zero Crossings

How often does a random walk cross zero?

**What to do:**
1. Run 1000 walks of 1000 steps each
2. For each walk, count how many times it crosses zero (changes sign)
3. Plot a histogram of crossing counts
4. Compute average crossings per walk

**Hints:**
- Use the `count_zero_crossings()` function from simulations.py, or write your own
- A crossing happens when the sign changes from positive to negative or vice versa
- The walker starts at zero, so the first crossing is when it first leaves zero

**Questions:**
- What's the typical number of zero crossings?
- Are there walks with very few crossings? Very many?
- Do you expect the number of crossings to increase with walk length? How?

---

## Thought Experiments

**Goal:** Think conceptually, no code required (though you can verify with simulation if curious).

### Exercise 4.10: The Prediction Problem

Imagine you watch a random walk for 100 steps and observe that the walker is at position +30.

**Questions:**
1. What would you guess the walker's position will be after another 100 steps?
2. How confident are you in that guess?
3. How would you predict if the walker will be closer to zero or farther from zero after those next 100 steps?

**Hint:** Think about the independence of steps. After 100 steps, the walker's "next 100 steps" are independent of where they currently are.

---

### Exercise 4.11: The Escape Problem

Consider a walker in 1D who *always* returns to origin (we proved this).

**Questions:**
1. If we move to 2D (where the walker can go up/down/left/right), will the walker still always return home?
2. If we move to 3D, what do you think happens?
3. What's your intuition: as dimensions increase, does return become more likely or less likely?

**Hint:** In higher dimensions, there's "more space." Does that help or hurt a wanderer trying to find their way home?

---

### Exercise 4.12: The √n Intuition

Why does spread grow like √n and not n?

**Think about:**
1. If each step is ±1, the total distance is the sum of n random ±1's.
2. If the steps were *all* the same direction, how far would you be? (This is the upper bound.)
3. But they're random, so they cancel out. Why doesn't this cancellation bring you closer to zero?
4. Intuitively, what does √n scaling mean? Is it fast or slow growth?

**Challenge:** Can you explain in words why variances add but standard deviations don't?

---

### Exercise 4.13: Real-World Intuition

Consider these scenarios. Which behave like random walks? Why or why not?

1. A stock price over a year
2. Your bank account balance (with random deposits and withdrawals)
3. A person's position in a crowded room
4. The number of bacteria in a petri dish
5. A river's water level over a year
6. Daily temperature variations

**Think about:**
- What's the "step" in each scenario?
- Are steps independent?
- Are steps random?
- Are there external influences (trend, seasonality, memory)?

---

## Exploration Ideas

If you want to go further, try these open-ended explorations:

1. **Custom Step Distributions:** What if steps are normally distributed? Exponentially distributed? Uniform from -2 to +2?

2. **The Arcsine Law:** A strange result: a random walk spends most of its time on one side of zero. Can you observe this? (Plot where the walker is positive vs. negative over the course of a walk.)

3. **Recurrence in 2D:** We showed 1D is recurrent. Write a 2D random walk and estimate the return probability. Does it match the theoretical ~0.34?

4. **Brownian Bridges:** What if you condition a walk to end at a specific position (say, 0)? How does that constrain its path?

5. **Multiple Particles:** Simulate 100 particles doing random walks. Track how the distance between pairs grows over time. How does that relate to √n?

---

## Hints for Success

- **Start simple:** Before testing complex ideas, make sure you understand the basic simulation.
- **Visualize:** Plots often reveal patterns that numbers hide.
- **Compare to theory:** We derived √n scaling. Check if your data matches.
- **Ask questions:** Every result should trigger a "why?" or "what if?"
- **Reuse code:** The simulations.py module is your friend. Use it liberally.

---

## Next Steps

Once you've worked through these exercises, you're ready for Chapter 5: **Wandering in Two Dimensions**. There, random walks get visually interesting—and mathematically surprising.

See [solutions.md](solutions.md) when you want to compare your work or see different approaches.
