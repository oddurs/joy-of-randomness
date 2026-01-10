"""
Figure generation for Chapter 18: (Chapter name not yet added)

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

def generate_figure_18_1():
    """
    Figure 18.1: Regression Fit
    """
    random.seed(42)
    
    with figure(6, 18, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 18.1', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 18.1')


def generate_figure_18_2():
    """
    Figure 18.2: Changepoint Posterior
    """
    random.seed(42)
    
    with figure(6, 18, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 18.2', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 18.2')


def generate_figure_18_3():
    """
    Figure 18.3: Hierarchical Comparison
    """
    random.seed(42)
    
    with figure(6, 18, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 18.3', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 18.3')


def main():
    """Generate all figures for Chapter 18."""
    print(f"Generating Chapter 18 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 18.1"); generate_figure_18_1()
    print(f"Generating Figure 18.2"); generate_figure_18_2()
    print(f"Generating Figure 18.3"); generate_figure_18_3()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
