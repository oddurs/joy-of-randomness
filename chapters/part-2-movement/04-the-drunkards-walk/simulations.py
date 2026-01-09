"""
Simulations for Chapter 4: The Drunkard's Walk

This module provides functions for simulating 1D random walks and analyzing their properties.
It includes utilities for generating walks, visualizing them, and computing statistical properties.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# ============================================================================
# Core Simulation Functions
# ============================================================================

def simulate_random_walk(num_steps, start=0):
    """
    Simulate a 1D random walk with steps of ±1.
    
    Args:
        num_steps: Number of steps to take
        start: Starting position (default 0)
    
    Returns:
        np.array: Position history including starting position
    """
    position = start
    history = [position]
    
    for _ in range(num_steps):
        step = random.choice([-1, 1])
        position += step
        history.append(position)
    
    return np.array(history)


def simulate_random_walk_custom_steps(num_steps, step_distribution, start=0):
    """
    Simulate a 1D random walk with custom step distribution.
    
    Args:
        num_steps: Number of steps to take
        step_distribution: List of possible steps (will be sampled uniformly)
        start: Starting position (default 0)
    
    Returns:
        np.array: Position history including starting position
    """
    position = start
    history = [position]
    
    for _ in range(num_steps):
        step = random.choice(step_distribution)
        position += step
        history.append(position)
    
    return np.array(history)


def simulate_biased_random_walk(num_steps, p_forward=0.6, start=0):
    """
    Simulate a biased random walk where forward steps have probability p.
    
    Args:
        num_steps: Number of steps to take
        p_forward: Probability of stepping forward (+1)
        start: Starting position (default 0)
    
    Returns:
        np.array: Position history including starting position
    """
    position = start
    history = [position]
    
    for _ in range(num_steps):
        step = 1 if random.random() < p_forward else -1
        position += step
        history.append(position)
    
    return np.array(history)


def find_final_position_only(num_steps):
    """
    Fast simulation that returns only the final position (no history).
    Useful when running many walks.
    
    Args:
        num_steps: Number of steps to take
    
    Returns:
        int: Final position
    """
    position = 0
    for _ in range(num_steps):
        position += random.choice([-1, 1])
    return position


def first_return_time(max_steps=100000):
    """
    Simulate until the walker returns to origin.
    
    Args:
        max_steps: Maximum number of steps to allow
    
    Returns:
        int or None: Number of steps until first return, or None if max_steps exceeded
    """
    position = 0
    for step in range(1, max_steps + 1):
        position += random.choice([-1, 1])
        if position == 0:
            return step
    return None


def maximum_distance_reached(num_steps):
    """
    Simulate and return the maximum distance from origin.
    
    Args:
        num_steps: Number of steps to take
    
    Returns:
        int: Maximum absolute distance reached
    """
    position = 0
    max_dist = 0
    
    for _ in range(num_steps):
        position += random.choice([-1, 1])
        max_dist = max(max_dist, abs(position))
    
    return max_dist


def count_zero_crossings(num_steps):
    """
    Simulate and count how many times the walker returns to or crosses zero.
    
    Args:
        num_steps: Number of steps to take
    
    Returns:
        int: Number of zero crossings
    """
    position = 0
    crossings = 0
    was_positive = False
    was_negative = False
    
    for _ in range(num_steps):
        position += random.choice([-1, 1])
        
        if position > 0:
            if was_negative:
                crossings += 1
            was_positive = True
            was_negative = False
        elif position < 0:
            if was_positive:
                crossings += 1
            was_negative = True
            was_positive = False
        # position == 0 counts as a crossing of both sides
    
    return crossings


# ============================================================================
# Analysis Functions
# ============================================================================

def analyze_walk_ensemble(num_walks, num_steps):
    """
    Run many random walks and compute statistics.
    
    Args:
        num_walks: Number of walks to simulate
        num_steps: Steps per walk
    
    Returns:
        dict: Statistics including mean, std, min, max
    """
    final_positions = np.array([find_final_position_only(num_steps) for _ in range(num_walks)])
    
    return {
        'final_positions': final_positions,
        'mean': final_positions.mean(),
        'std': final_positions.std(),
        'median': np.median(final_positions),
        'min': final_positions.min(),
        'max': final_positions.max(),
        'theoretical_std': np.sqrt(num_steps),
    }


def test_sqrt_n_scaling(step_counts, num_walks_per_count=10000):
    """
    Test the theoretical √n scaling of standard deviation.
    
    Args:
        step_counts: List of step counts to test
        num_walks_per_count: Number of walks per step count
    
    Returns:
        tuple: (observed_stds, theoretical_stds)
    """
    observed_stds = []
    theoretical_stds = []
    
    for n in step_counts:
        final_positions = np.array([find_final_position_only(n) for _ in range(num_walks_per_count)])
        observed_stds.append(final_positions.std())
        theoretical_stds.append(np.sqrt(n))
    
    return np.array(observed_stds), np.array(theoretical_stds)


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_single_walk(num_steps=1000, figsize=(12, 6)):
    """
    Plot a single random walk.
    
    Args:
        num_steps: Number of steps to simulate
        figsize: Figure size (width, height)
    """
    walk = simulate_random_walk(num_steps)
    
    plt.figure(figsize=figsize)
    plt.plot(walk, linewidth=0.8, alpha=0.7)
    plt.xlabel("Step Number")
    plt.ylabel("Position")
    plt.title(f"A Single Random Walk: {num_steps} Steps")
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Starting point')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print(f"Final position: {walk[-1]}")
    print(f"Maximum distance from origin: {max(abs(walk))}")


def plot_ensemble_distribution(num_walks=10000, num_steps=1000, figsize=(14, 5)):
    """
    Plot histogram of final positions from many walks with theoretical overlay.
    
    Args:
        num_walks: Number of walks to simulate
        num_steps: Steps per walk
        figsize: Figure size
    """
    stats = analyze_walk_ensemble(num_walks, num_steps)
    final_positions = stats['final_positions']
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram
    axes[0].hist(final_positions, bins=50, density=True, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel("Final Position")
    axes[0].set_ylabel("Density")
    axes[0].set_title(f"Distribution of Final Positions ({num_walks:,} walks)")
    axes[0].grid(True, alpha=0.3)
    
    # Overlay theoretical normal distribution
    sigma = stats['theoretical_std']
    x = np.linspace(-4*sigma, 4*sigma, 1000)
    axes[0].plot(x, norm.pdf(x, 0, sigma), 'r-', linewidth=2, 
                label=f'Normal(0, √{num_steps:.0f}={sigma:.1f})')
    axes[0].legend()
    
    # Statistics panel
    axes[1].axis('off')
    stats_text = f"""
