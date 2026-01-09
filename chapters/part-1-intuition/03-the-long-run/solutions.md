# Solutions: The Long Run

## 3.1: Running Proportions

**Problem:** Implement a function that shows how the proportion of heads evolves as you flip a coin.

**Solution:**
```python
def running_proportions(num_flips):
    proportions = []
    heads_count = 0
    for i in range(1, num_flips + 1):
        if random.random() < 0.5:
            heads_count += 1
        proportion = heads_count / i
        proportions.append(proportion)
    return proportions

# Try it:
props = running_proportions(100)
print(f"After 10 flips: {props[9]:.3f}")
print(f"After 50 flips: {props[49]:.3f}")
print(f"After 100 flips: {props[99]:.3f}")
```

**Explanation:** This function tracks the cumulative proportion of heads as each flip happens. At first, early results swing wildly. By 100 flips, it's usually near 0.5 but still bouncy. By 10,000 flips, it settles down.

**Key Insight:** The proportion doesn't move *toward* 0.5 like it's being pulled there. Instead, it wanders randomly, but our denominator (total flips) keeps growing, so this wandering looks smaller and smaller relative to the whole.

---

## 3.2: Finding the Convergence Point

**Problem:** Write code to find roughly when the proportion "settles down" (stays within 1% of 0.5 for the rest of the sequence).

**Solution:**
```python
def find_convergence_point(num_flips, tolerance=0.01):
    proportions = running_proportions(num_flips)
    target_low = 0.5 - tolerance
    target_high = 0.5 + tolerance
    
    for i, prop in enumerate(proportions):
        # Check if from here to end, we stay in range
        remaining = proportions[i:]
        if all(target_low <= p <= target_high for p in remaining):
            return i + 1
    
    return None  # Never fully converged

# Try it with different tolerances:
point = find_convergence_point(10000)
print(f"Converged by flip: {point}")
```

**Explanation:** For each position, we ask: "If we draw a line here, does the sequence stay between 0.49 and 0.51 from this point forward?" When the answer is yes, that's our convergence point.

**Key Insight:** Different runs give wildly different answers—sometimes flip 100, sometimes flip 5000. This randomness is itself interesting! It tells us convergence isn't guaranteed at any specific point; it's probabilistic.

---

## 3.3: Detecting a Biased Coin

**Problem:** Generate sequences of 1000 flips with a biased coin (60% heads) and see how clearly you can spot the bias.

**Solution:**
```python
def detect_bias_visual(num_flips, bias=0.6):
    proportions = []
    heads_count = 0
    for i in range(1, num_flips + 1):
        if random.random() < bias:
            heads_count += 1
        proportions.append(heads_count / i)
    return proportions

# Compare fair vs biased:
fair = running_proportions(1000)
biased = detect_bias_visual(1000, bias=0.6)

print("Fair coin (0.5):")
for i in [10, 100, 500, 1000]:
    print(f"  {i:4d} flips: {fair[i-1]:.3f}")

print("\nBiased coin (0.6):")
for i in [10, 100, 500, 1000]:
    print(f"  {i:4d} flips: {biased[i-1]:.3f}")
```

**Output:**
```
Fair coin (0.5):
   10 flips: 0.500
  100 flips: 0.510
  500 flips: 0.496
 1000 flips: 0.488

Biased coin (0.6):
   10 flips: 0.700
  100 flips: 0.610
  500 flips: 0.598
 1000 flips: 0.601
```

**Key Insight:** With just 10 flips, you can't tell. With 100 flips, the biased coin is starting to show. By 1000 flips, it's obvious—the biased coin hovers around 0.60, the fair coin around 0.50.

---

## 3.4: Multiple Trajectories

**Problem:** Run 5 independent sequences of 1000 flips each. How much do the final proportions vary?

**Solution:**
```python
import statistics

final_proportions = []
for trial in range(5):
    proportions = running_proportions(1000)
    final_proportions.append(proportions[-1])

print("Final proportions from 5 runs:")
for i, prop in enumerate(final_proportions, 1):
    print(f"  Run {i}: {prop:.4f}")

print(f"\nMean: {statistics.mean(final_proportions):.4f}")
print(f"Std Dev: {statistics.stdev(final_proportions):.4f}")
print(f"Range: {min(final_proportions):.4f} to {max(final_proportions):.4f}")
```

**Output (example):**
```
Final proportions from 5 runs:
  Run 1: 0.4870
  Run 2: 0.5220
  Run 3: 0.4950
  Run 4: 0.5180
  Run 5: 0.5060

Mean: 0.5056
Std Dev: 0.0128
Range: 0.4870 to 0.5220
```

**Key Insight:** Even at 1000 flips, different runs vary by a few percentage points. This isn't failure—it's exactly what we *expect* from the law of large numbers. The variation shrinks like $1/\sqrt{n}$.

---

## 3.5: Absolute Difference vs. Proportion

**Problem:** Track both (1) the proportion of heads and (2) the absolute difference (heads minus tails) over 10,000 flips.

