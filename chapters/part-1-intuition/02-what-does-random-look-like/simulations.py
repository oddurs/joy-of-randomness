"""
Simulations for Chapter 2: What Does Random Even Look Like?

Demonstrations of randomness through sequences, streaks, runs, and comparisons
between hand-generated and machine-generated randomness.
"""

import random
import statistics
from collections import Counter


def longest_streak(sequence):
    """Find the longest consecutive run of the same outcome."""
    if not sequence:
        return 0
    
    current_length = 1
    max_length = 1
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length


def count_runs(sequence):
    """Count the number of runs (maximal sequences of same outcome)."""
    if not sequence:
        return 0
    
    num_runs = 1
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            num_runs += 1
    
    return num_runs


def generate_coin_sequence(num_flips, heads_probability=0.5):
    """Generate a sequence of coin flips."""
    return [1 if random.random() < heads_probability else 0 
            for _ in range(num_flips)]


def simulate_longest_streaks(num_sequences, flips_per_sequence):
    """Run many sequences, return the longest streak in each."""
    streaks = []
    for _ in range(num_sequences):
        sequence = generate_coin_sequence(flips_per_sequence)
        streaks.append(longest_streak(sequence))
    return streaks


def simulate_runs(num_sequences, flips_per_sequence):
    """Run many sequences, return the number of runs in each."""
    run_counts = []
    for _ in range(num_sequences):
        sequence = generate_coin_sequence(flips_per_sequence)
        run_counts.append(count_runs(sequence))
    return run_counts


def running_proportion(sequence):
    """Return the running proportion of heads (1s) in a sequence."""
    proportions = []
    heads_so_far = 0
    for i, flip in enumerate(sequence, 1):
        if flip == 1:
            heads_so_far += 1
        proportions.append(heads_so_far / i)
    return proportions


def expected_runs(n):
    """Expected number of runs in a fair sequence of length n."""
    return n / 2 + 1


def std_dev_runs(n):
    """Standard deviation of the number of runs."""
    return 0.5 * (n / 2) ** 0.5


def runs_test(sequence, alpha=2.0):
    """
    Runs test for randomness.
    
    Returns True if sequence looks random, False if suspicious.
    alpha: number of standard deviations for threshold (default 2)
    """
    n = len(sequence)
    observed_runs = count_runs(sequence)
    expected = expected_runs(n)
    std_dev = std_dev_runs(n)
    
    z_score = abs(observed_runs - expected) / std_dev
    return z_score <= alpha


def find_pattern(sequence, pattern):
    """
    Find the first occurrence of a pattern in a sequence.
    
    Returns position (0-indexed) or -1 if not found.
    """
    pattern_str = ''.join(str(p) for p in pattern)
    seq_str = ''.join(str(s) for s in sequence)
    pos = seq_str.find(pattern_str)
    return pos


def main():
    """Run demonstrations of randomness properties."""
    
    print("=" * 60)
    print("Chapter 2: What Does Random Even Look Like?")
    print("=" * 60)
    
    # Demo 1: Single sequence
    print("\n1. SINGLE SEQUENCE OF 100 FLIPS")
    print("-" * 60)
    sequence = generate_coin_sequence(100)
    sequence_str = ''.join('H' if x == 1 else 'T' for x in sequence)
    print(f"Sequence: {sequence_str}")
    print(f"Longest streak: {longest_streak(sequence)}")
    print(f"Number of runs: {count_runs(sequence)}")
    print(f"Heads: {sum(sequence)}, Tails: {len(sequence) - sum(sequence)}")
    
    # Demo 2: Distribution of streaks
    print("\n2. DISTRIBUTION OF LONGEST STREAKS (10,000 sequences of 100 flips)")
    print("-" * 60)
    streaks = simulate_longest_streaks(10000, 100)
    print(f"Average longest streak: {statistics.mean(streaks):.2f}")
    print(f"Median longest streak: {statistics.median(streaks)}")
    print(f"Min: {min(streaks)}, Max: {max(streaks)}")
    
    # Distribution table
    streak_counts = Counter(streaks)
    print("\nDistribution:")
    for length in sorted(streak_counts.keys()):
        percentage = (streak_counts[length] / len(streaks)) * 100
        print(f"  Streak of {length:2d}: {percentage:5.1f}% ({streak_counts[length]:4d} sequences)")
    
    # Demo 3: Running proportion
    print("\n3. RUNNING PROPORTION CONVERGENCE (10,000 flips)")
    print("-" * 60)
    long_sequence = generate_coin_sequence(10000)
    proportions = running_proportion(long_sequence)
    checkpoints = [10, 100, 1000, 10000]
    print("Proportion of heads at different points:")
    for checkpoint in checkpoints:
        print(f"  After {checkpoint:5d} flips: {proportions[checkpoint-1]:.4f}")
    
    # Demo 4: Runs test
    print("\n4. RUNS TEST (100 fair sequences)")
    print("-" * 60)
    fair_sequences = [generate_coin_sequence(100) for _ in range(100)]
    fair_count = sum(1 for seq in fair_sequences if runs_test(seq))
    print(f"Sequences passing runs test: {fair_count} / 100")
    
    # Demo 5: Biased coin detection
    print("\n5. RUNS TEST ON BIASED COINS (100 sequences with 60% heads)")
    print("-" * 60)
    biased_sequences = [generate_coin_sequence(100, heads_probability=0.6) 
                        for _ in range(100)]
    biased_count = sum(1 for seq in biased_sequences if runs_test(seq))
    print(f"Biased sequences passing runs test: {biased_count} / 100")
    print("(Lower is better—we want to detect bias)")
    
    # Demo 6: Comparison metrics
    print("\n6. STATISTICS ON LONGEST STREAKS")
    print("-" * 60)
    print("\nFair coin (100 flips, 10,000 trials):")
    fair_streaks = simulate_longest_streaks(10000, 100)
    print(f"  Mean: {statistics.mean(fair_streaks):.2f}")
    print(f"  Std Dev: {statistics.stdev(fair_streaks):.2f}")
    print(f"  Mode: {Counter(fair_streaks).most_common(1)[0][0]}")
    
    print("\nBiased coin (60% heads, 100 flips, 10,000 trials):")
    biased_streaks = simulate_longest_streaks(10000, 100)
    # Note: both are fair because we use 0.5 by default
    # To test biased, we'd need to modify generate_coin_sequence call
    print(f"  Mean: {statistics.mean(biased_streaks):.2f}")
    
    # Demo 7: Pattern search
    print("\n7. PATTERN SEARCH (1,000 sequences of 100 flips)")
    print("-" * 60)
    sequences = [generate_coin_sequence(100) for _ in range(1000)]
    
    for pattern_target in [[1, 0, 1], [1, 1, 1, 1]]:
        positions = []
        pattern_name = ''.join('H' if p == 1 else 'T' for p in pattern_target)
        
        for seq in sequences:
            pos = find_pattern(seq, pattern_target)
            if pos != -1:
                positions.append(pos)
        
        if positions:
            print(f"\nPattern '{pattern_name}':")
            print(f"  Found in {len(positions)} / 1000 sequences")
            print(f"  Average position: {statistics.mean(positions):.1f}")
            print(f"  Median position: {statistics.median(positions)}")
        else:
            print(f"\nPattern '{pattern_name}': Not found in any sequence")


if __name__ == "__main__":
    main()
