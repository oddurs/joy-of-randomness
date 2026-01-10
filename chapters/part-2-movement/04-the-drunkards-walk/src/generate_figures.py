"""
Figure generation for Chapter 4: The Drunkard's Walk

Generates publication-quality figures from the chapter simulations.
"""

import sys
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Disable LaTeX rendering to avoid special character issues
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from shared.figures import figure
from simulations import (
    simulate_random_walk,
    simulate_random_walk_custom_steps,
    simulate_biased_random_walk,
    analyze_walk_ensemble,
    test_sqrt_n_scaling,
    first_return_time,
    find_final_position_only,
)

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_4_1():
    """
    Figure 4.1: A Single Random Walk
    Shows one trajectory of a 1D random walk.
    """
    random.seed(42)
    num_steps = 1000
    walk = simulate_random_walk(num_steps)
    
    with figure(2, 4, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        ax.plot(walk, linewidth=1.2, alpha=0.8, color='steelblue')
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='Starting point')
        ax.set_xlabel('Step Number')
        ax.set_ylabel('Position')
        ax.set_title('A Single Random Walk: 1,000 Steps')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')


def generate_figure_4_2():
    """
    Figure 4.2: Distribution of Final Positions
    Histogram of final positions from 10,000 walks with theoretical overlay.
    """
    random.seed(42)
    num_walks = 5000
    num_steps = 1000
    stats = analyze_walk_ensemble(num_walks, num_steps)
    final_positions = stats['final_positions']
    
    with figure(2, 4, 2, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Histogram
        ax.hist(final_positions, bins=50, density=True, alpha=0.7, 
                edgecolor='black', color='steelblue', label='Observed')
        
        # Overlay theoretical normal distribution
        sigma = stats['theoretical_std']
        x = np.linspace(-4*sigma, 4*sigma, 1000)
        ax.plot(x, norm.pdf(x, 0, sigma), 'r-', linewidth=2.5, 
                label=f'Normal(0, sqrt({num_steps}) ~ {sigma:.1f})')
        
        ax.set_xlabel('Final Position')
        ax.set_ylabel('Density')
        ax.set_title(f'Distribution of Final Positions: {num_walks:,} Walks, {num_steps} Steps Each')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=11)


def generate_figure_4_3():
    """
    Figure 4.3: Sqrt(n) Scaling Law
    Demonstrates how spread grows as the square root of the number of steps.
    """
    random.seed(42)
    step_counts = [10, 50, 100, 500, 1000, 5000]
    observed_stds, theoretical_stds = test_sqrt_n_scaling(step_counts, num_walks_per_count=1000)
    
    with figure(2, 4, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.loglog(step_counts, observed_stds, 'o-', label='Observed', 
                 linewidth=2.5, markersize=8, color='steelblue')
        ax.loglog(step_counts, theoretical_stds, 's--', label='Theoretical (sqrt(n))', 
                 linewidth=2.5, markersize=8, color='red')
        
        ax.set_xlabel('Number of Steps (log scale)')
        ax.set_ylabel('Standard Deviation of Final Position (log scale)')
        ax.set_title('Random Walk Spread Grows as Sqrt(n)')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, which='both')