Simulation Statistics
({num_walks:,} walks, {num_steps} steps each)

Mean final position: {stats['mean']:.1f}
Median final position: {stats['median']:.1f}

Standard deviation: {stats['std']:.1f}
√(number of steps): {stats['theoretical_std']:.1f}

Min position: {stats['min']}
Max position: {stats['max']}

Ratio (observed / theoretical): {stats['std'] / stats['theoretical_std']:.3f}
"""
    axes[1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()


def plot_sqrt_n_scaling(max_n=10000, figsize=(10, 6)):
    """
    Plot observed vs theoretical √n scaling.
    
    Args:
        max_n: Maximum number of steps to test
        figsize: Figure size
    """
    step_counts = [10, 50, 100, 500, 1000, 5000, 10000]
    step_counts = [n for n in step_counts if n <= max_n]
    
    observed_stds, theoretical_stds = test_sqrt_n_scaling(step_counts)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.loglog(step_counts, observed_stds, 'o-', label='Observed', 
             linewidth=2, markersize=8, color='blue')
    ax.loglog(step_counts, theoretical_stds, 's--', label='Theoretical (√n)', 
             linewidth=2, markersize=8, color='red')
    
    ax.set_xlabel("Number of Steps (log scale)")
    ax.set_ylabel("Standard Deviation of Final Position (log scale)")
    ax.set_title("Random Walk Spread: Observed vs. Theory")
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.show()
    
    # Print comparison table
    print("\nNumber of Steps | Observed Std | Theoretical | Ratio")
    print("=" * 55)
    for n, obs, theo in zip(step_counts, observed_stds, theoretical_stds):
        ratio = obs / theo
        print(f"{n:>14d} | {obs:>12.2f} | {theo:>11.2f} | {ratio:.3f}")


def plot_multiple_walks(num_walks=10, num_steps=1000, figsize=(12, 8)):
    """
    Plot multiple random walks on the same axes.
    
    Args:
        num_walks: Number of walks to plot
        num_steps: Steps per walk
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for i in range(num_walks):
        walk = simulate_random_walk(num_steps)
        ax.plot(walk, linewidth=0.8, alpha=0.6)
    
    ax.set_xlabel("Step Number")
    ax.set_ylabel("Position")
    ax.set_title(f"{num_walks} Random Walks: {num_steps} Steps Each")
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.3, label='Starting point')
    ax.legend()
    
    plt.tight_layout()
    plt.show()