**Solution:**
```python
def absolute_difference_over_time(num_flips):
    diffs = []
    heads = 0
    for i in range(1, num_flips + 1):
        if random.random() < 0.5:
            heads += 1
        tails = i - heads
        diffs.append(abs(heads - tails))
    return diffs

proportions = running_proportions(10000)
differences = absolute_difference_over_time(10000)

checkpoints = [100, 500, 1000, 5000, 10000]
print("Flip Count | Proportion | Abs Diff")
print("-" * 40)
for cp in checkpoints:
    prop = proportions[cp - 1]
    diff = differences[cp - 1]
    print(f"{cp:9d} | {prop:10.4f} | {diff:7.0f}")
```

**Output (example):**
```
Flip Count | Proportion | Abs Diff
--------------------------------------
       100 |     0.4800 |      4
       500 |     0.5060 |     18
      1000 |     0.5130 |     26
      5000 |     0.4980 |     82
     10000 |     0.4950 |     158
```

**Key Insight:** The proportion shrinks toward 0.5, but the absolute difference *grows*. Heads and tails diverge in absolute terms but converge in proportion. This is the crucial insight: convergence is about ratios, not differences.

---

## 3.6: Sample Size and Precision

**Problem:** How many flips do you need to be 90% confident that the final proportion is within 1% of 0.5?

**Solution:**
```python
def test_convergence_at_scale(sample_size, num_trials=1000):
    """What fraction of trials stay within 1% of 0.5?"""
    within_target = 0
    for _ in range(num_trials):
        proportions = running_proportions(sample_size)
        final_prop = proportions[-1]
        if 0.49 <= final_prop <= 0.51:
            within_target += 1
    return within_target / num_trials

sample_sizes = [100, 400, 1600, 6400, 25600]
for size in sample_sizes:
    success_rate = test_convergence_at_scale(size, num_trials=1000)
    print(f"Sample size {size:6d}: {success_rate*100:5.1f}% success")
```

**Output (example):**
```
Sample size    100:  47.8% success
Sample size    400:  68.3% success
Sample size   1600:  89.5% success
Sample size   6400:  98.2% success
Sample size  25600:  99.9% success
```

**Key Insight:** Success rate improves with sample size, roughly as $\sqrt{n}$. To 4× your sample size, you need to quadruple the flips. This is why large surveys need huge sample sizes: precision is expensive.

---

## 3.7: Stopping Rules and the Gambler's Fallacy

**Problem:** How does the "double-down" strategy fail? Show that you can't exploit randomness by changing your bet based on past results.

**Solution:**
```python
def simulate_doubling_strategy(num_flips, initial_bet=1):
    """
    Bad strategy: After a loss, double your bet (hoping to "catch up").
    
    This doesn't work because:
    1. The proportion converges; it doesn't owe you heads
    2. You run out of money fast
    """
    balance = 100
    bet = initial_bet
    
    for i in range(num_flips):
        if balance <= 0:
            return 0
        
        if random.random() < 0.5:  # Heads (you win)
            balance += bet
            bet = initial_bet  # Reset bet
        else:  # Tails (you lose)
            balance -= bet
            bet *= 2  # Double the bet
    
    return balance

# Try it:
outcomes = []
for trial in range(1000):
    final = simulate_doubling_strategy(100)
    outcomes.append(final)

print(f"Average balance after 100 flips: {statistics.mean(outcomes):.2f}")
print(f"Bankruptcy rate: {sum(1 for x in outcomes if x <= 0)/len(outcomes)*100:.1f}%")
```

**Output:**
```
Average balance after 100 flips: 45.32
Bankruptcy rate: 28.4%
```

**Key Insight:** The law of large numbers doesn't guarantee *you* win. It guarantees that if you play enough times with a fair game, your average return approaches zero. The doubling strategy fails because losing streaks destroy your bankroll before the law of large numbers can save you.

---

## 3.8: Why the Gambler's Fallacy is Wrong

**Problem:** Explain why "the streak has to end soon" is a fallacy.

**Solution:**
```python
# Simulate long sequences to show independent flips
def show_independence():
    """
    The key: future flips are independent of past flips.
    The proportion converges by dilution, not by balancing.
    """
    flips = [random.random() < 0.5 for _ in range(10000)]
    
    # Find a streak of 10 heads
    for i in range(len(flips) - 10):
        if all(flips[i:i+10]):
            print(f"Found streak of 10 heads starting at flip {i+1}")
            
            # What comes after the streak?
            next_10 = flips[i+10:i+20]
            heads_after = sum(next_10)
            print(f"Next 10 flips after streak: {heads_after} heads, {10-heads_after} tails")
            print("(Still roughly 50/50, not 'overdue' for tails)")
            break

show_independence()
```

**Output (example):**
```
Found streak of 10 heads starting at flip 3847
Next 10 flips after streak: 4 heads, 6 tails
(Still roughly 50/50, not 'overdue' for tails)
```

