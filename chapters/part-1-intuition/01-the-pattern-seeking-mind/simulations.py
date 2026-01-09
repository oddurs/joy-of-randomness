"""
Simulations for Chapter 1: The Pattern-Seeking Mind

Demonstrations of the clustering illusion, birthday paradox,
and related phenomena in randomness.
"""

import random
import statistics
import matplotlib.pyplot as plt
from collections import Counter


def generate_random_points(num_points, seed=None):
    """
    Generate random points uniformly distributed in [0,1] × [0,1].
    
    Args:
        num_points: Number of points to generate
        seed: Random seed for reproducibility
    
    Returns:
        List of (x, y) tuples
    """
    if seed is not None:
        random.seed(seed)
    return [(random.random(), random.random()) for _ in range(num_points)]


def plot_random_points(num_points=200, title="Random Points in a Square"):
    """
    Generate and visualize random points.
    
    Args:
        num_points: Number of points to plot
        title: Title for the plot
    """
    points = generate_random_points(num_points)
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=30, alpha=0.6, color='steelblue')
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.gca().set_aspect('equal')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()


def longest_streak(flips):
    """
    Find the length of the longest consecutive sequence of the same result.
    
    Args:
        flips: List of 'H' (heads) or 'T' (tails)
    
    Returns:
        Integer: length of longest streak
    """
    if not flips:
        return 0
    
    max_streak = 1
    current_streak = 1
    
    for i in range(1, len(flips)):
        if flips[i] == flips[i-1]:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    
    return max_streak


def simulate_coin_flips(num_flips, num_simulations=10000):
    """
    Run many coin flip simulations and analyze longest streaks.
    
    Args:
        num_flips: Number of flips per simulation
        num_simulations: Number of simulations to run
    
    Returns:
        Dictionary with statistics about streaks
    """
    streaks = []
    
    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(num_flips)]
        streaks.append(longest_streak(flips))
    
    return {
        'mean': statistics.mean(streaks),
        'median': statistics.median(streaks),
        'stdev': statistics.stdev(streaks),
        'min': min(streaks),
        'max': max(streaks),
        'distribution': streaks
    }


def plot_streak_distribution(num_flips=100, num_simulations=10000):
    """
    Generate and plot the distribution of longest streaks.
    
    Args:
        num_flips: Number of flips per simulation
        num_simulations: Number of simulations to run
    """
    results = simulate_coin_flips(num_flips, num_simulations)
    
    plt.figure(figsize=(10, 6))
    plt.hist(results['distribution'], bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(results['mean'], color='red', linestyle='--', 
                linewidth=2, label=f"Mean: {results['mean']:.1f}")
    plt.axvline(results['median'], color='green', linestyle='--', 
                linewidth=2, label=f"Median: {results['median']:.0f}")
    plt.xlabel("Length of Longest Streak")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Longest Streaks in {num_flips} Coin Flips\n(10,000 simulations)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f"Results for {num_flips} coin flips:")
    print(f"  Mean longest streak: {results['mean']:.2f}")
    print(f"  Median: {results['median']:.0f}")
    print(f"  Std dev: {results['stdev']:.2f}")
    print(f"  Range: {results['min']} to {results['max']}")


def compare_human_vs_random(human_sequence_str, num_simulations=1000):
    """
    Compare a human-generated sequence to random sequences.
    
    Args:
        human_sequence_str: String of H and T (e.g., "HTHHTTHH...")
        num_simulations: Number of random sequences to generate
    
    Returns:
        Dictionary with comparison statistics
    """
    human_flips = list(human_sequence_str.upper())
    human_longest = longest_streak(human_flips)
    human_h_count = human_flips.count('H')
    
    # Generate random sequences of same length
    random_streaks = []
    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(len(human_flips))]
        random_streaks.append(longest_streak(flips))
    
    return {
        'human_longest_streak': human_longest,
        'human_heads_count': human_h_count,
        'human_heads_percent': 100 * human_h_count / len(human_flips),
        'random_mean_streak': statistics.mean(random_streaks),
        'random_streaks': random_streaks
    }


def birthday_probability(num_people):
    """
    Calculate probability that at least two people share a birthday.
    
    Using the complement: P(at least one match) = 1 - P(no matches)
    
    Args:
        num_people: Number of people in the group
    
    Returns:
        Probability (0 to 1)
    """
    # Probability that all birthdays are different
    prob_no_match = 1.0
    for i in range(num_people):
        prob_no_match *= (365 - i) / 365
    
    return 1 - prob_no_match


