"""
Figure generation for Chapter 14: (Chapter name not yet added)

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

OUTPUT_DIR = Path(__file__).parent / "figures"

def generate_figure_14_1():
    """
    Figure 14.1: Queue Dynamics
    """
    random.seed(42)
    
    with figure(5, 14, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 14.1', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 14.1')


def generate_figure_14_2():
    """
    Figure 14.2: Utilization Effect
    """
    random.seed(42)
    
    with figure(5, 14, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 14.2', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 14.2')


def generate_figure_14_3():
    """
    Figure 14.3: Single Vs Multiple Servers
    """
    random.seed(42)
    
    with figure(5, 14, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 14.3', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 14.3')


def generate_figure_14_4():
    """
    Figure 14.4: Stationary Distribution
    """
    random.seed(42)
    
    with figure(5, 14, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 14.4', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 14.4')


def main():
    """Generate all figures for Chapter 14."""
    print(f"Generating Chapter 14 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 14.1"); generate_figure_14_1()
    print(f"Generating Figure 14.2"); generate_figure_14_2()
    print(f"Generating Figure 14.3"); generate_figure_14_3()
    print(f"Generating Figure 14.4"); generate_figure_14_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
