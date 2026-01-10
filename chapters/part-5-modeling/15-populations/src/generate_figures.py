"""Generate figures for Chapter 15: Populations."""

import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

def birth_death_process(n0, lambda_birth, mu_death, t_max=100, seed=None):
    """Simulate birth-death process.
    
    lambda_birth: probability per individual per time step
    mu_death: probability per individual per time step
    """
    if seed is not None:
        np.random.seed(seed)
    
    # If rates > 1, rescale them to probabilities
    if lambda_birth > 1:
        lambda_birth = min(lambda_birth / 10, 0.99)  # Cap at 0.99
    if mu_death > 1:
        mu_death = min(mu_death / 10, 0.99)
    
    n = int(n0)
    history = [n]
    
    for t in range(t_max):
        if n <= 0:
            history.extend([0] * (t_max - t))
            break
        
        # Cap n to prevent overflow in binomial
        n_safe = int(min(n, 100000))
        
        # Births and deaths for each individual
        births = np.random.binomial(n_safe, lambda_birth)
        deaths = np.random.binomial(n_safe, mu_death)
        
        # If n > 100000, use expectation
        if n > 100000:
            births = int(n * lambda_birth)
            deaths = int(n * mu_death)
        
        n = max(0, n + births - deaths)
        history.append(n)
    
    return np.array(history)

def generate_figure_15_1():
    """Figure 15.1: Population trajectories with different starting sizes."""
    with figure(5, 15, 1, output_dir=OUTPUT_DIR) as fig:
        lambda_rate = 0.6
        mu_rate = 0.4
        t_max = 100
        
        # Four starting population sizes
        starting_sizes = [1, 5, 10, 50]
        
        for idx, n0 in enumerate(starting_sizes):
            ax = fig.add_subplot(2, 2, idx + 1)
            
            np.random.seed(42)
            num_runs = 30
            
            for run in range(num_runs):
                traj = birth_death_process(n0, lambda_rate, mu_rate, t_max, seed=42+run)
                ax.plot(traj, alpha=0.3, linewidth=0.8, color='steelblue')
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Population Size')
            ax.set_title(f'$n_0 = {n0}$')
            ax.grid(alpha=0.3)
            ax.set_ylim([0, 200])
        
        plt.tight_layout()

def generate_figure_15_2():
    """Figure 15.2: Extinction probability vs initial population size."""
    with figure(5, 15, 2, output_dir=OUTPUT_DIR) as fig:
        ax = fig.add_subplot(111)
        
        lambda_rate = 1.2
        mu_rate = 1.0
        ratio = mu_rate / lambda_rate
        
        # Vary initial population size
        n0_vals = np.arange(1, 21)
        extinction_probs_sim = []
        extinction_probs_theory = []
        
        np.random.seed(42)
        
        for n0 in n0_vals:
            # Simulate
            num_sims = 100
            extinctions = 0
            
            for _ in range(num_sims):
                traj = birth_death_process(n0, lambda_rate, mu_rate, t_max=300)
                if traj[-1] == 0:
                    extinctions += 1
            
            extinction_probs_sim.append(extinctions / num_sims)
            
            # Theoretical: p = (mu/lambda)^n0
            extinction_probs_theory.append(ratio ** n0)
        
        ax.semilogy(n0_vals, extinction_probs_sim, 'o-', color='steelblue', 
                   markersize=6, linewidth=2, label='Simulated')
        ax.semilogy(n0_vals, extinction_probs_theory, '--', color='red', 
                   linewidth=2, label=r'Theory: $\left(\frac{\mu}{\lambda}\right)^{n_0}$')
        
        ax.set_xlabel(r'Initial Population Size $n_0$')
        ax.set_ylabel('Extinction Probability')
        ax.set_title(r'Extinction Probability vs Initial Size ($\lambda=1.2, \mu=1.0$)')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3, which='both')
        
        plt.tight_layout()

def generate_figure_15_3():
    """Figure 15.3: Effect of variance on extinction risk."""
    with figure(5, 15, 3, output_dir=OUTPUT_DIR) as fig:
        # Two scenarios with same mean growth but different variance
        scenarios = [
            ('Low Variance', 0.55, 0.45),  # growth = 0.1
            ('High Variance', 0.8, 0.7),   # growth = 0.1
        ]
        
        for idx, (name, lambda_rate, mu_rate) in enumerate(scenarios):
            ax = fig.add_subplot(1, 2, idx + 1)
            
            np.random.seed(42)
            n0 = 10
            num_runs = 30
            
            for run in range(num_runs):
                traj = birth_death_process(n0, lambda_rate, mu_rate, t_max=150, seed=42+run)
                ax.plot(traj, alpha=0.3, linewidth=0.8, color='steelblue')
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Population Size')
            ax.set_title(name + rf'$\lambda={lambda_rate}, \mu={mu_rate}$')
            ax.grid(alpha=0.3)
            ax.set_ylim([0, 300])
        
        plt.tight_layout()

def generate_figure_15_4():
    """Figure 15.4: Distribution of final population sizes (survivors)."""
    with figure(5, 15, 4, output_dir=OUTPUT_DIR) as fig:
        lambda_rate = 1.2
        mu_rate = 1.0
        n0 = 5
        
        np.random.seed(42)
        num_sims = 500
        final_sizes = []
        survivor_sizes = []
        
        for _ in range(num_sims):
            traj = birth_death_process(n0, lambda_rate, mu_rate, t_max=200)
            final = traj[-1]
            final_sizes.append(final)
            
            if final > 0:
                survivor_sizes.append(final)
        
        # Left: all outcomes
        ax = fig.add_subplot(1, 2, 1)
        extinction_count = np.sum(np.array(final_sizes) == 0)
        counts = np.bincount(final_sizes, minlength=max(final_sizes)+1 if final_sizes else 0)
        
        ax.bar(range(min(100, len(counts))), counts[:100], color='steelblue', alpha=0.7)
        ax.set_xlabel('Final Population Size')
        ax.set_ylabel('Number of Simulations')
        ax.set_title(f'All Outcomes\n({extinction_count} extinctions, {len(survivor_sizes)} survivors)')
        ax.grid(alpha=0.3, axis='y')
        
        # Right: survivors only
        ax = fig.add_subplot(1, 2, 2)
        if survivor_sizes:
            ax.hist(survivor_sizes, bins=30, color='orange', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Final Population Size')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Survivors Only\n(Mean = {np.mean(survivor_sizes):.1f})')
            ax.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()

def main():
    """Generate all Chapter 15 figures."""
    print("Generating Chapter 15 figures...")
    
    try:
        print("Generating Figure 15.1")
        generate_figure_15_1()
        print("✓ Saved figure: .../15.1.png")
        
        print("Generating Figure 15.2")
        generate_figure_15_2()
        print("✓ Saved figure: .../15.2.png")
        
        print("Generating Figure 15.3")
        generate_figure_15_3()
        print("✓ Saved figure: .../15.3.png")
        
        print("Generating Figure 15.4")
        generate_figure_15_4()
        print("✓ Saved figure: .../15.4.png")
        
        print("✓ All figures generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
