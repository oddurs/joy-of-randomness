import matplotlib.pyplot as plt
import random
import statistics
import numpy as np
from pathlib import Path
import sys

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(chapter_dir))

from shared.figures import figure
from shared.figure_config import DEFAULT_FIGSIZE, DEFAULT_MARGIN_PAD

OUTPUT_DIR = Path(__file__).parent / "figures"


def generate_figure_3_1():
    """
    Figure 3.1: Running Proportion Convergence
    Shows how the proportion of heads converges to 0.5 over 10,000 flips.
    The line starts chaotic and gradually settles into a narrow band around 0.5.
    """
    # Generate coin flips
    num_flips = 10000
    proportions = []
    heads_so_far = 0
    
    for i in range(1, num_flips + 1):
        if random.random() < 0.5:
            heads_so_far += 1
        proportion = heads_so_far / i
        proportions.append(proportion)
    
    with figure(1, 3, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Plot the running proportion
        ax.plot(range(1, num_flips + 1), proportions, linewidth=1.5, color='steelblue', alpha=0.8)
        
        # Add horizontal line at 0.5
        ax.axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Expected proportion (0.5)')
        
        # Add shaded bands for reference
        ax.fill_between(range(1, num_flips + 1), 0.45, 0.55, alpha=0.1, color='gray', label='±5% band')
        
        ax.set_xlabel('Number of flips (log scale)')
        ax.set_ylabel('Proportion of heads')
        ax.set_title('Convergence to 0.5: Running Proportion Over 10,000 Coin Flips')
        ax.set_xscale('log')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)


