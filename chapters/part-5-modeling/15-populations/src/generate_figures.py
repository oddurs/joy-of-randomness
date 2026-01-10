"""
Figure generation for Chapter 15: (Chapter name not yet added)

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

def generate_figure_15_1():
    """
    Figure 15.1: Population Trajectories
    """
    random.seed(42)
    
    with figure(5, 15, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 15.1', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 15.1')


def generate_figure_15_2():
    """
    Figure 15.2: Extinction Probability Vs Initial Population
    """
    random.seed(42)
    
    with figure(5, 15, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 15.2', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 15.2')


def generate_figure_15_3():
    """
    Figure 15.3: Density Dependent Vs Independent
    """
    random.seed(42)
    
    with figure(5, 15, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 15.3', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 15.3')


def generate_figure_15_4():
    """
    Figure 15.4: Allee Effect
    """
    random.seed(42)
    
    with figure(5, 15, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 15.4', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 15.4')


def generate_figure_15_5():
    """
    Figure 15.5: Metapopulation Dynamics
    """
    random.seed(42)
    
    with figure(5, 15, 5, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure 15.5', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure 15.5')


def main():
    """Generate all figures for Chapter 15."""
    print(f"Generating Chapter 15 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 15.1"); generate_figure_15_1()
    print(f"Generating Figure 15.2"); generate_figure_15_2()
    print(f"Generating Figure 15.3"); generate_figure_15_3()
    print(f"Generating Figure 15.4"); generate_figure_15_4()
    print(f"Generating Figure 15.5"); generate_figure_15_5()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
