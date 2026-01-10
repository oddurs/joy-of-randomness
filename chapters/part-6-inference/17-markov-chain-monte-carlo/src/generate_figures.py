"""
Figure generation for Chapter 17: (Chapter name not yet added)

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

def generate_figure_17_1():
    """
    Figure 17.1: Mcmc Trace And Density
    """
    random.seed(42)
    
    with figure(6, 17, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 17.1', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 17.1')


def generate_figure_17_2():
    """
    Figure 17.2: Mcmc 2D
    """
    random.seed(42)
    
    with figure(6, 17, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 17.2', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 17.2')


def generate_figure_17_3():
    """
    Figure 17.3: Proposal Effect
    """
    random.seed(42)
    
    with figure(6, 17, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 17.3', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 17.3')


def generate_figure_17_4():
    """
    Figure 17.4: Autocorrelation
    """
    random.seed(42)
    
    with figure(6, 17, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 17.4', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 17.4')


def main():
    """Generate all figures for Chapter 17."""
    print(f"Generating Chapter 17 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 17.1"); generate_figure_17_1()
    print(f"Generating Figure 17.2"); generate_figure_17_2()
    print(f"Generating Figure 17.3"); generate_figure_17_3()
    print(f"Generating Figure 17.4"); generate_figure_17_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
