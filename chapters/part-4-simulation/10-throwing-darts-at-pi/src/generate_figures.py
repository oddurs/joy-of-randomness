"""
Figure generation for Chapter 10: Throwing Darts at Pi

Generates publication-quality figures for Monte Carlo integration and pi estimation.
"""

import sys
from pathlib import Path
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


def generate_figure_10_1():
    """
    Figure 10.1: Darts hitting the circle - visualization of random sampling
    """
    np.random.seed(42)
    n_darts = 5000
    
    # Random points in [-1, 1] x [-1, 1]
    x = np.random.uniform(-1, 1, n_darts)
    y = np.random.uniform(-1, 1, n_darts)
    distance = np.sqrt(x**2 + y**2)
    
    # Split into inside and outside
    inside = distance <= 1
    outside = ~inside
    
    with figure(4, 10, 1, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Plot points
        ax.scatter(x[inside], y[inside], s=1, alpha=0.5, color='crimson', label='Inside circle')
        ax.scatter(x[outside], y[outside], s=1, alpha=0.5, color='steelblue', label='Outside circle')
        
        # Draw circle
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2)
        
        # Draw square
        ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k-', linewidth=2)
        
        # Estimate pi
        pi_est = 4 * inside.sum() / n_darts
        
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Random Darts in Circle (n={n_darts:,}, pi est. = {pi_est:.4f})')
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.2)


def generate_figure_10_2():
    """
    Figure 10.2: Convergence of pi estimate with increasing sample size
    """
    np.random.seed(42)
    
    # Generate many darts
    n_max = 100000
    x = np.random.uniform(-1, 1, n_max)
    y = np.random.uniform(-1, 1, n_max)
    distance = np.sqrt(x**2 + y**2)
    inside = distance <= 1
    
    # Calculate running estimate
    n_samples = np.logspace(1, 5, 50, dtype=int)
    pi_estimates = []
    
    for n in n_samples:
        hits = inside[:n].sum()
        pi_est = 4 * hits / n
        pi_estimates.append(pi_est)
    
    with figure(4, 10, 2, output_dir=OUTPUT_DIR) as fig:
        # Left: estimate vs sample size
        ax1 = fig.add_subplot(121)
        ax1.semilogx(n_samples, pi_estimates, 'o-', color='steelblue', linewidth=2, markersize=4)
        ax1.axhline(np.pi, color='red', linestyle='--', linewidth=2, label='True pi')
        ax1.fill_between(n_samples, np.pi - 0.1, np.pi + 0.1, alpha=0.1, color='red')
        
        ax1.set_xlabel('Number of Samples')
        ax1.set_ylabel('Estimated pi')
        ax1.set_title('Convergence of pi Estimate')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3, which='both')
        ax1.set_ylim([2.8, 3.6])
        
        # Right: error vs sample size
        ax2 = fig.add_subplot(122)
        errors = np.abs(np.array(pi_estimates) - np.pi)
        ax2.loglog(n_samples, errors, 'o-', color='crimson', linewidth=2, markersize=4)
        
        # Theoretical 1/sqrt(n) line
        theoretical_error = 1 / np.sqrt(n_samples)
        ax2.loglog(n_samples, theoretical_error, 'k--', linewidth=2, alpha=0.5, label='1/sqrt(n)')
        
        ax2.set_xlabel('Number of Samples')
        ax2.set_ylabel('Absolute Error')
        ax2.set_title('Error Convergence (log-log)')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, which='both')


def generate_figure_10_3():
    """
    Figure 10.3: Error scaling and confidence intervals
    """
    np.random.seed(42)
    
    n_trials = 50
    n_darts_list = np.logspace(1.5, 5, 10, dtype=int)
    
    all_estimates = []
    
    for n_darts in n_darts_list:
        estimates = []
        for trial in range(n_trials):
            x = np.random.uniform(-1, 1, n_darts)
            y = np.random.uniform(-1, 1, n_darts)
            distance = np.sqrt(x**2 + y**2)
            inside = (distance <= 1).sum()
            pi_est = 4 * inside / n_darts
            estimates.append(pi_est)
        all_estimates.append(estimates)
    
    with figure(4, 10, 3, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Calculate statistics
        means = [np.mean(ests) for ests in all_estimates]
        stds = [np.std(ests) for ests in all_estimates]
        ci_lower = [m - 1.96*s for m, s in zip(means, stds)]
        ci_upper = [m + 1.96*s for m, s in zip(means, stds)]
        
        # Plot mean and confidence intervals
        ax.errorbar(n_darts_list, means, yerr=[np.array(means) - np.array(ci_lower), 
                                                 np.array(ci_upper) - np.array(means)],
                   fmt='o-', color='steelblue', ecolor='steelblue', capsize=5, 
                   capthick=2, linewidth=2, markersize=6, label='95% CI')
        
        ax.axhline(np.pi, color='red', linestyle='--', linewidth=2, label='True pi')
        
        ax.set_xscale('log')
        ax.set_xlabel('Number of Samples (per trial)')
        ax.set_ylabel('Estimated pi')
        ax.set_title('Distribution of pi Estimates (50 trials each)')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which='both')
        ax.set_ylim([2.8, 3.5])


def generate_figure_10_4():
    """
    Figure 10.4: High-dimensional hypersphere volumes
    
    As dimension increases, most of the volume is near the boundary.
    """
    np.random.seed(42)
    
    dimensions = np.arange(1, 11)
    n_samples = 100000
    
    volume_estimates = []
    
    for d in dimensions:
        # Sample from unit hypercube and check if in unit ball
        points = np.random.uniform(-1, 1, (n_samples, d))
        distances = np.sqrt((points**2).sum(axis=1))
        inside = (distances <= 1).sum()
        
        # Volume = (2^d) * (fraction inside)
        # True volume of d-ball = pi^(d/2) / gamma(d/2 + 1)
        volume_est = (2**d) * inside / n_samples
        volume_estimates.append(volume_est)
    
    # True volumes
    from scipy.special import gamma
    true_volumes = [np.pi**(d/2) / gamma(d/2 + 1) for d in dimensions]
    
    with figure(4, 10, 4, output_dir=OUTPUT_DIR) as fig:
        # Left: volume vs dimension
        ax1 = fig.add_subplot(121)
        ax1.semilogy(dimensions, true_volumes, 'o-', color='crimson', linewidth=2, 
                    markersize=6, label='True volume')
        ax1.semilogy(dimensions, volume_estimates, 's--', color='steelblue', linewidth=2, 
                    markersize=5, alpha=0.7, label='MC estimate')
        
        ax1.set_xlabel('Dimension')
        ax1.set_ylabel('Volume of Unit Ball (log scale)')
        ax1.set_title('Hypersphere Volumes by Dimension')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3, which='both')
        
        # Right: percentage of cube volume
        ax2 = fig.add_subplot(122)
        percentage = [100 * v / (2**d) for v, d in zip(true_volumes, dimensions)]
        ax2.semilogy(dimensions, percentage, 'go-', linewidth=2, markersize=6)
        
        ax2.set_xlabel('Dimension')
        ax2.set_ylabel('Percentage of Cube (log scale)')
        ax2.set_title('Ball as Fraction of Hypercube')
        ax2.grid(True, alpha=0.3, which='both')


def main():
    """Generate all figures for Chapter 10."""
    print(f"Generating Chapter 10 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 10.1"); generate_figure_10_1()
    print(f"Generating Figure 10.2"); generate_figure_10_2()
    print(f"Generating Figure 10.3"); generate_figure_10_3()
    print(f"Generating Figure 10.4"); generate_figure_10_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
