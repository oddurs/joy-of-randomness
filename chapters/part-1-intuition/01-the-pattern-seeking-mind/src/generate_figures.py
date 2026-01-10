"""
Figure generation for Chapter 1: The Pattern-Seeking Mind

This module handles all figure generation and export to src/figures/.
Educational simulation functions are in ../simulations.py.
"""

import random
import statistics
from pathlib import Path
import sys
import matplotlib
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401

matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
plt.style.use('science')

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from simulations import (
    generate_random_points,
    simulate_coin_flips,
    birthday_probability,
    analyze_clustering_in_grid,
    longest_streak,
    count_runs,
)

# Local output directory for this chapter's figures
OUTPUT_DIR = Path(__file__).parent / "figures"


def save_figure(fig, filename):
    """Save figure to OUTPUT_DIR with custom filename."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    fig.tight_layout(pad=1.5)
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"✓ Saved figure: {filepath}")
    plt.close(fig)


def generate_figure_1_1(num_points=200):
    """
    Figure 1.1: Random Points in a Square
    Demonstrates the clustering illusion with 200 random points.
    """
    points = generate_random_points(num_points, seed=42)
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.scatter(x, y, s=30, alpha=0.6, color='steelblue')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    ax.set_title('Random Points in a Square')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "1.1.png")


def generate_figure_1_2(num_flips=100, num_simulations=10000):
    """
    Figure 1.2: Distribution of Longest Streaks in Coin Flips
    Shows how longest streaks distribute across many simulations.
    """
    results = simulate_coin_flips(num_flips, num_simulations)
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.hist(results['distribution'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    ax.axvline(results['mean'], color='red', linestyle='--', 
                linewidth=2, label=f"Mean: {results['mean']:.1f}")
    ax.axvline(results['median'], color='green', linestyle='--', 
                linewidth=2, label=f"Median: {results['median']:.0f}")
    ax.set_xlabel("Length of Longest Streak")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Longest Streaks")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "1.2.png")


def generate_figure_1_3():
    """
    Figure 1.3: The Birthday Paradox
    Probability of shared birthdays increases rapidly with group size.
    """
    group_sizes = range(2, 101)
    probabilities = [birthday_probability(n) for n in group_sizes]
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(group_sizes, probabilities, linewidth=2, color='steelblue')
    ax.axhline(0.5, color='red', linestyle='--', alpha=0.5, label='50% probability')
    ax.axvline(23, color='green', linestyle='--', alpha=0.5, label='23 people')
    ax.set_xlabel("Number of People")
    ax.set_ylabel("Probability of Shared Birthday")
    ax.set_title("The Birthday Paradox")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_ylim(0, 1)
    
    save_figure(fig, "1.3.png")


def generate_figure_1_4(num_points=200, num_cells=10):
    """
    Figure 1.4: Clustering in a Grid
    Shows how random points cluster into cells, revealing the illusion.
    """
    points = generate_random_points(num_points, seed=42)
    analysis = analyze_clustering_in_grid(points, num_cells)
    
    # Prepare data for visualization
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    for x, y in points:
        cell_x = int(x * num_cells)
        cell_y = int(y * num_cells)
        cell_x = min(cell_x, num_cells - 1)
        cell_y = min(cell_y, num_cells - 1)
        grid[cell_x][cell_y] += 1
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Create heatmap
    im = ax.imshow(grid, cmap='YlOrRd', origin='lower', aspect='auto')
    ax.set_xlabel('Cell X')
    ax.set_ylabel('Cell Y')
    ax.set_title('Clustering in Random Data')
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Points per cell')
    
    # Add grid lines
    for i in range(num_cells + 1):
        ax.axhline(i - 0.5, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        ax.axvline(i - 0.5, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    
    save_figure(fig, "1.4.png")


def generate_figure_1_5(num_simulations=1000):
    """
    Figure 1.5: Hot Hand vs Random
    Compares streak distributions in simulated "hot hand" data vs pure randomness.
    Demonstrates that streaks appear even in completely random sequences.
    """
    # Generate random sequences and collect streak statistics
    streak_lengths = []
    run_counts = []
    
    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(100)]
        streak_lengths.append(longest_streak(flips))
        run_counts.append(count_runs(flips))
    
    fig = plt.figure(figsize=(12, 5))
    
    # Left panel: Distribution of longest streaks
    ax1 = fig.add_subplot(121)
    ax1.hist(streak_lengths, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.axvline(statistics.mean(streak_lengths), color='red', linestyle='--', 
                linewidth=2, label=f"Mean: {statistics.mean(streak_lengths):.1f}")
    ax1.set_xlabel("Longest Streak Length")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Streaks in Random Sequences")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right panel: Distribution of runs/transitions
    ax2 = fig.add_subplot(122)
    ax2.hist(run_counts, bins=20, edgecolor='black', alpha=0.7, color='coral')
    ax2.axvline(statistics.mean(run_counts), color='red', linestyle='--', 
                linewidth=2, label=f"Mean: {statistics.mean(run_counts):.1f}")
    ax2.set_xlabel("Number of Transitions")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Run Transitions in Random Sequences")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle("Random Sequences: Streaks and Transitions", fontsize=12, y=1.00)
    
    save_figure(fig, "1.5.png")


def generate_all_figures():
    """
    Generate all figures for Chapter 1.
    """
    print("Generating Chapter 1 figures...")
    print()
    
    print("Generating Figure 1.1: Random Points in a Square")
    generate_figure_1_1()
    
    print("Generating Figure 1.2: Distribution of Longest Streaks")
    generate_figure_1_2()
    
    print("Generating Figure 1.3: The Birthday Paradox")
    generate_figure_1_3()
    
    print("Generating Figure 1.4: Clustering in a Grid")
    generate_figure_1_4()
    
    print("Generating Figure 1.5: Streaks and Transitions in Random Sequences")
    generate_figure_1_5()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    generate_all_figures()
