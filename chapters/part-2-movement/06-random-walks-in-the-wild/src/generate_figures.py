"""
Figure generation for Chapter 6: Random Walks in the Wild
"""

import sys
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_6_1():
    """Figure 6.1: Ideal vs realistic animal tracks"""
    np.random.seed(42)
    
    # Ideal random walk - fewer steps for faster execution
    ideal_x, ideal_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        ideal_x.append(ideal_x[-1] + np.cos(angle))
        ideal_y.append(ideal_y[-1] + np.sin(angle))
    ideal_x, ideal_y = np.array(ideal_x), np.array(ideal_y)
    
    # Realistic animal track
    animal_x, animal_y = [0], [0]
    angle = np.random.uniform(0, 2 * np.pi)
    for _ in range(1000):
        step_size = np.random.exponential(scale=1.0)
        angle += np.random.normal(loc=0, scale=0.3)
        animal_x.append(animal_x[-1] + step_size * np.cos(angle))
        animal_y.append(animal_y[-1] + step_size * np.sin(angle))
    animal_x, animal_y = np.array(animal_x), np.array(animal_y)
    
    # Lévy flight
    levy_x, levy_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        step_size = np.random.pareto(a=1.5) + 1
        levy_x.append(levy_x[-1] + step_size * np.cos(angle))
        levy_y.append(levy_y[-1] + step_size * np.sin(angle))
    levy_x, levy_y = np.array(levy_x), np.array(levy_y)
    
    with figure(2, 6, 1, output_dir=OUTPUT_DIR) as fig:
        ax1 = fig.add_subplot(131)
        ax1.plot(ideal_x, ideal_y, linewidth=0.3, alpha=0.7, color='C0')
        ax1.scatter([0], [0], color='red', s=50, zorder=5)
        ax1.set_aspect('equal')
        ax1.set_title('Ideal Random Walk')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.grid(True, alpha=0.3)
        
        ax2 = fig.add_subplot(132)
        ax2.plot(animal_x, animal_y, linewidth=0.3, alpha=0.7, color='C1')
        ax2.scatter([0], [0], color='red', s=50, zorder=5)
        ax2.set_aspect('equal')
        ax2.set_title('Animal Track')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(133)
        ax3.plot(levy_x, levy_y, linewidth=0.3, alpha=0.7, color='C2')
        ax3.scatter([0], [0], color='red', s=50, zorder=5)
        ax3.set_aspect('equal')
        ax3.set_title('Lévy Flight')
        ax3.set_xlabel('X')
        ax3.set_ylabel('Y')
        ax3.grid(True, alpha=0.3)
        
        fig.suptitle('Movement Patterns: Ideal vs Realistic', fontsize=14, y=0.98)


def generate_figure_6_2():
    """Figure 6.2: Step length distributions"""
    np.random.seed(42)
    
    def step_lengths(x, y):
        dx = np.diff(x)
        dy = np.diff(y)
        return np.sqrt(dx**2 + dy**2)
    
    # Generate three types of walks
    ideal_x, ideal_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        ideal_x.append(ideal_x[-1] + np.cos(angle))
        ideal_y.append(ideal_y[-1] + np.sin(angle))
    ideal_x, ideal_y = np.array(ideal_x), np.array(ideal_y)
    
    animal_x, animal_y = [0], [0]
    angle = np.random.uniform(0, 2 * np.pi)
    for _ in range(1000):
        step_size = np.random.exponential(scale=1.0)
        angle += np.random.normal(loc=0, scale=0.3)
        animal_x.append(animal_x[-1] + step_size * np.cos(angle))
        animal_y.append(animal_y[-1] + step_size * np.sin(angle))
    animal_x, animal_y = np.array(animal_x), np.array(animal_y)
    
    levy_x, levy_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        step_size = np.random.pareto(a=1.5) + 1
        levy_x.append(levy_x[-1] + step_size * np.cos(angle))
        levy_y.append(levy_y[-1] + step_size * np.sin(angle))
    levy_x, levy_y = np.array(levy_x), np.array(levy_y)
    
    steps_ideal = step_lengths(ideal_x, ideal_y)
    steps_animal = step_lengths(animal_x, animal_y)
    steps_levy = step_lengths(levy_x, levy_y)
    
    with figure(2, 6, 2, output_dir=OUTPUT_DIR) as fig:
        ax1 = fig.add_subplot(131)
        ax1.hist(steps_ideal, bins=20, alpha=0.7, edgecolor='black', color='C0', density=True)
        ax1.set_xlabel('Step Length')
        ax1.set_ylabel('Probability Density')
        ax1.set_title('Ideal Random Walk')
        ax1.grid(True, alpha=0.3)
        
        ax2 = fig.add_subplot(132)
        ax2.hist(steps_animal, bins=20, alpha=0.7, edgecolor='black', color='C1', density=True)
        ax2.set_xlabel('Step Length')
        ax2.set_ylabel('Probability Density')
        ax2.set_title('Animal Track')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(133)
        sorted_steps = np.sort(steps_levy)
        ccdf = np.arange(1, len(sorted_steps) + 1)[::-1] / len(sorted_steps)
        ax3.loglog(sorted_steps, ccdf, marker='.', linestyle='none', alpha=0.5, color='C2')
        ax3.set_xlabel('Step Length (log)')
        ax3.set_ylabel('Tail Probability (log)')
        ax3.set_title('Lévy Flight')
        ax3.grid(True, alpha=0.3, which='both')
        
        fig.suptitle('Step Length Distributions', fontsize=14, y=0.98)


