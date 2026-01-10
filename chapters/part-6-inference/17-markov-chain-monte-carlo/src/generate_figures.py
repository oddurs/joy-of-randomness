"""
Figure generation for Chapter 17: Markov Chain Monte Carlo

Generates publication-quality figures demonstrating MCMC algorithms,
convergence diagnostics, and multimodal challenges.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
matplotlib.rcParams['mathtext.fontset'] = 'stix'
import matplotlib.pyplot as plt
from scipy.stats import norm
from pathlib import Path
import sys

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

np.random.seed(42)

OUTPUT_DIR = Path(__file__).parent / 'figures'
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================================
# Helper Functions for MCMC Simulation
# ============================================================================

def metropolis_hastings(target_density, proposal_std, n_iter):
    """Run Metropolis-Hastings algorithm."""
    chain = np.zeros(n_iter)
    current = np.random.normal(0, 1)
    accepted = 0
    
    for i in range(n_iter):
        # Propose
        proposed = current + np.random.normal(0, proposal_std)
        
        # Acceptance ratio
        ratio = target_density(proposed) / target_density(current)
        alpha = min(1, ratio)
        
        # Accept/reject
        if np.random.uniform() < alpha:
            current = proposed
            accepted += 1
        
        chain[i] = current
    
    acceptance_rate = accepted / n_iter
    return chain, acceptance_rate

# ============================================================================
# Figure 17.1: Metropolis-Hastings Convergence
# ============================================================================

# Target: mixture of two Gaussians
def mixture_density(x):
    return 0.4 * norm.pdf(x, -3, 1) + 0.6 * norm.pdf(x, 2, 1.2)

def generate_figure_17_1():
    """Figure 17.1: Metropolis-Hastings: Convergence to Target Distribution"""
    
    # Run with moderate proposal
    n_iter = 5000
    n_burn = 500
    chain, acc_rate = metropolis_hastings(mixture_density, 1.5, n_iter)
    
    with figure(6, 17, 1, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Metropolis-Hastings: Convergence to Target Distribution', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Trace plot with burn-in
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(chain[:1000], alpha=0.7, linewidth=0.8)
        ax1.axvline(n_burn, color='red', linestyle='--', label='Burn-in end')
        ax1.fill_between(range(n_burn), -5, 5, alpha=0.2, color='red')
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Parameter')
        ax1.set_title('Trace Plot (Early iterations)')
        ax1.set_ylim(-5, 5)
        ax1.legend()
        
        # Plot 2: Full trace plot
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(chain, alpha=0.4, linewidth=0.5)
        ax2.axvline(n_burn, color='red', linestyle='--', label='Burn-in')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Parameter')
        ax2.set_title(f'Full Trace (acceptance rate: {acc_rate:.1%})')
        ax2.legend()
        
        # Plot 3: Histogram of samples vs target
        ax3 = plt.subplot(2, 2, 3)
        samples = chain[n_burn:]
        ax3.hist(samples, bins=50, density=True, alpha=0.6, label='MCMC samples')
        x = np.linspace(-6, 6, 200)
        ax3.plot(x, mixture_density(x), 'r-', linewidth=2, label='Target density')
        ax3.set_xlabel('Parameter')
        ax3.set_ylabel('Density')
        ax3.set_title('Distribution Match')
        ax3.legend()
        
        # Plot 4: Autocorrelation
        ax4 = plt.subplot(2, 2, 4)
        lags = np.arange(0, 100)
        acf = []
        for lag in lags:
            if lag == 0:
                acf.append(1.0)
            else:
                acf.append(np.corrcoef(samples[:-lag], samples[lag:])[0, 1])
        ax4.bar(lags, acf, alpha=0.7)
        ax4.axhline(0, color='black', linewidth=0.5)
        ax4.set_xlabel('Lag')
        ax4.set_ylabel('Autocorrelation')
        ax4.set_title('Sample Autocorrelation')
        
        plt.tight_layout()

def generate_figure_17_2():
    """Figure 17.2: Proposal Distribution Tuning"""
    
    def run_mcmc(proposal_std, n_iter=3000):
        """Run MCMC with given proposal std."""
        chain, acc_rate = metropolis_hastings(mixture_density, proposal_std, n_iter)
        return chain[500:], acc_rate
    
    proposals = [0.3, 1.0, 2.5, 5.0]
    proposal_labels = ['Too narrow\n(SD=0.3)', 'Goldilocks\n(SD=1.0)', 
                       'Too wide\n(SD=2.5)', 'Way too wide\n(SD=5.0)']
    colors = ['#e74c3c', '#27ae60', '#27ae60', '#e74c3c']
    
    with figure(6, 17, 2, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Proposal Distribution: The Sweet Spot', 
                     fontsize=14, fontweight='bold')
        
        for idx, (prop_std, label, color) in enumerate(zip(proposals, proposal_labels, colors)):
            samples, acc_rate = run_mcmc(prop_std)
            
            ax = plt.subplot(2, 2, idx + 1)
            ax.hist(samples, bins=40, density=True, alpha=0.6, 
                   color=color, edgecolor='black')
            x = np.linspace(-6, 6, 200)
            ax.plot(x, mixture_density(x), 'k-', linewidth=1.5, alpha=0.7)
            ax.set_xlabel('Parameter')
            ax.set_ylabel('Density')
            ax.set_title(f'{label}\nAccept rate: {acc_rate:.1%}')
            ax.set_ylim(0, 0.4)
        
        plt.tight_layout()

def generate_figure_17_3():
    """Figure 17.3: Convergence Diagnostics"""
    
    # Run 4 independent chains
    n_chains = 4
    n_iter = 2000
    chains_list = []
    starting_points = [-4, 0, 3, 5]
    
    for start in starting_points:
        chain = np.zeros(n_iter)
        current = start
        
        for i in range(n_iter):
            proposed = current + np.random.normal(0, 1.5)
            ratio = mixture_density(proposed) / mixture_density(current)
            if np.random.uniform() < min(1, ratio):
                current = proposed
            chain[i] = current
        
        chains_list.append(chain)
    
    with figure(6, 17, 3, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Convergence Diagnostics: Multiple Chains', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Trace of all chains
        ax1 = plt.subplot(2, 2, 1)
        for i, chain in enumerate(chains_list):
            ax1.plot(chain, alpha=0.7, linewidth=1, label=f'Chain {i+1}')
        ax1.axvline(500, color='red', linestyle='--', linewidth=1, alpha=0.7)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Parameter')
        ax1.set_title('All Chains: Trace Plots')
        ax1.legend(fontsize=8)
        
        # Plot 2: R-hat diagnostic
        ax2 = plt.subplot(2, 2, 2)
        burn_in = 500
        windows = range(burn_in, n_iter, 100)
        r_hats = []
        
        for w in windows:
            within_chain_var = np.mean([np.var(chain[:w]) for chain in chains_list])
            between_chain_var = np.var([np.mean(chain[:w]) for chain in chains_list])
            r_hat = np.sqrt((1 - 2/w) + (n_chains + 1)/n_chains * 
                           between_chain_var / (within_chain_var + 1e-10) + 1e-6)
            r_hats.append(r_hat)
        
        ax2.plot(list(windows), r_hats, 'o-', linewidth=2, markersize=4)
        ax2.axhline(1.1, color='green', linestyle='--', linewidth=1, 
                   label='Good convergence')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('R-hat')
        ax2.set_title('Gelman-Rubin Diagnostic')
        ax2.set_ylim(0.95, max(r_hats) + 0.1)
        ax2.legend()
        
        # Plot 3: Posterior overlays
        ax3 = plt.subplot(2, 2, 3)
        for i, chain in enumerate(chains_list):
            samples = chain[burn_in:]
            ax3.hist(samples, bins=30, alpha=0.5, density=True, label=f'Chain {i+1}')
        x = np.linspace(-6, 6, 200)
        ax3.plot(x, mixture_density(x), 'k-', linewidth=2, label='Target')
        ax3.set_xlabel('Parameter')
        ax3.set_ylabel('Density')
        ax3.set_title('Posterior Distributions Match')
        ax3.legend(fontsize=8)
        
        # Plot 4: Effective sample size
        ax4 = plt.subplot(2, 2, 4)
        n_samples = n_iter - burn_in
        ess_list = []
        
        for chain in chains_list:
            samples = chain[burn_in:]
            acf_vals = []
            for lag in range(1, 50):
                if lag < len(samples):
                    acf_vals.append(np.corrcoef(samples[:-lag], samples[lag:])[0, 1])
            tau = 1 + 2 * np.sum(acf_vals)
            ess = n_samples / tau
            ess_list.append(ess)
        
        colors_chains = plt.cm.Set2(np.linspace(0, 1, n_chains))
        ax4.bar(range(n_chains), ess_list, color=colors_chains, edgecolor='black')
        ax4.axhline(n_samples, color='red', linestyle='--', linewidth=1, label='Total samples')
        ax4.set_ylabel('Effective Sample Size')
        ax4.set_xlabel('Chain')
        ax4.set_title('Effective Sample Size (autocorrelation adjusted)')
        ax4.set_xticks(range(n_chains))
        ax4.set_xticklabels([f'C{i+1}' for i in range(n_chains)])
        ax4.legend()
        
        plt.tight_layout()

def generate_figure_17_4():
    """Figure 17.4: Multimodal Challenge"""
    
    # Target: two well-separated Gaussians
    def bimodal_density(x):
        return 0.5 * norm.pdf(x, -5, 0.8) + 0.5 * norm.pdf(x, 5, 0.8)
    
    n_iter = 5000
    
    # Narrow proposal: explores one mode well
    chain_narrow = np.zeros(n_iter)
    current = -5
    for i in range(n_iter):
        proposed = current + np.random.normal(0, 0.5)
        if np.random.uniform() < min(1, bimodal_density(proposed) / bimodal_density(current)):
            current = proposed
        chain_narrow[i] = current
    
    # Wide proposal: can jump between modes
    chain_wide = np.zeros(n_iter)
    current = -5
    for i in range(n_iter):
        proposed = current + np.random.normal(0, 3)
        if np.random.uniform() < min(1, bimodal_density(proposed) / bimodal_density(current)):
            current = proposed
        chain_wide[i] = current
    
    with figure(6, 17, 4, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Multimodal Challenge: Chain Gets Stuck', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Narrow proposal trace
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(chain_narrow[:1500], linewidth=0.8, alpha=0.8)
        ax1.axhline(-5, color='green', linewidth=2, alpha=0.3, label='Mode 1')
        ax1.axhline(5, color='orange', linewidth=2, alpha=0.3, label='Mode 2')
        ax1.set_ylabel('Parameter')
        ax1.set_xlabel('Iteration')
        ax1.set_title('Narrow Proposal (SD=0.5): Stuck in One Mode')
        ax1.set_ylim(-8, 8)
        ax1.legend()
        
        # Plot 2: Wide proposal trace
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(chain_wide[:1500], linewidth=0.8, alpha=0.8, color='purple')
        ax2.axhline(-5, color='green', linewidth=2, alpha=0.3, label='Mode 1')
        ax2.axhline(5, color='orange', linewidth=2, alpha=0.3, label='Mode 2')
        ax2.set_ylabel('Parameter')
        ax2.set_xlabel('Iteration')
        ax2.set_title('Wide Proposal (SD=3): Jumps Between Modes')
        ax2.set_ylim(-8, 8)
        ax2.legend()
        
        # Plot 3: Histogram comparison
        ax3 = plt.subplot(2, 2, 3)
        ax3.hist(chain_narrow[500:], bins=50, alpha=0.5, density=True, 
                label='Narrow proposal', color='blue')
        x = np.linspace(-8, 8, 200)
        ax3.plot(x, bimodal_density(x), 'k-', linewidth=2, 
                label='Target (both modes)')
        ax3.set_xlabel('Parameter')
        ax3.set_ylabel('Density')
        ax3.set_title('Narrow: Misses One Mode')
        ax3.legend()
        
        # Plot 4: Wide histogram
        ax4 = plt.subplot(2, 2, 4)
        ax4.hist(chain_wide[500:], bins=50, alpha=0.5, density=True, 
                label='Wide proposal', color='purple')
        ax4.plot(x, bimodal_density(x), 'k-', linewidth=2, 
                label='Target (both modes)')
        ax4.set_xlabel('Parameter')
        ax4.set_ylabel('Density')
        ax4.set_title('Wide: Captures Both Modes')
        ax4.legend()
        
        plt.tight_layout()

if __name__ == '__main__':
    print('Generating Chapter 17 figures...')
    
    print('Generating Figure 17.1')
    generate_figure_17_1()
    print('✓ Saved figure: figures/17.1.png')
    
    print('Generating Figure 17.2')
    generate_figure_17_2()
    print('✓ Saved figure: figures/17.2.png')
    
    print('Generating Figure 17.3')
    generate_figure_17_3()
    print('✓ Saved figure: figures/17.3.png')
    
    print('Generating Figure 17.4')
    generate_figure_17_4()
    print('✓ Saved figure: figures/17.4.png')
    
    print('✓ All figures generated successfully!')
