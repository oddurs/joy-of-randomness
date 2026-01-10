import matplotlib.pyplot as plt
import matplotlib
import random
import statistics
import os
import numpy as np
import scienceplots  # noqa: F401

# Configure matplotlib with SciencePlots
matplotlib.style.use('science')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

OUTPUT_DIR = 'src/figures'


def save_figure(fig, filename):
    """Save figure with consistent settings."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.tight_layout(pad=1.5)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {filepath}")
    plt.close(fig)


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
    
    fig = plt.figure(figsize=(12, 6))
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
    
    save_figure(fig, "3.1.png")


def generate_figure_3_2():
    """
    Figure 3.2: Convergence Rate (1/√n)
    Shows how the standard deviation of the proportion shrinks as 1/√n.
    Multiple simulations show the envelope of typical fluctuation.
    """
    # Generate multiple simulations
    num_simulations = 100
    sample_sizes = np.logspace(1, 5, 50).astype(int)  # 10 to 100,000 flips
    
    fig = plt.figure(figsize=(12, 6))
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
    
    save_figure(fig, "3.2.png")


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
    
    fig = plt.figure(figsize=(14, 5))
    
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
    
    fig.suptitle('The Key Distinction: Absolute vs Relative Imbalance', fontsize=13, y=1.02)
    
    save_figure(fig, "3.3.png")


def generate_figure_3_4():
    """
    Figure 3.4: Gambler's Fallacy Illustration
    Shows how an early streak (e.g., 60 heads in first 100 flips) gets diluted
    but doesn't "reverse" - subsequent flips are still 50/50.
    """
    # First batch: 100 flips starting with an intentional streak
    first_batch_size = 100
    first_batch_heads = 60  # Start with a streak (60 heads, 40 tails)
    
    # Generate subsequent flips
    num_additional_flips = 9900
    additional_heads = sum([1 for _ in range(num_additional_flips) if random.random() < 0.5])
    
    # Track cumulative proportion
    proportions = []
    batch_boundaries = []
    
    # Add the first batch proportion
    proportions.append(first_batch_heads / first_batch_size)
    batch_boundaries.append(first_batch_size)
    
    # Add proportions as we add more flips
    total_heads = first_batch_heads
    for i in range(1, num_additional_flips + 1):
        if i <= additional_heads:
            total_heads += 1
        total_flips = first_batch_size + i
        proportion = total_heads / total_flips
        proportions.append(proportion)
    
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    
    # Plot the running proportion
    flip_counts = np.arange(first_batch_size, first_batch_size + num_additional_flips + 1)
    ax.plot(flip_counts, proportions, linewidth=2, color='steelblue', label='Running proportion')
    
    # Mark the first batch
    ax.axvline(first_batch_size, color='red', linestyle='--', linewidth=2, alpha=0.5, label='End of initial streak (100 flips)')
    
    # Add the expected proportion line
    ax.axhline(0.5, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Expected proportion (0.5)')
    
    # Shade the initial streak region
    ax.axvspan(0, first_batch_size, alpha=0.1, color='red', label='Initial streak region')
    
    ax.set_xlabel('Number of flips')
    ax.set_ylabel('Proportion of heads')
    ax.set_title('Gambler\'s Fallacy: Early Streak Gets Diluted, Not Reversed')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.45, 0.65)
    
    save_figure(fig, "3.4.png")


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
    
    print("Generating Figure 3.4: Gambler's Fallacy Illustration")
    generate_figure_3_4()
    
    print()
    print("All figures generated successfully!")


if __name__ == "__main__":
    generate_all_figures()