def generate_figure_6_3():
    """Figure 6.3: Search efficiency comparison"""
    np.random.seed(42)
    
    def search_efficiency(x, y, num_targets=50):
        target_positions = np.random.uniform(-100, 100, (num_targets, 2))
        found = 0
        search_radius = 5.0
        
        for i in range(min(len(x), 1000)):
            walker_pos = np.array([x[i], y[i]])
            distances = np.linalg.norm(target_positions - walker_pos, axis=1)
            found += np.sum(distances < search_radius)
            target_positions = target_positions[distances >= search_radius]
        
        return found
    
    # Generate walks
    ideal_x, ideal_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        ideal_x.append(ideal_x[-1] + np.cos(angle))
        ideal_y.append(ideal_y[-1] + np.sin(angle))
    ideal_x, ideal_y = np.array(ideal_x), np.array(ideal_y)
    
    animal_x, animal_y = [0], [0]
    angle = np.random.uniform(0, 2 * np.pi)
    for _ in range(1000):
        step_size = np.random.exponential(scale=1.0)
        angle += np.random.normal(loc=0, scale=0.3)
        animal_x.append(animal_x[-1] + step_size * np.cos(angle))
        animal_y.append(animal_y[-1] + step_size * np.sin(angle))
    animal_x, animal_y = np.array(animal_x), np.array(animal_y)
    
    levy_x, levy_y = [0], [0]
    for _ in range(1000):
        angle = np.random.uniform(0, 2 * np.pi)
        step_size = np.random.pareto(a=1.5) + 1
        levy_x.append(levy_x[-1] + step_size * np.cos(angle))
        levy_y.append(levy_y[-1] + step_size * np.sin(angle))
    levy_x, levy_y = np.array(levy_x), np.array(levy_y)
    
    # Run multiple simulations
    ideal_found = [search_efficiency(ideal_x, ideal_y, 50) for _ in range(5)]
    animal_found = [search_efficiency(animal_x, animal_y, 50) for _ in range(5)]
    levy_found = [search_efficiency(levy_x, levy_y, 50) for _ in range(5)]
    
    with figure(2, 6, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        data = [ideal_found, animal_found, levy_found]
        positions = [1, 2, 3]
        labels = ['Ideal\nWalk', 'Animal\nTrack', 'Lévy\nFlight']
        colors = ['C0', 'C1', 'C2']
        
        for pos, d, label, color in zip(positions, data, labels, colors):
            ax.scatter([pos] * len(d), d, alpha=0.6, s=100, color=color, zorder=3)
            ax.plot([pos, pos], [np.min(d), np.max(d)], 'k-', alpha=0.3, zorder=1)
            ax.scatter([pos], [np.mean(d)], marker='_', s=500, color='red', zorder=4, linewidth=3)
        
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Targets Found')
        ax.set_title('Search Efficiency: Targets Found in Fixed Time')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0, max(max(ideal_found), max(animal_found), max(levy_found)) + 5])


def main():
    print("Generating Chapter 6 figures...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print('Figure 6.1: Movement Patterns'); generate_figure_6_1()
    print(f"✓ Saved figure: {OUTPUT_DIR}/6.1.png")
    print('Figure 6.2: Step Length Distributions'); generate_figure_6_2()
    print(f"✓ Saved figure: {OUTPUT_DIR}/6.2.png")
    print('Figure 6.3: Search Efficiency'); generate_figure_6_3()
    print(f"✓ Saved figure: {OUTPUT_DIR}/6.3.png")
    print("✓ All figures generated!")


if __name__ == "__main__":
    main()
