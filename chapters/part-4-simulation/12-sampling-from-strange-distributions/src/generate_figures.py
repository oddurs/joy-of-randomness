"""
Figure generation for Chapter 12: Sampling from Strange Distributions

Demonstrates inverse transform and rejection sampling techniques.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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


def generate_figure_12_1():
    """
    Figure 12.1: Inverse transform sampling visualization
    """
    np.random.seed(42)
    
    with figure(4, 12, 1, output_dir=OUTPUT_DIR) as fig:
        # Top left: Exponential CDF
        ax1 = fig.add_subplot(2, 2, 1)
        x = np.linspace(0, 4, 500)
        cdf = 1 - np.exp(-x)
        
        ax1.plot(x, cdf, 'b-', linewidth=2, label='CDF F(x) = 1 - exp(-x)')
        ax1.fill_between(x, 0, cdf, alpha=0.2, color='blue')
        
        # Show inverse transform for a few u values
        u_samples = [0.3, 0.6, 0.9]
        colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(u_samples)))
        
        for u, color in zip(u_samples, colors):
            x_inv = -np.log(1 - u)
            ax1.plot([0, u], [u, u], 'k--', alpha=0.3, linewidth=0.5)
            ax1.plot([u, u], [u, 0], 'k--', alpha=0.3, linewidth=0.5)
            ax1.plot(x_inv, u, 'o', color=color, markersize=8)
            ax1.text(x_inv, u+0.05, f'x={x_inv:.2f}', fontsize=8, ha='center', color=color)
        
        ax1.set_xlim(0, 4)
        ax1.set_ylim(0, 1)
        ax1.set_xlabel('x')
        ax1.set_ylabel('CDF value')
        ax1.set_title('Inverse Transform: F inverse(U) = X')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)
        
        # Top right: Uniform samples
        ax2 = fig.add_subplot(2, 2, 2)
        n_samples = 1000
        u_uniform = np.random.uniform(0, 1, n_samples)
        
        ax2.hist(u_uniform, bins=30, density=True, alpha=0.7, color='green', edgecolor='black')
        ax2.axhline(1, color='k', linestyle='--', linewidth=1, alpha=0.5, label='Uniform(0,1)')
        
        ax2.set_xlabel('U')
        ax2.set_ylabel('Density')
        ax2.set_title('Uniform Input')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Bottom left: Transformed samples
        ax3 = fig.add_subplot(2, 2, 3)
        x_samples = -np.log(1 - u_uniform)
        
        ax3.hist(x_samples, bins=40, density=True, alpha=0.7, color='purple', edgecolor='black')
        
        # Overlay true exponential PDF
        x_theory = np.linspace(0, 5, 200)
        pdf_theory = np.exp(-x_theory)
        ax3.plot(x_theory, pdf_theory, 'r-', linewidth=2, label='True Exponential(1)')
        
        ax3.set_xlabel('X')
        ax3.set_ylabel('Density')
        ax3.set_title('Transformed Output')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.set_xlim(0, 5)
        
        # Bottom right: Q-Q plot
        ax4 = fig.add_subplot(2, 2, 4)
        sample_quantiles = np.sort(x_samples)
        theoretical_quantiles = -np.log(1 - np.linspace(0.001, 0.999, len(sample_quantiles)))
        
        ax4.scatter(theoretical_quantiles, sample_quantiles, alpha=0.5, s=20, color='purple')
        ax4.plot([0, max(theoretical_quantiles)], [0, max(theoretical_quantiles)], 'r--', linewidth=2)
        
        ax4.set_xlabel('Theoretical Quantiles')
        ax4.set_ylabel('Sample Quantiles')
        ax4.set_title('Q-Q Plot (Perfect Match = True)')
        ax4.grid(True, alpha=0.3)


def generate_figure_12_2():
    """
    Figure 12.2: Rejection sampling visualization
    """
    np.random.seed(42)
    
    with figure(4, 12, 2, output_dir=OUTPUT_DIR) as fig:
        # Left: Geometric illustration
        ax1 = fig.add_subplot(1, 2, 1)
        
        # Target: Beta(2, 2)
        x = np.linspace(0, 1, 500)
        target_pdf = stats.beta.pdf(x, 2, 2)
        
        # Proposal: Uniform
        proposal_pdf = np.ones_like(x)
        m = np.max(target_pdf / proposal_pdf)  # M such that target <= M * proposal
        envelope = m * proposal_pdf
        
        ax1.fill_between(x, 0, envelope, alpha=0.2, color='gray', label='Envelope M*g(x)')
        ax1.fill_between(x, 0, target_pdf, alpha=0.5, color='blue', label='Target f(x)')
        ax1.plot(x, envelope, 'k--', linewidth=1.5, alpha=0.7)
        ax1.plot(x, target_pdf, 'b-', linewidth=2)
        
        # Show some sample points (accept/reject)
        np.random.seed(43)
        n_demo = 100
        x_samples = np.random.uniform(0, 1, n_demo)
        u_samples = np.random.uniform(0, 1, n_demo)
        
        accepts = u_samples <= target_pdf[np.searchsorted(x, x_samples)] / envelope[np.searchsorted(x, x_samples)]
        
        ax1.scatter(x_samples[accepts], u_samples[accepts] * envelope[np.searchsorted(x, x_samples[accepts])],
                   s=20, alpha=0.6, color='green', label='Accepted')
        ax1.scatter(x_samples[~accepts], u_samples[~accepts] * envelope[np.searchsorted(x, x_samples[~accepts])],
                   s=20, alpha=0.3, color='red', label='Rejected')
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, max(envelope) * 1.1)
        ax1.set_xlabel('x')
        ax1.set_ylabel('Density')
        ax1.set_title('Rejection Sampling: Accept/Reject Decision')
        ax1.legend(fontsize=9, loc='upper center')
        ax1.grid(True, alpha=0.3)
        
        # Right: Efficiency vs dimension
        ax2 = fig.add_subplot(1, 2, 2)
        
        dimensions = np.arange(1, 21)
        # For d-dimensional normals, rejection efficiency ~ exp(-c*d) for some c
        acceptance_rates = np.exp(-0.15 * dimensions)
        
        ax2.semilogy(dimensions, acceptance_rates * 100, 'o-', color='crimson', 
                    linewidth=2, markersize=6)
        
        ax2.axhline(1, color='gray', linestyle='--', alpha=0.5, label='1% acceptance')
        ax2.axhline(0.1, color='gray', linestyle='--', alpha=0.5, label='0.1% acceptance')
        
        ax2.set_xlabel('Dimension (d)')
        ax2.set_ylabel('Acceptance Rate (%)')
        ax2.set_title('Exponential Collapse in High Dimensions')
        ax2.grid(True, alpha=0.3, which='both')
        ax2.legend(fontsize=9)
        ax2.set_ylim([0.01, 100])


def generate_figure_12_3():
    """
    Figure 12.3: Comparison of different proposals
    """
    np.random.seed(42)
    
    with figure(4, 12, 3, output_dir=OUTPUT_DIR) as fig:
        x = np.linspace(-4, 4, 500)
        target = stats.norm.pdf(x)
        
        # Three proposals
        proposals = {
            'Exponential': (0.8, lambda x: np.exp(-np.abs(x)) / 2, 'blue'),
            'Uniform': (2.5, lambda x: np.where(np.abs(x) < 2, 0.25, 0), 'green'),
            'Laplace': (1.2, lambda x: 0.5 * np.exp(-np.abs(x)), 'red')
        }
        
        # Left: Envelopes
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.fill_between(x, 0, target, alpha=0.3, color='black', label='Target N(0,1)')
        
        for name, (m, prop_fn, color) in proposals.items():
            proposal = prop_fn(x)
            envelope = m * proposal
            ax1.plot(x, envelope, '--', linewidth=2, color=color, alpha=0.7, label=f'{name} (M={m:.1f})')
        
        ax1.plot(x, target, 'k-', linewidth=2.5)
        ax1.set_xlim(-4, 4)
        ax1.set_ylim(0, 1)
        ax1.set_xlabel('x')
        ax1.set_ylabel('Density')
        ax1.set_title('Envelopes for Different Proposals')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Right: Efficiency comparison
        ax2 = fig.add_subplot(1, 2, 2)
        
        names = list(proposals.keys())
        efficiencies = [1/m for m, _, _ in proposals.values()]
        colors_bars = [proposals[n][2] for n in names]
        
        bars = ax2.bar(names, efficiencies, color=colors_bars, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bar, eff in zip(bars, efficiencies):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{eff:.1%}', ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax2.set_ylabel('Acceptance Rate (1/M)')
        ax2.set_title('Proposal Efficiency: 1/M')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3, axis='y')


def generate_figure_12_4():
    """
    Figure 12.4: Ziggurat algorithm visualization
    """
    np.random.seed(42)
    
    with figure(4, 12, 4, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        # Ziggurat structure for normal distribution
        x = np.linspace(0, 4, 1000)
        pdf = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
        
        # Draw the distribution
        ax.fill_between(x, 0, pdf, alpha=0.2, color='blue', label='Target N(0,1)')
        ax.plot(x, pdf, 'b-', linewidth=2)
        
        # Draw ziggurat strips (simplified)
        n_strips = 8
        y_edges = []
        x_edges = []
        
        # Calculate ziggurat levels
        for i in range(n_strips):
            prob = (n_strips - i) / n_strips
            # Solve: integral from x_i to infinity = prob / n_strips
            # For normal, this is roughly x_i = sqrt(-2 * ln(prob))
            x_i = np.sqrt(-2 * np.log(prob / np.sqrt(2 * np.pi)))
            x_edges.append(x_i)
            y_i = np.exp(-x_i**2 / 2) / np.sqrt(2 * np.pi)
            y_edges.append(y_i)
        
        # Draw strips
        for i in range(len(x_edges) - 1):
            y_bottom = y_edges[i+1]
            y_top = y_edges[i]
            x_right = x_edges[i]
            
            rect_y = [y_bottom, y_top, y_top, y_bottom, y_bottom]
            rect_x = [0, 0, x_right, x_right, 0]
            
            color = plt.cm.Greens(0.3 + 0.6 * i / len(x_edges))
            ax.fill(rect_x, rect_y, color=color, alpha=0.5, edgecolor='darkgreen', linewidth=1)
            ax.text(x_right/2, (y_top + y_bottom)/2, f'L{i+1}', fontsize=8, ha='center', va='center')
        
        # Label the levels
        ax.text(3.5, 0.35, 'Most samples\nfrom L1\n(fast path)', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 0.45)
        ax.set_xlabel('x (positive side)')
        ax.set_ylabel('Density')
        ax.set_title('Ziggurat Algorithm: Stacked Strips for Efficient Sampling')
        ax.legend(fontsize=10, loc='upper right')
        ax.grid(True, alpha=0.3)


def main():
    """Generate all figures for Chapter 12."""
    print(f"Generating Chapter 12 figures...")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating Figure 12.1"); generate_figure_12_1()
    print(f"Generating Figure 12.2"); generate_figure_12_2()
    print(f"Generating Figure 12.3"); generate_figure_12_3()
    print(f"Generating Figure 12.4"); generate_figure_12_4()
    
    print()
    print("✓ All figures generated successfully!")


if __name__ == "__main__":
    main()