def plot_first_return_times(num_walks=1000, max_steps=100000, figsize=(14, 5)):
    """
    Plot distribution of first return times.
    
    Args:
        num_walks: Number of walks to simulate
        max_steps: Maximum steps before giving up
        figsize: Figure size
    """
    first_returns = []
    
    for _ in range(num_walks):
        ret_time = first_return_time(max_steps)
        if ret_time is not None:
            first_returns.append(ret_time)
    
    first_returns = np.array(first_returns)
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram (log scale)
    axes[0].hist(first_returns, bins=50, alpha=0.7, edgecolor='black', color='blue')
    axes[0].set_xlabel("Steps Until First Return")
    axes[0].set_ylabel("Count")
    axes[0].set_title(f"Distribution of First Return Times ({len(first_returns)} successful returns)")
    axes[0].set_yscale('log')
    axes[0].set_xscale('log')
    axes[0].grid(True, alpha=0.3, which='both')
    
    # Statistics
    axes[1].axis('off')
    percent_returned = 100 * len(first_returns) / num_walks
    stats_text = f"""
First Return Statistics

Walkers that returned: {len(first_returns)}/{num_walks}
  ({percent_returned:.1f}%)

Minimum return time: {first_returns.min()} steps
Maximum return time: {first_returns.max()} steps
Median return time: {np.median(first_returns):.0f} steps
Mean return time: {first_returns.mean():.0f} steps

Probability of return (1D): ~99.99%
"""
    axes[1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.show()


def plot_step_distribution_comparison(num_walks=10000, num_steps=1000, figsize=(14, 10)):
    """
    Compare final position distributions under different step distributions.
    
    Args:
        num_walks: Number of walks per scenario
        num_steps: Steps per walk
        figsize: Figure size
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Scenario 1: Steps of ±1
    final_positions = np.array([find_final_position_only(num_steps) for _ in range(num_walks)])
    axes[0, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='blue')
    axes[0, 0].set_title("Steps: ±1 (baseline)")
    axes[0, 0].set_ylabel("Count")
    axes[0, 0].set_xlim(-150, 150)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Scenario 2: Steps of ±2
    final_positions = np.array([
        simulate_random_walk_custom_steps(num_steps, [-2, 2])[-1] 
        for _ in range(num_walks)
    ])
    axes[0, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='orange')
    axes[0, 1].set_title("Steps: ±2")
    axes[0, 1].set_xlim(-300, 300)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Scenario 3: Mixed step sizes
    final_positions = np.array([
        simulate_random_walk_custom_steps(num_steps, [-1, 1, 1, 1, 3, 3, 3, 3])[-1]
        for _ in range(num_walks)
    ])
    axes[1, 0].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='green')
    axes[1, 0].set_title("Steps: -1 (1/8), +1 (3/8), +3 (4/8)")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].set_xlim(-150, 150)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Scenario 4: Biased walk
    final_positions = np.array([
        simulate_biased_random_walk(num_steps, p_forward=0.6)[-1]
        for _ in range(num_walks)
    ])
    axes[1, 1].hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='red')
    axes[1, 1].set_title("Biased: +1 with p=0.6, -1 with p=0.4")
    axes[1, 1].set_xlim(-150, 300)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle(f"Final Position Distributions Under Different Step Distributions ({num_walks:,} walks each)")
    plt.tight_layout()
    plt.show()


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == "__main__":
    print("Chapter 4: The Drunkard's Walk - Simulations")
    print("=" * 50)
    print()
    print("This module contains functions for simulating and visualizing random walks.")
    print("Import it or run specific functions to explore:")
    print()
    print("Examples:")
    print("  plot_single_walk(1000)")
    print("  plot_ensemble_distribution(10000, 1000)")
    print("  plot_sqrt_n_scaling()")
    print("  plot_first_return_times(1000)")
    print()
    
    # Run a quick demo
    print("Running quick demo...")
    print()
    
    # Test √n scaling
    print("Testing √n scaling with 5 step counts:")
    step_counts = [100, 500, 1000, 5000, 10000]
    obs, theo = test_sqrt_n_scaling(step_counts, num_walks_per_count=5000)
    
    print("Steps  | Observed Std | Theoretical | Ratio")
    print("-" * 45)
    for n, o, t in zip(step_counts, obs, theo):
        print(f"{n:>5d}  | {o:>12.2f} | {t:>11.2f} | {o/t:.3f}")
