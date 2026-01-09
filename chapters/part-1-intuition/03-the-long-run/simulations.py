"""
Simulations for Chapter 3: The Long Run

Demonstrations of the law of large numbers, convergence, and how proportions
stabilize as we accumulate more data.
"""

import random
import statistics
import math


def running_proportions(num_flips, heads_probability=0.5):
    """
    Simulate coin flips and return the proportion of heads after each flip.

    Returns a list where element i is the proportion of heads after i+1 flips.
    """
    proportions = []
    heads_so_far = 0

    for i in range(1, num_flips + 1):
        if random.random() < heads_probability:
            heads_so_far += 1
        proportion = heads_so_far / i
        proportions.append(proportion)

    return proportions


def absolute_difference(num_flips, heads_probability=0.5):
    """
    Simulate coin flips and return the absolute difference (heads - tails) after each flip.
    """
    differences = []
    heads_so_far = 0

    for i in range(1, num_flips + 1):
        if random.random() < heads_probability:
            heads_so_far += 1
        tails_so_far = i - heads_so_far
        diff = heads_so_far - tails_so_far
        differences.append(abs(diff))

    return differences


def find_convergence_point(num_flips, target_range=0.01, heads_probability=0.5):
    """
    Find the first point where proportion stays within target_range of 0.5.

    Returns (position, stabilized) where position is the number of flips and stabilized
    is True if it stayed in range for the rest of the simulation.
    """
    proportions = running_proportions(num_flips, heads_probability)
    target_low = 0.5 - target_range
    target_high = 0.5 + target_range

    for i, prop in enumerate(proportions):
        remaining = proportions[i:]
        if all(target_low <= p <= target_high for p in remaining):
            return i + 1, True

    return len(proportions), False


def convergence_test(sample_size, num_trials, target_range=0.01):
    """
    Run multiple simulations and check convergence at a given sample size.

    Returns the proportion of trials where the final proportion was in target range.
    """
    in_range_count = 0

    for _ in range(num_trials):
        proportions = running_proportions(sample_size)
        final_prop = proportions[-1]

        target_low = 0.5 - target_range
        target_high = 0.5 + target_range

        if target_low <= final_prop <= target_high:
            in_range_count += 1

    return in_range_count / num_trials


def detect_bias_required_flips(bias, z_score=1.96):
    """
    Estimate how many flips are needed to detect a given bias.

    Uses the formula: n = z^2 * p(1-p) / (bias)^2

    Args:
        bias: Difference from 0.5 you want to detect (e.g., 0.05 for 55% vs 50%)
        z_score: Critical value (1.96 for 95% confidence)
    """
    p = 0.5
    n = (z_score ** 2) * p * (1 - p) / (bias ** 2)
    return int(n)


def main():
    """Run demonstrations of convergence and the law of large numbers."""

    print("=" * 70)
    print("Chapter 3: The Long Run")
    print("=" * 70)

    # Demo 1: Single trajectory
    print("\n1. SINGLE TRAJECTORY (1000 flips)")
    print("-" * 70)
    proportions = running_proportions(1000)
    checkpoints = [10, 50, 100, 500, 1000]
    print("Running proportion of heads at key points:")
    for cp in checkpoints:
        print(f"  After {cp:4d} flips: {proportions[cp-1]:.4f}")

    # Demo 2: Multiple trajectories
    print("\n2. MULTIPLE TRAJECTORIES (5 runs of 1000 flips)")
    print("-" * 70)
    for run in range(1, 6):
        proportions = running_proportions(1000)
        final = proportions[-1]
        max_val = max(proportions[:50])
        min_val = min(proportions[:50])
        print(f"  Run {run}: Final proportion = {final:.4f}, "
              f"Range in first 50: [{min_val:.2f}, {max_val:.2f}]")

    # Demo 3: Convergence point detection
    print("\n3. CONVERGENCE POINT (staying within 1% of 0.5)")
    print("-" * 70)
    convergence_points = []
    for run in range(1, 6):
        point, stabilized = find_convergence_point(10000, target_range=0.01)
        convergence_points.append(point)
        status = "yes" if stabilized else "no"
        print(f"  Run {run}: Converged at flip {point:5d} (stabilized: {status})")
    print(f"  Average convergence point: {statistics.mean(convergence_points):.0f}")

    # Demo 4: Proportion vs. absolute difference
    print("\n4. PROPORTION VS. ABSOLUTE DIFFERENCE (10000 flips)")
    print("-" * 70)
    proportions = running_proportions(10000)
    diffs = absolute_difference(10000)
    checkpoints = [100, 1000, 5000, 10000]
    print("Proportion and absolute difference at key points:")
    for cp in checkpoints:
        prop = proportions[cp - 1]
        diff = diffs[cp - 1]
        print(f"  After {cp:5d} flips: Proportion = {prop:.4f}, "
              f"Absolute difference = {diff:3.0f}")

    # Demo 5: Biased coin convergence
    print("\n5. BIASED COIN DETECTION (60% heads, 10000 flips)")
    print("-" * 70)
    proportions_biased = running_proportions(10000, heads_probability=0.6)
    checkpoints = [100, 500, 1000, 5000, 10000]
    print("Biased coin (true proportion = 0.6):")
    for cp in checkpoints:
        prop = proportions_biased[cp - 1]
        print(f"  After {cp:5d} flips: {prop:.4f}")

    # Demo 6: Sample size requirements
    print("\n6. CONVERGENCE BY SAMPLE SIZE (1000 trials each)")
    print("-" * 70)
    sample_sizes = [100, 400, 1600, 6400, 25600]
    print("Proportion of trials ending within 1% of 0.5:")
    for size in sample_sizes:
        success_rate = convergence_test(size, 1000, target_range=0.01)
        print(f"  Sample size {size:5d}: {success_rate*100:5.1f}% success")

    # Demo 7: Required flips to detect bias
    print("\n7. FLIPS NEEDED TO DETECT BIAS (95% confidence)")
    print("-" * 70)
    print("To distinguish from a fair coin (50%) with 95% confidence:")
    biases = [0.05, 0.10, 0.20]
    for bias in biases:
        needed = detect_bias_required_flips(bias)
        pct = 50 + (bias * 100)
        print(f"  To detect {pct:.0f}% heads: ~{needed:6d} flips")

    # Demo 8: The gambler's fallacy
    print("\n8. INDEPENDENCE OF FLIPS")
    print("-" * 70)
    batch1_heads = sum([1 for _ in range(100) if random.random() < 0.5])
    batch2_heads = sum([1 for _ in range(100) if random.random() < 0.5])

    print(f"Batch 1 (100 flips): {batch1_heads} heads, {100-batch1_heads} tails")
    print(f"Batch 2 (100 flips): {batch2_heads} heads, {100-batch2_heads} tails")
    print(f"Batch 1 proportion: {batch1_heads/100:.2f}")
    print(f"Batch 2 proportion: {batch2_heads/100:.2f}")
    print("(Batch 2 doesn't try to 'balance out' Batch 1)")


if __name__ == "__main__":
    main()
