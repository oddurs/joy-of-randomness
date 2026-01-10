"""
Figure generation for Chapter 13: (Chapter name not yet added)

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

def generate_figure_13_1():
    """
    Figure 13.1: Deterministic Vs Stochastic
    """
    random.seed(42)
    
    with figure(5, 13, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 13.1', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 13.1')


def generate_figure_13_2():
    """
    Figure 13.2: Extinction Probability
    """
    random.seed(42)
    
    with figure(5, 13, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 13.2', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 13.2')


def generate_figure_13_3():
    """
    Figure 13.3: Major Outbreak Vs R0
    """
    random.seed(42)
    
    with figure(5, 13, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 13.3', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 13.3')


def generate_figure_13_4():
    """
    Figure 13.4: Superspreaders Effect
    """
    random.seed(42)
    
    with figure(5, 13, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 13.4', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 13.4')


def main():
    """Generate all figures for Chapter 13."""
    print(f"Generating Chapter 13 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 13.1"); generate_figure_13_1()
    print(f"Generating Figure 13.2"); generate_figure_13_2()
    print(f"Generating Figure 13.3"); generate_figure_13_3()
    print(f"Generating Figure 13.4"); generate_figure_13_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