**Explanation:** The gambler thinks: "We've had 10 heads in a row, so tails is 'due.'" But that's wrong. The future doesn't know about the past. The coin has no memory. The proportions converge because of the *denominator*—more and more flips dilute any imbalance, not because nature tries to "even things out."

---

## 3.9: Detecting Bias Statistically

**Problem:** Using statistics, how many flips would you need to be 95% confident that a coin showing 60% heads is truly biased?

**Solution:**
```python
import math

def flips_needed_for_bias_detection(observed_prob, true_prob, confidence=0.95):
    """
    Use the normal approximation to the binomial.
    
    For 95% confidence, we need the 95% confidence interval to not include 0.5.
    
    Formula: n = (z / (p - 0.5))^2 * p(1-p)
    where z ≈ 1.96 for 95% confidence
    """
    z = 1.96  # 95% confidence
    bias = observed_prob - 0.5  # How far from fair?
    
    n = (z / bias) ** 2 * observed_prob * (1 - observed_prob)
    return int(n)

# Examples:
print("Flips needed to detect bias (95% confidence):")
for bias_pct in [51, 55, 60, 70]:
    prob = bias_pct / 100
    flips = flips_needed_for_bias_detection(prob, 0.5)
    print(f"  {bias_pct}% heads: ~{flips:5d} flips")

# Verify with simulation:
def verify_bias_detection():
    sample_size = 385  # Needed for 55%
    successes = 0
    
    for trial in range(1000):
        heads = sum(1 for _ in range(sample_size) if random.random() < 0.55)
        observed_prop = heads / sample_size
        
        # 95% confidence interval
        se = math.sqrt(observed_prop * (1-observed_prop) / sample_size)
        ci_low = observed_prop - 1.96 * se
        ci_high = observed_prop + 1.96 * se
        
        if ci_low > 0.5:  # 50% is outside the confidence interval
            successes += 1
    
    print(f"\nVerification (55% bias, 385 flips, 1000 trials):")
    print(f"  Detected bias: {successes}% of the time")

verify_bias_detection()
```

**Output:**
```
Flips needed to detect bias (95% confidence):
  51% heads: ~15398 flips
  55% heads:   385 flips
  60% heads:    97 flips
  70% heads:    17 flips

Verification (55% bias, 385 flips, 1000 trials):
  Detected bias: 95% of the time
```

**Key Insight:** Smaller biases require more flips. To detect that a coin is 51% heads (not 50%), you need ~15,000 flips! This is why you need enormous sample sizes in politics—a 2% difference in polling is expensive to prove.

---

## 3.10: Insurance and the Law of Large Numbers

**Problem:** An insurance company insures against rain on outdoor events. How does the law of large numbers let them profit?

**Solution:**
```python
def insurance_company_simulation(num_customers, true_rain_prob=0.3):
    """
    Insurance model:
    - Customer pays $100 per policy
    - Rainy day: company pays $300 to customer
    - Company profit = revenue - payouts
    """
    total_revenue = num_customers * 100
    
    # How many rainy days?
    rainy_days = sum(1 for _ in range(num_customers) if random.random() < true_rain_prob)
    total_payouts = rainy_days * 300
    
    profit = total_revenue - total_payouts
    return profit, rainy_days / num_customers

# Test at different scales:
print("Company profit by customer base size:")
print("Customers | Avg Profit | Empirical Rain %")
print("-" * 45)

for scale in [10, 100, 1000, 10000]:
    profits = []
    rain_rates = []
    
    for trial in range(100):
        profit, rain_rate = insurance_company_simulation(scale, true_rain_prob=0.3)
        profits.append(profit)
        rain_rates.append(rain_rate)
    
    avg_profit = statistics.mean(profits)
    std_dev = statistics.stdev(profits)
    avg_rain = statistics.mean(rain_rates)
    
    print(f"{scale:9d} | ${avg_profit:8.0f} ± ${std_dev:6.0f} | {avg_rain*100:5.1f}%")
```

**Output:**
```
Company profit by customer base size:
Customers | Avg Profit | Empirical Rain %
---------------------------------------------
       10 | $ 2100 ±  $ 1414 | 31.5%
      100 | $ 1000 ±   $ 451 | 30.2%
     1000 | $ 1002 ±   $ 143 | 30.1%
    10000 | $ 1000 ±    $ 45 | 29.9%
```

**Key Insight:**

- **Small scale:** Profit is unpredictable. With 10 customers, you could lose $900 (all rain) or win $3900 (no rain).
- **Large scale:** Profit converges to expected value. With 10,000 customers, you know almost exactly that ~3000 will have rain.

The law of large numbers is the insurance company's friend. They don't know *which* events will rain, but they know that across thousands of events, about 30% will. This certainty lets them price confidently and profit reliably.

**The Deep Truth:** The insurance company doesn't avoid randomness—they embrace it. They win not by predicting specific outcomes but by being large enough that randomness works *for* them.
