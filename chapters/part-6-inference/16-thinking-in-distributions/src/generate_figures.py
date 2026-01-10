"""Generate figures for Chapter 16: Thinking in Distributions."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
matplotlib.rcParams['mathtext.fontset'] = 'stix'
import matplotlib.pyplot as plt
from scipy.stats import binom, beta
import sys
from pathlib import Path

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_figure_16_1():
    """Figure 16.1: Prior, Likelihood, and Posterior."""
    with figure(6, 16, 1, output_dir=OUTPUT_DIR) as fig:
        # Data: 7 heads in 10 flips
        n_successes = 7
        n_trials = 10
        
        theta = np.linspace(0, 1, 1000)
        
        # Prior: Uniform(0, 1) = Beta(1, 1)
        prior = beta.pdf(theta, 1, 1)
        
        # Likelihood: Binomial
        likelihood = binom.pmf(n_successes, n_trials, theta)
        likelihood = likelihood / np.max(likelihood)  # Normalize for visualization
        
        # Posterior: Beta(8, 4)
        posterior = beta.pdf(theta, n_successes + 1, n_trials - n_successes + 1)
        
        # Three subplots
        ax = fig.add_subplot(1, 3, 1)
        ax.fill_between(theta, prior, alpha=0.6, color='steelblue')
        ax.plot(theta, prior, linewidth=2, color='steelblue')
        ax.set_xlabel(r'$\theta$ (probability of heads)')
        ax.set_ylabel('Density')
        ax.set_title(r'Prior: $\mathrm{Beta}(1,1)$')
        ax.grid(alpha=0.3)
        
        ax = fig.add_subplot(1, 3, 2)
        ax.fill_between(theta, likelihood, alpha=0.6, color='orange')
        ax.plot(theta, likelihood, linewidth=2, color='orange')
        ax.set_xlabel(r'$\theta$')
        ax.set_ylabel('Likelihood (normalized)')
        ax.set_title(f'Likelihood: {n_successes} heads in {n_trials} flips')
        ax.grid(alpha=0.3)
        
        ax = fig.add_subplot(1, 3, 3)
        ax.fill_between(theta, posterior, alpha=0.6, color='red')
        ax.plot(theta, posterior, linewidth=2, color='red')
        ax.set_xlabel(r'$\theta$')
        ax.set_ylabel('Density')
        ax.set_title(r'Posterior: $\mathrm{Beta}(8,4)$')
        ax.grid(alpha=0.3)
        
        plt.tight_layout()

def generate_figure_16_2():
    """Figure 16.2: Effect of different priors."""
    with figure(6, 16, 2, output_dir=OUTPUT_DIR) as fig:
        n_successes = 7
        n_trials = 10
        theta = np.linspace(0, 1, 1000)
        
        # Three priors
        priors = [
            (r'Uniform: $\mathrm{Beta}(1,1)$', 1, 1),
            (r'Skeptical: $\mathrm{Beta}(10,10)$', 10, 10),
            (r'Diffuse: $\mathrm{Beta}(0.5,0.5)$', 0.5, 0.5),
        ]
        
        colors = ['steelblue', 'orange', 'green']
        
        for idx, (name, alpha, beta_param) in enumerate(priors):
            ax = fig.add_subplot(2, 2, idx + 1)
            
            # Prior
            prior = beta.pdf(theta, alpha, beta_param)
            ax.plot(theta, prior, linewidth=1.5, label='Prior', color=colors[idx], alpha=0.5)
            
            # Posterior
            post_alpha = alpha + n_successes
            post_beta = beta_param + (n_trials - n_successes)
            posterior = beta.pdf(theta, post_alpha, post_beta)
            
            ax.fill_between(theta, posterior, alpha=0.6, color=colors[idx])
            ax.plot(theta, posterior, linewidth=2, color=colors[idx], label='Posterior')
            
            ax.set_xlabel(r'$\theta$')
            ax.set_ylabel('Density')
            ax.set_title(name)
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)
        
        # Bottom right: credible intervals
        ax = fig.add_subplot(2, 2, 4)
        credible_intervals = []
        
        for name, alpha, beta_param in priors:
            post_alpha = alpha + n_successes
            post_beta = beta_param + (n_trials - n_successes)
            ci_lower = beta.ppf(0.025, post_alpha, post_beta)
            ci_upper = beta.ppf(0.975, post_alpha, post_beta)
            credible_intervals.append((ci_lower, ci_upper))
        
        names = ['Uniform', 'Skeptical', 'Diffuse']
        y_pos = np.arange(len(names))
        
        for i, (lower, upper) in enumerate(credible_intervals):
            ax.plot([lower, upper], [i, i], 'o-', linewidth=2, markersize=6, color=colors[i])
            ax.text(upper + 0.02, i, f'[{lower:.2f}, {upper:.2f}]', fontsize=9, va='center')
        
        ax.axvline(7/10, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Observed frequency')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names)
        ax.set_xlabel(r'95\% Credible Interval for $\theta$')
        ax.set_title('Effect of Prior on Credible Interval')
        ax.grid(alpha=0.3, axis='x')
        ax.legend(fontsize=9)
        ax.set_xlim([0, 1])
        
        plt.tight_layout()

def generate_figure_16_3():
    """Figure 16.3: Convergence with more data."""
    with figure(6, 16, 3, output_dir=OUTPUT_DIR) as fig:
        theta = np.linspace(0, 1, 1000)
        true_theta = 0.6
        
        # Different sample sizes, same frequency
        sample_sizes = [10, 50, 200, 1000]
        frequencies = [int(n * true_theta) for n in sample_sizes]
        
        for idx, (n, k) in enumerate(zip(sample_sizes, frequencies)):
            ax = fig.add_subplot(2, 2, idx + 1)
            
            # Three priors
            priors = [(1, 1), (10, 10), (0.5, 0.5)]
            colors_prior = ['steelblue', 'orange', 'green']
            
            for (alpha, beta_param), color in zip(priors, colors_prior):
                post_alpha = alpha + k
                post_beta = beta_param + (n - k)
                posterior = beta.pdf(theta, post_alpha, post_beta)
                ax.plot(theta, posterior, linewidth=1.5, color=color, alpha=0.7)
            
            ax.axvline(true_theta, color='red', linestyle='--', linewidth=2, label=f'True value')
            ax.set_xlabel(r'$\theta$')
            ax.set_ylabel('Density')
            ax.set_title(f'n = {n}, k = {k}')
            ax.grid(alpha=0.3)
            if idx == 0:
                ax.legend(fontsize=9)
        
        plt.tight_layout()

def generate_figure_16_4():
    """Figure 16.4: A/B testing."""
    with figure(6, 16, 4, output_dir=OUTPUT_DIR) as fig:
        # Design A: 12 conversions out of 100
        a_conversions = 12
        a_trials = 100
        
        # Design B: 18 conversions out of 100
        b_conversions = 18
        b_trials = 100
        
        theta = np.linspace(0, 0.4, 1000)
        
        # Posteriors (Beta(1,1) prior)
        posterior_a = beta.pdf(theta, a_conversions + 1, a_trials - a_conversions + 1)
        posterior_b = beta.pdf(theta, b_conversions + 1, b_trials - b_conversions + 1)
        
        # Left: posterior distributions
        ax = fig.add_subplot(1, 2, 1)
        ax.fill_between(theta, posterior_a, alpha=0.5, color='steelblue', label='Design A')
        ax.fill_between(theta, posterior_b, alpha=0.5, color='orange', label='Design B')
        ax.set_xlabel(r'Conversion Rate ($\theta$)')
        ax.set_ylabel('Density')
        ax.set_title('Posterior Distributions')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        
        # Right: difference distribution
        ax = fig.add_subplot(1, 2, 2)
        
        # Sample from posteriors and compute difference
        np.random.seed(42)
        samples_a = np.random.beta(a_conversions + 1, a_trials - a_conversions + 1, 10000)
        samples_b = np.random.beta(b_conversions + 1, b_trials - b_conversions + 1, 10000)
        
        difference = samples_b - samples_a
        
        ax.hist(difference, bins=50, density=True, alpha=0.7, color='purple', edgecolor='black')
        ax.axvline(0, color='black', linestyle='--', linewidth=2, label='No difference')
        
        # Probability B is better
        prob_b_better = np.mean(samples_b > samples_a)
        
        ax.set_xlabel(r'Difference in Conversion Rate ($\theta_B - \theta_A$)')
        ax.set_ylabel('Density')
        ax.set_title(f'Posterior Difference\n$P(\\theta_B > \\theta_A) = {prob_b_better:.3f}$')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()

def main():
    """Generate all Chapter 16 figures."""
    print("Generating Chapter 16 figures...")
    
    try:
        print("Generating Figure 16.1")
        generate_figure_16_1()
        print("✓ Saved figure: .../16.1.png")
        
        print("Generating Figure 16.2")
        generate_figure_16_2()
        print("✓ Saved figure: .../16.2.png")
        
        print("Generating Figure 16.3")
        generate_figure_16_3()
        print("✓ Saved figure: .../16.3.png")
        
        print("Generating Figure 16.4")
        generate_figure_16_4()
        print("✓ Saved figure: .../16.4.png")
        
        print("✓ All figures generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
