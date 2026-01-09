# Exercises: The Long Run

---

## 3.1: Running Proportion (Warm-up)

Write a function `running_proportions(num_flips)` that simulates coin flips and returns a list of the proportion of heads after each flip.

Test it on 100 flips. Print key checkpoints: after 10, 50, and 100 flips. Does the proportion stabilize? How much does it bounce around?

---

## 3.2: Spotting Convergence (Warm-up)

Run the simulation for 10,000 flips. At what point does the proportion stay within 1% of 0.5 (i.e., between 0.49 and 0.51) *for the rest of the simulation*? Is it at 100 flips? 1,000 flips?

Run this experiment multiple times. Does the convergence point vary?

---

## 3.3: Biased Coin Detection (Exploration)

Modify your simulation to use a biased coin (60% heads, 40% tails). Run it for 10,000 flips.

Track the running proportion. How long does it take for the convergence to reveal the bias? At what point would a statistician be confident the coin isn't fair?

---

## 3.4: Multiple Trajectories (Exploration)

Run the fair coin simulation 5 times, each for 1,000 flips. Describe the behavior of all 5 trajectories.

Do they all converge to 0.5? Do they all follow the same path? What does this tell you about randomness and determinism?

---

## 3.5: Absolute Difference (Challenge)

The proportion of heads converges to 0.5, but the absolute difference $|\text{heads} - \text{tails}|$ doesn't converge to 0.

Simulate 100,000 coin flips. Track both:
- The running proportion of heads
- The absolute difference (heads minus tails) at each step

How do they behave differently?

---

## 3.6: Sample Size and Precision (Challenge)

You want to estimate the probability of heads for a coin by flipping it and observing the proportion.

How many flips do you need to be 95% confident that your estimate is within 1% of the true value (i.e., between 0.49 and 0.51)?

Design an experiment: try sample sizes of 100, 400, 1,600, 6,400, and 25,600 flips. For each size, run 1,000 simulations. Record how many times the final proportion landed in the target range.

---

## 3.7: Stopping Rules (Challenge)

Suppose you flip a coin and want to stop once you're 95% confident it's fair (proportion within 1% of 0.5).

Implement a simulation that flips until convergence, then records how many flips were needed. Run this 1,000 times. What's the distribution of stopping times? Do some simulations take much longer than others?

---

## 3.8: The Gambler's Fallacy Trap (Thought Experiment)

You flip a coin 10 times and get 8 heads, 2 tails. You're convinced tails is "due."

You flip 10 more times. What's the expected proportion of heads in those 10 new flips? Why doesn't the first batch's imbalance affect the second batch?

---

## 3.9: Detecting Bias with Confidence (Challenge)

Suppose a casino gives you 100 flips from their "fair" coin. You observe 65 heads, 35 tails.

Should you be suspicious? At what proportion of heads would you become 95% confident the coin is biased (not 50/50)?

Hint: for a fair coin with n flips, the standard deviation of the proportion is approximately $\sqrt{p(1-p)/n}$, where p=0.5.

---

## 3.10: Insurance and the Law of Large Numbers (Thought Experiment)

An insurance company sells 1,000,000 policies. Each policy has a 1% chance of a claim worth \\$10,000 this year.

The company needs to charge enough so that their expected payout is less than their expected revenue.

Estimate the expected total payout for the year. If the company charges \\$120 per policy, what's their expected profit? Why does the law of large numbers make this profitable?
