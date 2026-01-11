"""
Figure generation for Chapter 1: The Pattern-Seeking Mind

This module handles all figure generation and export to src/figures/.
Educational simulation functions are in ../simulations.py.
"""

import random
import statistics
from pathlib import Path
import sys

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from shared.figures import figure
from shared.figure_config import DEFAULT_FIGSIZE, DEFAULT_MARGIN_PAD
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


def generate_figure_1_1(num_points=200):
    """
    Figure 1.1: The Clustering Illusion - Uniform vs. Random
    Side-by-side comparison showing the paradox: what we expect randomness
    to look like (left) versus what it actually looks like (right).
    """
    # Generate truly random points
    random_points = generate_random_points(num_points, seed=42)
    
    # Generate quasi-uniform points (grid with small jitter)
    # This approximates what human intuition expects from "random"
    grid_size = int((num_points) ** 0.5)
    uniform_points = []
    for i in range(grid_size):
        for j in range(grid_size):
            if len(uniform_points) >= num_points:
                break
            x = (i + 0.5) / grid_size + random.uniform(-0.03, 0.03)
            y = (j + 0.5) / grid_size + random.uniform(-0.03, 0.03)
            uniform_points.append((max(0, min(1, x)), max(0, min(1, y))))
    
    x_random = [p[0] for p in random_points]
    y_random = [p[1] for p in random_points]
    x_uniform = [p[0] for p in uniform_points]
    y_uniform = [p[1] for p in uniform_points]
    
    with figure(1, 1, 1, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        # Left: What we expect (quasi-uniform)
        ax1 = fig.add_subplot(121)
        ax1.scatter(x_uniform, y_uniform, s=30, alpha=0.6, color='coral')
        ax1.set_xlim(-0.05, 1.05)
        ax1.set_ylim(-0.05, 1.05)
        ax1.set_aspect('equal')
        ax1.set_title('What We Expect:\nBalanced Distribution')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.grid(True, alpha=0.3)
        
        # Right: What we actually get (truly random)
        ax2 = fig.add_subplot(122)
        ax2.scatter(x_random, y_random, s=30, alpha=0.6, color='steelblue')
        ax2.set_xlim(-0.05, 1.05)
        ax2.set_ylim(-0.05, 1.05)
        ax2.set_aspect('equal')
        ax2.set_title('What We Actually Get:\nTrue Randomness')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.grid(True, alpha=0.3)


def generate_figure_1_2(num_flips=100, num_simulations=10000):
    """
    Figure 1.2: Expected vs. Actual Streak Lengths
    Shows the gap between what we expect (short streaks) and reality (mean ~7).
    Same axis ranges and binning to emphasize the distributional difference.
    """
    import numpy as np
    
    results = simulate_coin_flips(num_flips, num_simulations)
    
    # Create synthetic "expected" distribution that peaks around 2-3
    max_streak = max(results['distribution'])
    
    # Bins centered on integers: 0.5, 1.5, 2.5, etc. puts bars at 1, 2, 3, etc.
    bins = np.arange(0.5, int(max_streak) + 1.5, 1)
    
    # Generate expected data with clean weights
    # Represents human intuition: expect very short streaks
    expected_data = []
    weights = [0.1, 0.35, 0.35, 0.15]  # Peak at 2-3, drop off rapidly
    
    for streak_length in range(1, int(max_streak) + 1):
        if streak_length < len(weights):
            weight = weights[streak_length - 1]
        else:
            weight = weights[-1] * (0.6 ** (streak_length - len(weights)))
        
        count = max(1, int(num_simulations * weight))
        expected_data.extend([streak_length] * count)
    
    # Trim or pad to match num_simulations
    expected_data = expected_data[:num_simulations]
    while len(expected_data) < num_simulations:
        expected_data.append(2)
    
    with figure(1, 1, 2, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        # Left: What we expect (human intuition)
        ax1 = fig.add_subplot(121)
        ax1.hist(expected_data, bins=bins, edgecolor='black', alpha=0.7, color='coral')
        ax1.axvline(2.5, color='red', linestyle='--', linewidth=2, label='Expected mean: ~2.5')
        ax1.set_xlabel("Longest Streak Length")
        ax1.set_ylabel("Frequency")
        ax1.set_title("What We Expect:\nShorter Streaks Dominant")
        ax1.set_xticks(range(1, int(max_streak) + 1))
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_xlim(0.5, max_streak + 0.5)
        
        # Right: What we actually get (true randomness)
        ax2 = fig.add_subplot(122)
        ax2.hist(results['distribution'], bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
        ax2.axvline(results['mean'], color='red', linestyle='--', 
                    linewidth=2, label=f"Actual mean: {results['mean']:.1f}")
        ax2.set_xlabel("Longest Streak Length")
        ax2.set_ylabel("Frequency")
        ax2.set_title("What We Actually Get:\nLonger Streaks Common")
        ax2.set_xticks(range(1, int(max_streak) + 1))
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_xlim(0.5, max_streak + 0.5)


def generate_figure_1_3():
    """
    Figure 1.3: The Birthday Paradox - Expectation vs Reality
    Shows the gap between what we expect (linear growth) and what happens (exponential transition).
    """
    group_sizes = range(2, 101)
    actual_probs = [birthday_probability(n) for n in group_sizes]
    
    # What we might expect: linear increase (if people thought probability grew evenly)
    # Naive intuition: 1/365 per person, so roughly n/365
    expected_probs = [min(1.0, (n - 1) / 365) for n in group_sizes]
    
    with figure(1, 1, 3, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        # Left: What we expect (linear/naive intuition)
        ax1 = fig.add_subplot(121)
        ax1.plot(group_sizes, expected_probs, linewidth=2.5, color='coral', label='Naive expectation')
        ax1.axhline(0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='50% threshold')
        ax1.axvline(183, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)  # Where linear reaches 50%
        ax1.fill_between(group_sizes, expected_probs, alpha=0.2, color='coral')
        ax1.set_xlabel("Number of People")
        ax1.set_ylabel("Probability of Shared Birthday")
        ax1.set_title("What We Expect:\nLinear Growth")
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_ylim(0, 1)
        ax1.set_xlim(0, 100)
        
        # Right: What we actually get (sharp transition)
        ax2 = fig.add_subplot(122)
        ax2.plot(group_sizes, actual_probs, linewidth=2.5, color='steelblue', label='Actual probability')
        ax2.axhline(0.5, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='50% threshold')
        ax2.axvline(23, color='green', linestyle='--', alpha=0.7, linewidth=1.5, label='23 people')
        ax2.fill_between(group_sizes, actual_probs, alpha=0.2, color='steelblue')
        ax2.set_xlabel("Number of People")
        ax2.set_ylabel("Probability of Shared Birthday")
        ax2.set_title("What We Actually Get:\nSharp Transition")
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim(0, 1)
        ax2.set_xlim(0, 100)


def generate_figure_1_4(num_points=200, num_cells=10):
    """
    Figure 1.4: Clustering in a Grid Heatmap
    Visualizes random point distribution across cells to demonstrate clustering.
    Single large visualization - no "expected vs actual" needed here.
    """
    import numpy as np
    
    points = generate_random_points(num_points, seed=42)
    
    # Build grid and count points per cell
    grid = [[0 for _ in range(num_cells)] for _ in range(num_cells)]
    for x, y in points:
        cell_x = int(x * num_cells)
        cell_y = int(y * num_cells)
        cell_x = min(cell_x, num_cells - 1)
        cell_y = min(cell_y, num_cells - 1)
        grid[cell_x][cell_y] += 1
    
    grid_array = np.array(grid)
    expected_per_cell = num_points / (num_cells * num_cells)
    
    with figure(1, 1, 4, figsize=(10, 9), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Create heatmap with improved colormap
        im = ax.imshow(grid_array, cmap='YlOrRd', origin='lower', aspect='equal', vmin=0)
        
        # Add text annotations for each cell
        for i in range(num_cells):
            for j in range(num_cells):
                text_color = 'white' if grid_array[j, i] > expected_per_cell * 1.5 else 'black'
                ax.text(i, j, str(int(grid_array[j, i])), 
                       ha="center", va="center", color=text_color, fontsize=8, fontweight='bold')
        
        # Labels and title
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')
        ax.set_title(f'Random Points in {num_cells}×{num_cells} Grid\n({num_points} points total)')
        
        # Set ticks to show cell boundaries
        ax.set_xticks(np.arange(-0.5, num_cells, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, num_cells, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        
        # Colorbar with statistics
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Points per cell')
        
        # Add statistical annotation
        mean_val = grid_array.mean()
        std_val = grid_array.std()
        min_val = grid_array.min()
        max_val = grid_array.max()
        
        stats_text = f'Mean: {mean_val:.1f}\nStd Dev: {std_val:.1f}\nRange: {int(min_val)}–{int(max_val)}'
        ax.text(0.98, 0.02, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def generate_figure_1_5(num_simulations=1000):
    """
    Figure 1.5: The "Hot Hand" in Random Data
    Shows that randomness naturally produces streaks and transitions.
    Demonstrates why we see patterns everywhere—they're baked into randomness itself.
    """
    # Generate random sequences and collect streak statistics
    streak_lengths = []
    run_counts = []
    
    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(100)]
        streak_lengths.append(longest_streak(flips))
        run_counts.append(count_runs(flips))
    
    with figure(1, 1, 5, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        # Left panel: Distribution of longest streaks
        ax1 = fig.add_subplot(121)
        n1, bins1, patches1 = ax1.hist(streak_lengths, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        mean_streak = statistics.mean(streak_lengths)
        ax1.axvline(mean_streak, color='red', linestyle='--', 
                    linewidth=2.5, label=f"Mean: {mean_streak:.1f}")
        ax1.set_xlabel("Longest Streak Length")
        ax1.set_ylabel("Frequency")
        ax1.set_title("How Streaky Is Randomness?\nLongest Streaks in 100-Flip Sequences")
        ax1.set_xticks(range(int(min(streak_lengths)), int(max(streak_lengths)) + 1))
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add annotation
        ax1.text(0.98, 0.97, f'n = {num_simulations} sequences', 
                transform=ax1.transAxes, fontsize=9, 
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Right panel: Distribution of transitions (runs)
        ax2 = fig.add_subplot(122)
        n2, bins2, patches2 = ax2.hist(run_counts, bins=20, edgecolor='black', alpha=0.7, color='coral')
        mean_runs = statistics.mean(run_counts)
        ax2.axvline(mean_runs, color='red', linestyle='--', 
                    linewidth=2.5, label=f"Mean: {mean_runs:.1f}")
        ax2.set_xlabel("Number of Transitions (Runs)")
        ax2.set_ylabel("Frequency")
        ax2.set_title("How Many Transitions?\nRun Changes in 100-Flip Sequences")
        ax2.set_xticks(range(int(min(run_counts)), int(max(run_counts)) + 1, 2))
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add annotation
        ax2.text(0.98, 0.97, f'n = {num_simulations} sequences', 
                transform=ax2.transAxes, fontsize=9,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


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