def generate_figure_4_4():
    """
    Figure 4.4: Multiple Random Walks Ensemble
    Shows 20 trajectories to visualize the ensemble behavior.
    """
    random.seed(42)
    num_walks = 20
    num_steps = 1000
    
    with figure(2, 4, 4, figsize=(14, 8), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        for i in range(num_walks):
            walk = simulate_random_walk(num_steps)
            ax.plot(walk, linewidth=0.8, alpha=0.5, color='steelblue')
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Starting point')
        ax.set_xlabel('Step Number')
        ax.set_ylabel('Position')
        ax.set_title(f'{num_walks} Random Walks: {num_steps} Steps Each')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')


def generate_figure_4_5():
    """
    Figure 4.5: First Return Times Distribution
    Log-log histogram showing how often walks return to origin.
    """
    random.seed(42)
    num_walks = 2000
    max_steps = 100000
    first_returns = []
    
    for _ in range(num_walks):
        ret_time = first_return_time(max_steps)
        if ret_time is not None:
            first_returns.append(ret_time)
    
    first_returns = np.array(first_returns)
    
    with figure(2, 4, 5, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.hist(first_returns, bins=60, alpha=0.7, edgecolor='black', 
                color='steelblue', label='Observed')
        ax.set_xlabel('Steps Until First Return')
        ax.set_ylabel('Count')
        ax.set_title(f'Distribution of First Return Times: {len(first_returns)}/{num_walks} Walkers Returned')
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.grid(True, alpha=0.3, which='both')
        ax.legend(loc='best')


def generate_figure_4_6():
    """
    Figure 4.6: Step Distribution Comparison
    Compares final position distributions under different step rules.
    """
    random.seed(42)
    num_walks = 2000
    num_steps = 1000
    
    with figure(2, 4, 6, figsize=(14, 10), output_dir=OUTPUT_DIR) as fig:
        
        # Scenario 1: Steps of ±1
        ax1 = fig.add_subplot(2, 2, 1)
        final_positions = np.array([find_final_position_only(num_steps) for _ in range(num_walks)])
        ax1.hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='steelblue')
        ax1.set_title('Steps: ±1 (baseline)', fontsize=12)
        ax1.set_ylabel('Count')
        ax1.set_xlim(-150, 150)
        ax1.grid(True, alpha=0.3)
        
        # Scenario 2: Steps of ±2
        ax2 = fig.add_subplot(2, 2, 2)
        final_positions = np.array([
            simulate_random_walk_custom_steps(num_steps, [-2, 2])[-1] 
            for _ in range(num_walks)
        ])
        ax2.hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='orange')
        ax2.set_title('Steps: ±2', fontsize=12)
        ax2.set_xlim(-300, 300)
        ax2.grid(True, alpha=0.3)
        
        # Scenario 3: Mixed step sizes
        ax3 = fig.add_subplot(2, 2, 3)
        final_positions = np.array([
            simulate_random_walk_custom_steps(num_steps, [-1, 1, 1, 1, 3, 3, 3, 3])[-1]
            for _ in range(num_walks)
        ])
        ax3.hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='green')
        ax3.set_title('Steps: -1 (1/8), +1 (3/8), +3 (4/8)', fontsize=12)
        ax3.set_ylabel('Count')
        ax3.set_xlim(-150, 300)
        ax3.grid(True, alpha=0.3)
        
        # Scenario 4: Biased walk
        ax4 = fig.add_subplot(2, 2, 4)
        final_positions = np.array([
            simulate_biased_random_walk(num_steps, p_forward=0.6)[-1]
            for _ in range(num_walks)
        ])
        ax4.hist(final_positions, bins=50, alpha=0.7, edgecolor='black', color='red')
        ax4.set_title('Biased: +1 with p=0.6, -1 with p=0.4', fontsize=12)
        ax4.set_xlim(-50, 400)
        ax4.grid(True, alpha=0.3)
        
        fig.suptitle(f'Final Position Distributions: Different Step Rules ({num_walks:,} walks each)', 
                    fontsize=14, y=0.995)


def main():
    """Generate all figures for Chapter 4."""
    print("Generating Chapter 4 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Figure 4.1: A Single Random Walk")
    generate_figure_4_1()
    
    print("Generating Figure 4.2: Distribution of Final Positions")
    generate_figure_4_2()
    
    print("Generating Figure 4.3: √n Scaling Law")
    generate_figure_4_3()
    
    print("Generating Figure 4.4: Multiple Random Walks Ensemble")
    generate_figure_4_4()
    
    print("Generating Figure 4.5: First Return Times Distribution")
    generate_figure_4_5()
    
    print("Generating Figure 4.6: Step Distribution Comparison")
    generate_figure_4_6()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