def simulate_birthdays(num_people, num_simulations=10000):
    """
    Simulate birthday problem to verify calculation.
    
    Args:
        num_people: Number of people in each simulation
        num_simulations: Number of simulations
    
    Returns:
        Fraction of simulations with at least one match
    """
    matches = 0
    
    for _ in range(num_simulations):
        birthdays = [random.randint(1, 365) for _ in range(num_people)]
        if len(set(birthdays)) < len(birthdays):  # Duplicate found
            matches += 1
    
    return matches / num_simulations


def plot_birthday_problem():
    """
    Plot the probability of shared birthdays as group size increases.
    """
    group_sizes = range(2, 101)
    probabilities = [birthday_probability(n) for n in group_sizes]
    
    plt.figure(figsize=(10, 6))
    plt.plot(group_sizes, probabilities, linewidth=2, color='steelblue')
    plt.axhline(0.5, color='red', linestyle='--', alpha=0.5, label='50%')
    plt.axvline(23, color='green', linestyle='--', alpha=0.5, label='23 people')
    plt.xlabel("Number of People")
    plt.ylabel("Probability of Shared Birthday")
    plt.title("The Birthday Paradox")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
    
    # Print some key values
    print("Birthday Problem - Key Values:")
    for n in [10, 23, 30, 50, 70, 100]:
        prob = birthday_probability(n)
        print(f"  {n:3d} people: {prob:.1%} chance of shared birthday")


def count_runs(flips):
    """
    Count the number of "runs" (transitions between H and T).
    
    Args:
        flips: List of 'H' or 'T'
    
    Returns:
        Number of runs
    """
    if not flips:
        return 0
    
    runs = 1
    for i in range(1, len(flips)):
        if flips[i] != flips[i-1]:
            runs += 1
    
    return runs


def analyze_clustering_in_grid(points, num_cells=10):
    """
    Check for clustering by dividing space into a grid.
    
    Args:
        points: List of (x, y) tuples in [0,1] × [0,1]
        num_cells: Side length of grid (num_cells × num_cells)
    
    Returns:
        Dictionary with clustering statistics
    """
    # Initialize grid
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    
    # Count points in each cell
    for x, y in points:
        cell_x = int(x * num_cells)
        cell_y = int(y * num_cells)
        # Handle edge case
        cell_x = min(cell_x, num_cells - 1)
        cell_y = min(cell_y, num_cells - 1)
        grid[cell_x][cell_y] += 1
    
    # Analyze distribution
    counts = []
    for row in grid:
        counts.extend(row)
    
    expected_per_cell = len(points) / (num_cells * num_cells)
    
    return {
        'expected_per_cell': expected_per_cell,
        'mean_count': statistics.mean(counts),
        'max_count': max(counts),
        'min_count': min(counts),
        'counts': counts
    }


def demonstrate_clustering_illusion():
    """
    Generate random points and show how clustering can look suspicious.
    """
    print("Clustering Illusion Demonstration")
    print("=" * 50)
    
    num_points = 200
    points = generate_random_points(num_points)
    
    analysis = analyze_clustering_in_grid(points, num_cells=10)
    
    print(f"Generated {num_points} random points in a 10×10 grid")
    print(f"Expected points per cell: {analysis['expected_per_cell']:.1f}")
    print(f"Actual statistics:")
    print(f"  Mean per cell: {analysis['mean_count']:.1f}")
    print(f"  Max per cell: {analysis['max_count']}")
    print(f"  Min per cell: {analysis['min_count']}")
    print()
    print("This is randomness at work. Clustering is inevitable!")


if __name__ == "__main__":
    # Run demonstrations
    print("Chapter 1: The Pattern-Seeking Mind")
    print("=" * 50)
    print()
    
    # Streak analysis
    print("Longest Streak Analysis (100 flips, 10,000 simulations):")
    results = simulate_coin_flips(100, 10000)
    print(f"  Mean: {results['mean']:.2f}")
    print(f"  Median: {results['median']:.0f}")
    print(f"  Range: {results['min']} to {results['max']}")
    print()
    
    # Birthday paradox
    print("Birthday Problem:")
    for n in [23, 50, 70]:
        prob = birthday_probability(n)
        print(f"  {n} people: {prob:.1%}")
    print()
    
    # Clustering illusion
    demonstrate_clustering_illusion()

