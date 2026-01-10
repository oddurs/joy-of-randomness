#!/usr/bin/env python3
"""
Generate template figure generation files for all chapters.
Run this in the repo root to create generate_figures.py for chapters 5-18.
"""

import os
import re
from pathlib import Path

# Chapters 5-18 with their (part, chapter) tuples
CHAPTERS = {
    5: (2, 5),   # Wandering in Two Dimensions
    6: (2, 6),   # Random Walks in the Wild
    7: (3, 7),   # What Comes Next
    8: (3, 8),   # Chains Everywhere
    9: (3, 9),   # The Chain That Ranked the Internet
    10: (4, 10), # Throwing Darts at Pi
    11: (4, 11), # When Exact is Impossible
    12: (4, 12), # Sampling from Strange Distributions
    13: (5, 13), # Epidemics
    14: (5, 14), # Queues and Waiting
    15: (5, 15), # Populations
    16: (6, 16), # Thinking in Distributions
    17: (6, 17), # Markov Chain Monte Carlo
    18: (6, 18), # Fitting Models to Messy Data
}

def find_chapter_dir(chapter_num):
    """Find the directory for a chapter."""
    base = Path("/Users/oddurs/Code/joy-of-randomness/chapters")
    
    # Search all subdirectories for matching chapter
    for d in base.rglob("*"):
        if not d.is_dir():
            continue
        name = d.name
        # Check if directory name matches pattern like "05-chapter-name"
        if re.match(rf'^0?{chapter_num}-', name):
            return d
    
    return None

def extract_plot_functions(simulations_path):
    """Extract plot function names from simulations.py."""
    if not simulations_path.exists():
        return []
    
    content = simulations_path.read_text()
    matches = re.findall(r'^def (plot_\w+|visualize_\w+)', content, re.MULTILINE)
    return matches

def create_generate_figures(chapter_num, chapter_dir):
    """Create a generate_figures.py for a chapter."""
    part, chapter = CHAPTERS[chapter_num]
    plot_functions = extract_plot_functions(chapter_dir / "simulations.py")
    
    if not plot_functions:
        print(f"  No plot functions found for Chapter {chapter_num}, using minimal template")
        num_figures = 3
    else:
        num_figures = len(plot_functions)
    
    # Generate import statements and function calls
    imports = []
    function_calls = []
    figure_gens = []
    
    for i, func in enumerate(plot_functions[:num_figures]):
        figure_num = i + 1
        function_calls.append(f"    generate_figure_{chapter}_{figure_num}()")
        figure_gens.append(f'''
def generate_figure_{chapter}_{figure_num}():
    """
    Figure {chapter}.{figure_num}: {func.replace('plot_', '').replace('visualize_', '').replace('_', ' ').title()}
    """
    random.seed(42)
    
    with figure({part}, {chapter}, {figure_num}, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        # TODO: Implement figure generation
        ax.text(0.5, 0.5, 'Figure {chapter}.{figure_num}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure {chapter}.{figure_num}')
''')
    
    # Fill in gaps with minimal figures if needed
    while len(function_calls) < max(3, num_figures):
        fig_num = len(function_calls) + 1
        function_calls.append(f"    generate_figure_{chapter}_{fig_num}()")
        figure_gens.append(f'''
def generate_figure_{chapter}_{fig_num}():
    """
    Figure {chapter}.{fig_num}: Placeholder
    """
    random.seed(42)
    
    with figure({part}, {chapter}, {fig_num}, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Figure {chapter}.{fig_num}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Figure {chapter}.{fig_num}')
''')
    
    content = f'''"""
Figure generation for Chapter {chapter}: {'(Chapter name not yet added)'}

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
{chr(10).join(figure_gens)}

def main():
    """Generate all figures for Chapter {chapter}."""
    print(f"Generating Chapter {chapter} figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
{chr(10).join(f'    print(f"Generating Figure {chapter}.{i+1}"); generate_figure_{chapter}_{i+1}()' for i in range(len(function_calls)))}
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
'''
    
    return content

# Generate for chapters 5-18
for chapter_num in range(6, 19):  # 6-18 (5 is done manually)
    chapter_dir = find_chapter_dir(chapter_num)
    if not chapter_dir:
        print(f"Chapter {chapter_num}: NOT FOUND")
        continue
    
    print(f"Creating Chapter {chapter_num}: {chapter_dir.name}")
    content = create_generate_figures(chapter_num, chapter_dir)
    
    output_file = chapter_dir / "src" / "generate_figures.py"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content)
    print(f"  ✓ Created {output_file}")

print("\nDone!")
