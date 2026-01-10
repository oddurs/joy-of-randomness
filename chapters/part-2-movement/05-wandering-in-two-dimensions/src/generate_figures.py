"""
Figure generation for Chapter 5: Wandering in Two Dimensions

Generates publication-quality figures from the chapter simulations.
"""

import sys
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt

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
    random_walk_2d,
    simulate_return_distance_by_dimension,
    estimate_return_probability_by_dimension,
)

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_5_1():
    """
    Figure 5.1: A Single 2D Random Walk
    Shows one trajectory of a 2D random walk.
    """
    random.seed(42)
    num_steps = 5000
    walk = random_walk_2d(num_steps)
    
    with figure(2, 5, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        ax.plot(walk[:, 0], walk[:, 1], linewidth=0.5, alpha=0.7, color='steelblue')
        ax.plot(walk[0, 0], walk[0, 1], 'go', markersize=8, label='Start')
        ax.plot(walk[-1, 0], walk[-1, 1], 'r*', markersize=15, label='End')
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_title('A Single 2D Random Walk: 5,000 Steps')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')


def generate_figure_5_2():
    """
    Figure 5.2: Ensemble of 2D Random Walks
    Shows multiple 2D trajectories to visualize collective behavior.
    """
    random.seed(42)
    num_walks = 8
    num_steps = 2000
    
    with figure(2, 5, 2, figsize=(14, 10), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        for _ in range(num_walks):
            walk = random_walk_2d(num_steps)
            ax.plot(walk[:, 0], walk[:, 1], linewidth=0.5, alpha=0.5)
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_title(f'Ensemble of {num_walks} 2D Random Walks: {num_steps} Steps Each')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)


def generate_figure_5_3():
    """
    Figure 5.3: Distance from Origin by Dimension
    Compares spreading in 1D, 2D, and 3D random walks.
    """
    random.seed(42)
    num_walks = 500
    num_steps = 1000
    
    # Simulate distances for 1D, 2D, 3D
    data_1d = simulate_return_distance_by_dimension(1, num_walks, num_steps)
    data_2d = simulate_return_distance_by_dimension(2, num_walks, num_steps)
    data_3d = simulate_return_distance_by_dimension(3, num_walks, num_steps)
    
    with figure(2, 5, 3, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.hist(data_1d, bins=40, alpha=0.5, label='1D', color='blue', density=True)
        ax.hist(data_2d, bins=40, alpha=0.5, label='2D', color='green', density=True)
        ax.hist(data_3d, bins=40, alpha=0.5, label='3D', color='red', density=True)
        
        ax.set_xlabel('Distance from Origin')
        ax.set_ylabel('Density')
        ax.set_title(f'Final Distances: 1D vs 2D vs 3D ({num_walks} walks, {num_steps} steps)')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)


def generate_figure_5_4():
    """
    Figure 5.4: Return Probability by Dimension
    Shows why 2D walkers have difficulty returning to origin.
    """
    random.seed(42)
    dimensions = [1, 2, 3, 4]
    return_probs = estimate_return_probability_by_dimension(dimensions, num_walks=500, max_steps=50000)
    
    with figure(2, 5, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        colors = ['blue', 'green', 'red', 'orange']
        for dim, prob, color in zip(dimensions, return_probs, colors):
            ax.plot(dim, prob * 100, 'o', markersize=12, color=color, label=f'{dim}D')
        
        ax.set_xlabel('Dimension')
        ax.set_ylabel('Probability of Return (%)')
        ax.set_title('Return to Origin: How Dimension Matters')
        ax.set_ylim([0, 105])
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=11)
        ax.set_xticks(dimensions)


def generate_figure_5_5():
    """
    Figure 5.5: Return Times Comparison
    Compares first return time distributions across dimensions.
    """
    random.seed(42)
    max_steps = 100000
    num_walks = 300
    
    # Get return times for 2D and 3D
    def get_first_returns(dim, num_walks, max_steps):
        returns = []
        for _ in range(num_walks):
            position = np.zeros(dim)
            for step in range(1, max_steps + 1):
                # Random direction
                direction = np.random.randn(dim)
                direction /= np.linalg.norm(direction)
                position += direction
                
                if np.linalg.norm(position) < 1.0 and step > 1:
                    returns.append(step)
                    break
        return np.array(returns)
    
    returns_2d = get_first_returns(2, num_walks, max_steps)
    returns_3d = get_first_returns(3, num_walks, max_steps)
    
    with figure(2, 5, 5, figsize=(14, 6), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.hist(returns_2d, bins=50, alpha=0.6, label='2D', color='green', density=True)
        ax.hist(returns_3d, bins=50, alpha=0.6, label='3D', color='red', density=True)
        
        ax.set_xlabel('Steps Until First Return')
        ax.set_ylabel('Density')
        ax.set_title(f'First Return Times: 2D vs 3D ({num_walks} walks each)')
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3, which='both')


def main():
    """Generate all figures for Chapter 5."""
    print("Generating Chapter 5 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Figure 5.1: A Single 2D Random Walk")
    generate_figure_5_1()
    
    print("Generating Figure 5.2: Ensemble of 2D Random Walks")
    generate_figure_5_2()
    
    print("Generating Figure 5.3: Distance from Origin by Dimension")
    generate_figure_5_3()
    
    print("Generating Figure 5.4: Return Probability by Dimension")
    generate_figure_5_4()
    
    print("Generating Figure 5.5: Return Times Comparison")
    generate_figure_5_5()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
