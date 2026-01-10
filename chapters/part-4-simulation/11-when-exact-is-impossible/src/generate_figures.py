"""
Figure generation for Chapter 11: When Exact Is Impossible

Demonstrates curse of dimensionality and why Monte Carlo dominates in high dimensions.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

# Disable LaTeX rendering to avoid special character issues
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_11_1():
    """
    Figure 11.1: Grid vs Monte Carlo complexity scaling
    """
    np.random.seed(42)
    
    dimensions = np.arange(1, 16)
    m = 10  # bins per dimension
    
    # Grid method: m^d points
    grid_complexity = m ** dimensions
    
    # Monte Carlo: fixed 10,000 samples
    monte_carlo_complexity = np.full_like(dimensions, 10000, dtype=float)
    
    with figure(4, 11, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.semilogy(dimensions, grid_complexity, 'o-', color='crimson', 
                   linewidth=2, markersize=6, label='Grid method')
        ax.semilogy(dimensions, monte_carlo_complexity, 's-', color='steelblue', 
                   linewidth=2, markersize=6, label='Monte Carlo (fixed 10k)')
        
        # Highlight breakeven
        ax.axvline(4.5, color='gray', linestyle='--', alpha=0.5)
        ax.text(4.5, 1e8, 'Breakeven', fontsize=9, ha='center', 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.set_xlabel('Dimension (d)')
        ax.set_ylabel('Number of Samples (log scale)')
        ax.set_title('Curse of Dimensionality: Grid vs Monte Carlo')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3, which='both')
        ax.set_ylim([1e0, 1e20])


def generate_figure_11_2():
    """
    Figure 11.2: Volume concentration in corners and distance concentration
    """
    np.random.seed(42)
    
    dimensions = np.arange(1, 21)
    
    # Volume concentration in interior [0.1, 0.9]^d
    interior_volume = (0.8) ** dimensions
    
    with figure(4, 11, 2, output_dir=OUTPUT_DIR) as fig:
        # Left: Interior volume fraction
        ax1 = fig.add_subplot(121)
        ax1.semilogy(dimensions, interior_volume, 'o-', color='crimson', 
                    linewidth=2, markersize=5)
        ax1.axhline(0.5, color='gray', linestyle='--', alpha=0.3)
        ax1.axhline(0.01, color='gray', linestyle='--', alpha=0.3)
        
        ax1.set_xlabel('Dimension (d)')
        ax1.set_ylabel('Interior Volume Fraction (log scale)')
        ax1.set_title('Volume Concentrates at Boundaries')
        ax1.grid(True, alpha=0.3, which='both')
        
        # Annotate key points
        for d, vol in [(1, interior_volume[0]), (5, interior_volume[4]), 
                       (10, interior_volume[9]), (20, interior_volume[19])]:
            ax1.annotate(f'{vol:.1%}', xy=(d, vol), xytext=(5, -10),
                        textcoords='offset points', fontsize=8, 
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        # Right: Distance concentration ratio
        ax2 = fig.add_subplot(122)
        
        # Simulate distance concentration
        distance_ratios = []
        for d in dimensions:
            points = np.random.uniform(0, 1, (100, d))
            distances = np.linalg.norm(points[:, np.newaxis, :] - points[np.newaxis, :, :], axis=2)
            distances = distances[distances > 1e-10]
            ratio = distances.max() / distances.min()
            distance_ratios.append(ratio)
        
        ax2.semilogy(dimensions, distance_ratios, 's-', color='steelblue',
                    linewidth=2, markersize=5)
        ax2.axhline(1.1, color='gray', linestyle='--', alpha=0.3, label='Within 10%')
        
        ax2.set_xlabel('Dimension (d)')
        ax2.set_ylabel('Max Distance / Min Distance')
        ax2.set_title('Distance Concentration (All Distances Become Similar)')
        ax2.grid(True, alpha=0.3, which='both')
        ax2.legend(fontsize=9)
        ax2.set_ylim([1, 10])


def generate_figure_11_3():
    """
    Figure 11.3: Random vectors become nearly orthogonal in high dimensions
    """
    np.random.seed(42)
    
    dimensions = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
    angles = []
    
    for d in dimensions:
        # Generate two random vectors
        u = np.random.randn(d)
        v = np.random.randn(d)
        
        # Angle between them
        cos_angle = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        angle_deg = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
        angles.append(angle_deg)
    
    with figure(4, 11, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.semilogx(dimensions, angles, 'o-', color='darkgreen', 
                   linewidth=2, markersize=6)
        ax.axhline(90, color='red', linestyle='--', linewidth=2, alpha=0.5, 
                  label='Orthogonal (90 degrees)')
        
        ax.set_xlabel('Dimension (d)')
        ax.set_ylabel('Angle Between Random Vectors (degrees)')
        ax.set_title('Random Vectors Become Nearly Orthogonal')
        ax.grid(True, alpha=0.3, which='both')
        ax.set_ylim([0, 95])
        ax.legend(fontsize=10)
        
        # Annotate some points
        for d, angle in zip(dimensions[::2], np.array(angles)[::2]):
            ax.annotate(f'{angle:.1f} deg', xy=(d, angle), xytext=(0, 10),
                       textcoords='offset points', fontsize=8, ha='center',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))


def generate_figure_11_4():
    """
    Figure 11.4: Hypersphere volumes across dimensions
    Shows the unintuitive peak in volume around d=5-6
    """
    np.random.seed(42)
    
    dimensions = np.arange(1, 41)
    
    # Volume of unit ball in d dimensions: pi^(d/2) / gamma(d/2 + 1)
    volumes = [np.pi**(d/2) / gamma(d/2 + 1) for d in dimensions]
    
    with figure(4, 11, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        ax.plot(dimensions, volumes, 'o-', color='purple', linewidth=2, markersize=4)
        
        # Find maximum
        max_idx = np.argmax(volumes)
        max_d = dimensions[max_idx]
        max_vol = volumes[max_idx]
        
        ax.plot(max_d, max_vol, 'r*', markersize=20, label=f'Peak at d={max_d}')
        ax.axvline(max_d, color='red', linestyle='--', alpha=0.3)
        ax.annotate(f'Max at d={max_d}\nVolume = {max_vol:.3f}',
                   xy=(max_d, max_vol), xytext=(max_d+5, max_vol*0.7),
                   fontsize=9, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                   arrowprops=dict(arrowstyle='->', color='red', alpha=0.5))
        
        ax.set_xlabel('Dimension (d)')
        ax.set_ylabel('Volume of Unit Ball')
        ax.set_title('Hypersphere Volumes Peak Then Vanish in High Dimensions')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)


def main():
    """Generate all figures for Chapter 11."""
    print(f"Generating Chapter 11 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 11.1"); generate_figure_11_1()
    print(f"Generating Figure 11.2"); generate_figure_11_2()
    print(f"Generating Figure 11.3"); generate_figure_11_3()
    print(f"Generating Figure 11.4"); generate_figure_11_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()

