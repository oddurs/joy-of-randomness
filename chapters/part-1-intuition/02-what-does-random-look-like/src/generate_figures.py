"""
Figure generation for Chapter 2: What Does Random Even Look Like?

This module generates all figures for Chapter 2, demonstrating visualizations
of coin flips, randomness properties, and comparisons between machine and
hand-generated sequences.
"""

import random
import statistics
from pathlib import Path
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex'] = False  # Disable LaTeX to avoid dependency

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from shared.figures import FigureManager
from simulations import (
    longest_streak,
    count_runs,
    generate_coin_sequence,
    simulate_longest_streaks,
    simulate_runs,
    running_proportion,
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


def generate_figure_2_1(num_sequences=10000, flips_per_sequence=100):
    """
    Figure 2.1: Distribution of Longest Streaks
    Shows the distribution of longest streaks across 10,000 sequences of 100 coin flips.
    """
    streaks = simulate_longest_streaks(num_sequences, flips_per_sequence)
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.hist(streaks, bins=range(min(streaks), max(streaks) + 2), 
            edgecolor='black', alpha=0.7, color='steelblue')
    
    mean_streak = statistics.mean(streaks)
    median_streak = statistics.median(streaks)
    
    ax.axvline(mean_streak, color='red', linestyle='--', 
               linewidth=2, label=f"Mean: {mean_streak:.1f}")
    ax.axvline(median_streak, color='green', linestyle='--', 
               linewidth=2, label=f"Median: {median_streak:.0f}")
    
    ax.set_xlabel("Length of Longest Streak")
    ax.set_ylabel("Frequency (out of 10,000 sequences)")
    ax.set_title(f"Distribution of Longest Streaks\n({flips_per_sequence} flips per sequence, {num_sequences} sequences)")
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    save_figure(fig, "2.1.png")


def generate_figure_2_2(num_sequences=10000, flips_per_sequence=100):
    """
    Figure 2.2: Distribution of Runs (Transitions)
    Shows how many times the outcome changes from H to T or T to H.
    """
    run_counts = simulate_runs(num_sequences, flips_per_sequence)
    
    mean_runs = statistics.mean(run_counts)
    median_runs = statistics.median(run_counts)
    expected_runs = flips_per_sequence / 2 + 1
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.hist(run_counts, bins=range(min(run_counts), max(run_counts) + 2), 
            edgecolor='black', alpha=0.7, color='coral')
    
    ax.axvline(mean_runs, color='red', linestyle='--', 
               linewidth=2, label=f"Mean: {mean_runs:.1f}")
    ax.axvline(expected_runs, color='purple', linestyle='--', 
               linewidth=2, label=f"Expected: {expected_runs:.1f}")
    
    ax.set_xlabel("Number of Runs (Transitions)")
    ax.set_ylabel("Frequency (out of 10,000 sequences)")
    ax.set_title(f"Distribution of Runs in Coin Flip Sequences\n({flips_per_sequence} flips per sequence, {num_sequences} sequences)")
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    save_figure(fig, "2.2.png")


def generate_figure_2_3(flips_long=10000):
    """
    Figure 2.3: Running Proportion Convergence
    Demonstrates how the proportion of heads converges to 0.5 as the number
    of flips increases.
    """
    sequence = generate_coin_sequence(flips_long)
    proportions = running_proportion(sequence)
    
    # Prepare data for plotting at different scales
    checkpoints = np.logspace(0, np.log10(flips_long), 100, dtype=int)
    checkpoint_props = [proportions[cp - 1] for cp in checkpoints if cp <= len(proportions)]
    checkpoint_nums = [cp for cp in checkpoints if cp <= len(proportions)]
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    # Plot the full running proportion line
    ax.plot(range(1, len(proportions) + 1), proportions, 
            linewidth=1, color='steelblue', alpha=0.7, label='Running proportion')
    
    # Add a horizontal line at 0.5
    ax.axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='50% (fair coin)')
    
    # Add confidence bands
    for n in [100, 1000, 10000]:
        if n <= flips_long:
            margin = 1.96 / np.sqrt(n)  # 95% confidence interval
            ax.fill_between([n, n], 0.5 - margin, 0.5 + margin, 
                           alpha=0.1, color='green')
    
    ax.set_xlabel("Number of Flips")
    ax.set_ylabel("Proportion of Heads")
    ax.set_xscale('log')
    ax.set_ylim(0, 1)
    ax.set_title(f"Convergence of Heads Proportion to 0.5\n({flips_long:,} flips, log scale)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "2.3.png")


def generate_figure_2_4(num_sequences=100, flips_per_sequence=100):
    """
    Figure 2.4: Comparison of Runs: Fair vs Over-Alternating
    Shows the difference between truly random sequences (which cluster)
    and human-generated sequences (which alternate too much).
    """
    # Generate fair sequences
    fair_runs = []
    for _ in range(num_sequences):
        seq = generate_coin_sequence(flips_per_sequence)
        fair_runs.append(count_runs(seq))
    
    # Generate over-alternating sequences (human-like)
    # Alternate with 70% probability to simulate human behavior
    over_alternating_runs = []
    for _ in range(num_sequences):
        seq = []
        current = random.choice([0, 1])
        seq.append(current)
        
        for _ in range(flips_per_sequence - 1):
            # 70% chance to alternate, 30% chance to repeat
            if random.random() < 0.7:
                current = 1 - current  # Alternate
            seq.append(current)
        
        over_alternating_runs.append(count_runs(seq))
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    # Create histograms
    bins = range(min(min(fair_runs), min(over_alternating_runs)), 
                max(max(fair_runs), max(over_alternating_runs)) + 2)
    
    ax.hist(fair_runs, bins=bins, alpha=0.6, label='Fair Coin (truly random)', 
           color='steelblue', edgecolor='black')
    ax.hist(over_alternating_runs, bins=bins, alpha=0.6, label='Over-alternating (human-like)', 
           color='coral', edgecolor='black')
    
    ax.set_xlabel("Number of Runs")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Fair Coin vs Over-Alternating Sequences\n({num_sequences} sequences of {flips_per_sequence} flips)")
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add text annotations for means
    fair_mean = statistics.mean(fair_runs)
    over_mean = statistics.mean(over_alternating_runs)
    ax.text(0.98, 0.97, f"Fair mean: {fair_mean:.1f}\nHuman-like mean: {over_mean:.1f}", 
           transform=ax.transAxes, verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    save_figure(fig, "2.4.png")


def generate_figure_2_5(num_simulations=100):
    """
    Figure 2.5: Streak Distribution Across Sequences
    Shows individual streak lengths for multiple sequences, demonstrating
    the natural variation in what we expect from randomness.
    """
    sequences = [generate_coin_sequence(100) for _ in range(num_simulations)]
    max_streaks = [longest_streak(seq) for seq in sequences]
    run_counts = [count_runs(seq) for seq in sequences]
    
    fig = plt.figure(figsize=(12, 5))
    
    # Left subplot: Max streaks
    ax1 = fig.add_subplot(121)
    ax1.scatter(range(1, num_simulations + 1), max_streaks, alpha=0.6, s=50, color='steelblue')
    ax1.axhline(statistics.mean(max_streaks), color='red', linestyle='--', 
               linewidth=2, label=f"Mean: {statistics.mean(max_streaks):.1f}")
    ax1.set_xlabel("Sequence Number")
    ax1.set_ylabel("Longest Streak Length")
    ax1.set_title(f"Max Streak in Each Sequence")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right subplot: Run counts
    ax2 = fig.add_subplot(122)
    ax2.scatter(range(1, num_simulations + 1), run_counts, alpha=0.6, s=50, color='coral')
    ax2.axhline(statistics.mean(run_counts), color='red', linestyle='--', 
               linewidth=2, label=f"Mean: {statistics.mean(run_counts):.1f}")
    ax2.set_xlabel("Sequence Number")
    ax2.set_ylabel("Number of Runs")
    ax2.set_title(f"Runs in Each Sequence")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle(f"Variability in Randomness Across {num_simulations} Sequences of 100 Flips", 
                fontsize=12, y=1.00)
    
    save_figure(fig, "2.5.png")


def generate_all_figures():
    """Generate all figures for Chapter 2."""
    print("Generating Chapter 2: What Does Random Even Look Like?")
    print("=" * 60)
    print()
    
    print("Figure 2.1: Distribution of Longest Streaks...")
    generate_figure_2_1()
    print()
    
    print("Figure 2.2: Distribution of Runs (Transitions)...")
    generate_figure_2_2()
    print()
    
    print("Figure 2.3: Running Proportion Convergence...")
    generate_figure_2_3()
    print()
    
    print("Figure 2.4: Fair vs Over-Alternating Sequences...")
    generate_figure_2_4()
    print()
    
    print("Figure 2.5: Streak and Run Variability...")
    generate_figure_2_5()
    print()
    
    print("=" * 60)
    print("✓ All figures for Chapter 2 generated successfully!")


if __name__ == "__main__":
    generate_all_figures()