def generate_figure_3_2():
    """
    Figure 3.2: Convergence Rate (1/√n)
    Shows how the standard deviation of the proportion shrinks as 1/√n.
    Multiple simulations show the envelope of typical fluctuation.
    """
    # Generate multiple simulations
    num_simulations = 100
    sample_sizes = np.logspace(1, 5, 50).astype(int)  # 10 to 100,000 flips
    
    with figure(1, 3, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Plot a few individual trajectories
        for i in range(10):
            proportions = []
            heads_so_far = 0
            for j in range(1, max(sample_sizes) + 1):
                if random.random() < 0.5:
                    heads_so_far += 1
                proportions.append(heads_so_far / j)
            ax.plot(range(1, max(sample_sizes) + 1), proportions, alpha=0.2, color='steelblue', linewidth=0.8)
        
        # Plot the theoretical envelope: 1/√n
        theoretical_bound = 1 / np.sqrt(np.array(range(1, max(sample_sizes) + 1)))
        ax.plot(range(1, max(sample_sizes) + 1), 0.5 + theoretical_bound, 'r--', linewidth=2, label='Typical envelope: 0.5 ± 1/sqrt(n)')
        ax.plot(range(1, max(sample_sizes) + 1), 0.5 - theoretical_bound, 'r--', linewidth=2)
        
        # Add baseline
        ax.axhline(0.5, color='black', linestyle='-', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Number of flips (log scale)')
        ax.set_ylabel('Proportion of heads')
        ax.set_title('Convergence Rate: Fluctuations Shrink as 1/sqrt(n)')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, which='both')


def generate_figure_3_3():
    """
    Figure 3.3: Absolute vs Relative Difference
    Left panel: Shows absolute difference (heads - tails) grows over time
    Right panel: Shows proportional difference shrinks over time
    """
    num_flips = 10000
    heads_count = 0
    absolute_diffs = []
    relative_diffs = []
    
    for i in range(1, num_flips + 1):
        if random.random() < 0.5:
            heads_count += 1
        tails_count = i - heads_count
        
        abs_diff = abs(heads_count - tails_count)
        rel_diff = abs_diff / i
        
        absolute_diffs.append(abs_diff)
        relative_diffs.append(rel_diff)
    
    with figure(1, 3, 3, figsize=(15, 6), output_dir=OUTPUT_DIR) as fig:
        # Left panel: Absolute difference
        ax1 = fig.add_subplot(121)
        ax1.plot(range(1, num_flips + 1), absolute_diffs, linewidth=1.5, color='steelblue', alpha=0.8)
        ax1.set_xlabel('Number of flips (log scale)')
        ax1.set_ylabel('|Heads - Tails|')
        ax1.set_title('Absolute Difference: Growing With Sample Size')
        ax1.set_xscale('log')
        ax1.grid(True, alpha=0.3)
        
        # Right panel: Relative difference
        ax2 = fig.add_subplot(122)
        ax2.plot(range(1, num_flips + 1), relative_diffs, linewidth=1.5, color='coral', alpha=0.8)
        ax2.set_xlabel('Number of flips (log scale)')
        ax2.set_ylabel('|Heads - Tails| / Total flips')
        ax2.set_title('Proportional Difference: Shrinking With Sample Size')
        ax2.set_xscale('log')
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle('The Key Distinction: Absolute vs Relative Imbalance', fontsize=13, y=1.00)


def generate_figure_3_4():
    """
    Figure 3.4: The Gambler's Fallacy - Dilution Not Reversal
    
    Shows how an early streak (60 heads in first 100 flips) gets diluted
    but doesn't "reverse" - subsequent flips are still 50/50.
    
    Key insight: The running proportion declines toward 0.5 not because
    tails are "catching up" but because the large sample of fair flips
    dilutes the effect of the initial excess.
    """
    # First batch: 100 flips with 60 heads (intentional streak)
    first_batch_size = 100
    first_batch_heads = 60
    first_batch_tails = 40
    
    # Subsequent batch: 9,900 fair flips (~50/50)
    num_additional_flips = 9900
    additional_heads = sum([1 for _ in range(num_additional_flips) if random.random() < 0.5])
    additional_tails = num_additional_flips - additional_heads
    
    # Build running proportions
    total_heads = first_batch_heads
    proportions = []
    flip_numbers = []
    
    # Add first batch
    for flip_num in range(1, first_batch_size + 1):
        if flip_num <= first_batch_heads:
            if flip_num == 1:
                total_heads = 1
            else:
                total_heads += 1 if flip_num <= first_batch_heads else 0
        prop = total_heads / flip_num
        proportions.append(prop)
        flip_numbers.append(flip_num)
    
    # Reset and do it properly
    total_heads = first_batch_heads
    proportions = [(total_heads / first_batch_size)]
    flip_numbers = [first_batch_size]
    
    # Add subsequent flips
    for i in range(1, num_additional_flips + 1):
        if i <= additional_heads:
            total_heads += 1
        total_flips = first_batch_size + i
        proportions.append(total_heads / total_flips)
        flip_numbers.append(total_flips)
    
    with figure(1, 3, 4, figsize=(14, 7), output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Shade the initial streak region
        ax.axvspan(0, first_batch_size, alpha=0.15, color='red', label='Initial streak (60/100 = 60%)')
        
        # Plot the running proportion
        ax.plot(flip_numbers, proportions, linewidth=2.5, color='steelblue', alpha=0.9, label='Running proportion')
        
        # Add the expected proportion line
        ax.axhline(0.5, color='green', linestyle='--', linewidth=2.2, alpha=0.8, label='Fair coin expectation (50%)')
        
        # Mark the transition point
        ax.axvline(first_batch_size, color='gray', linestyle=':', linewidth=1.5, alpha=0.6)
        
        # Add annotations
        ax.annotate('Initial excess:\n60% heads', 
                   xy=(first_batch_size/2, 0.60), 
                   fontsize=11, 
                   ha='center',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.1))
        
        ax.annotate('Dilution by fair flips\n(not reversal)', 
                   xy=(first_batch_size + num_additional_flips/2, 0.505), 
                   fontsize=11, 
                   ha='center',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.3))
        
        ax.set_xlabel('Total number of flips', fontsize=12)
        ax.set_ylabel('Proportion of heads', fontsize=12)
        ax.set_title('The Gambler\'s Fallacy: Early Streak Gets Diluted, Not Reversed', fontsize=13, pad=15)
        ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_ylim(0.48, 0.62)
        
        # Format x-axis with commas for readability
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

def generate_all_figures():
    """Generate all figures for Chapter 3."""
    print("Generating Chapter 3 figures...")
    print()
    
    print("Generating Figure 3.1: Running Proportion Convergence")
    generate_figure_3_1()
    
    print("Generating Figure 3.2: Convergence Rate (1/√n)")
    generate_figure_3_2()
    
    print("Generating Figure 3.3: Absolute vs Relative Difference")
    generate_figure_3_3()
    
    print("Generating Figure 3.4: The Gambler's Fallacy")
    generate_figure_3_4()
    
    print()
    print("All figures generated successfully!")


if __name__ == "__main__":
    generate_all_figures()
