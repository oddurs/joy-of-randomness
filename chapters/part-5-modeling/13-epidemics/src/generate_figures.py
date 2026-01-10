#!/usr/bin/env python3
"""Generate figures for Chapter 13: Epidemics."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
from pathlib import Path

# Disable LaTeX rendering to avoid special character issues
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.default'] = 'regular'

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

def deterministic_sir(y, t, N, beta, gamma):
    """SIR differential equations."""
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

def stochastic_sir_step(S, I, R, N, beta, gamma, dt=1.0):
    """One step of stochastic SIR (continuous-time Markov chain)."""
    # Transmissions
    transmission_rate = beta * S * I / N
    new_infections = np.random.poisson(transmission_rate * dt)
    new_infections = min(new_infections, S)
    
    S -= new_infections
    I += new_infections
    
    # Recoveries
    recovery_rate = gamma * I
    new_recoveries = np.random.poisson(recovery_rate * dt)
    new_recoveries = min(new_recoveries, I)
    
    I -= new_recoveries
    R += new_recoveries
    
    return S, I, R

def generate_figure_13_1():
    """Figure 13.1: Deterministic vs Stochastic SIR."""
    with figure(5, 13, 1, output_dir=OUTPUT_DIR) as fig:
        # Parameters
        N = 10000
        beta = 0.5
        gamma = 0.1
        R0 = beta / gamma
        
        t_days = 100
        t_span = np.linspace(0, t_days, 500)
        
        # Deterministic solution
        y0 = [N - 1, 1, 0]
        sol = odeint(deterministic_sir, y0, t_span, args=(N, beta, gamma))
        S_det, I_det, R_det = sol.T
        
        # Stochastic realizations (multiple runs)
        np.random.seed(42)
        num_runs = 20
        stoch_solutions = []
        for _ in range(num_runs):
            S, I, R = N - 1, 1, 0
            I_hist = [I]
            
            for day in range(t_days):
                S, I, R = stochastic_sir_step(S, I, R, N, beta, gamma, dt=1.0)
                I_hist.append(I)
            
            stoch_solutions.append(np.array(I_hist))
        
        # Plot
        ax = fig.add_subplot(111)
        
        # Stochastic realizations in light gray
        t_days_array = np.arange(len(stoch_solutions[0]))
        for sol in stoch_solutions:
            ax.plot(t_days_array, sol, color='gray', alpha=0.3, linewidth=0.8)
        
        # Deterministic solution in bold
        ax.plot(t_span, I_det, color='red', linewidth=2.5, label='Deterministic SIR')
        
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number Infected (I)')
        ax.set_title(f'Deterministic vs Stochastic SIR (N={N}, R0={R0:.1f})')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()

def generate_figure_13_2():
    """Figure 13.2: Extinction Probability vs R0."""
    with figure(5, 13, 2, output_dir=OUTPUT_DIR) as fig:
        # Range of R0 values
        R0_vals = np.linspace(0.5, 3.0, 20)
        extinction_probs = []
        
        # For each R0, run many stochastic simulations
        N = 5000
        gamma = 0.1
        num_simulations = 100
        
        np.random.seed(42)
        for R0 in R0_vals:
            beta = R0 * gamma
            extinct_count = 0
            
            for _ in range(num_simulations):
                S, I, R = N - 1, 1, 0
                
                # Run until extinction or 500 days
                for _ in range(500):
                    if I == 0:
                        extinct_count += 1
                        break
                    S, I, R = stochastic_sir_step(S, I, R, N, beta, gamma, dt=1.0)
            
            extinction_probs.append(extinct_count / num_simulations)
        
        # Theoretical extinction probability for R0 > 1
        extinction_theory = []
        for R0 in R0_vals:
            if R0 <= 1.0:
                extinction_theory.append(1.0)
            else:
                # For branching process: extinction probability approximately = 1/R0
                extinction_theory.append(1.0 / R0)
        
        # Plot
        ax = fig.add_subplot(111)
        ax.plot(R0_vals, extinction_probs, 'o-', color='steelblue', linewidth=2, 
                markersize=6, label='Simulated')
        ax.plot(R0_vals, extinction_theory, '--', color='red', linewidth=2, 
                label='Theory (1/R0)')
        ax.axvline(x=1.0, color='black', linestyle=':', alpha=0.5, linewidth=1.5)
        ax.text(1.05, 0.9, 'R0=1', fontsize=9, color='black')
        
        ax.set_xlabel('Basic Reproduction Number (R0)')
        ax.set_ylabel('Extinction Probability')
        ax.set_title('Stochastic Extinction: Randomness Prevents Epidemics')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plt.tight_layout()

def generate_figure_13_3():
    """Figure 13.3: Major Outbreak Probability vs R0 and Population Size."""
    with figure(5, 13, 3, output_dir=OUTPUT_DIR) as fig:
        # Parameters
        gamma = 0.1
        outbreak_threshold = 0.1  # Major outbreak if > 10% infected
        
        # Two population sizes
        populations = [1000, 10000]
        num_simulations = 100
        
        R0_vals = np.linspace(0.5, 3.0, 15)
        results = {pop: [] for pop in populations}
        
        np.random.seed(42)
        for pop in populations:
            for R0 in R0_vals:
                beta = R0 * gamma
                major_outbreaks = 0
                
                for _ in range(num_simulations):
                    S, I, R = pop - 1, 1, 0
                    final_R = 0
                    
                    # Run until no infections
                    for _ in range(1000):
                        if I == 0:
                            final_R = R
                            break
                        S, I, R = stochastic_sir_step(S, I, R, pop, beta, gamma, dt=1.0)
                    
                    if final_R / pop >= outbreak_threshold:
                        major_outbreaks += 1
                
                results[pop].append(major_outbreaks / num_simulations)
        
        # Plot
        ax = fig.add_subplot(111)
        for pop in populations:
            ax.plot(R0_vals, results[pop], 'o-', linewidth=2, markersize=6, 
                    label=f'N={pop}')
        
        ax.axvline(x=1.0, color='black', linestyle=':', alpha=0.5, linewidth=1.5)
        ax.text(1.05, 0.85, 'R0=1', fontsize=9, color='black')
        
        ax.set_xlabel('Basic Reproduction Number (R0)')
        ax.set_ylabel('Probability of Major Outbreak (>10%)')
        ax.set_title('Outbreak Probability: Population Size and R0')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plt.tight_layout()

def generate_figure_13_4():
    """Figure 13.4: Impact of Superspreaders."""
    with figure(5, 13, 4, output_dir=OUTPUT_DIR) as fig:
        # Create 2x2 subplots
        axes = [fig.add_subplot(2, 2, i+1) for i in range(4)]
        
        N = 5000
        gamma = 0.1
        R0 = 2.0
        beta = R0 * gamma
        
        np.random.seed(42)
        
        # Scenario 1: Homogeneous transmission
        # Scenario 2: Superspreaders (10% cause 80% of transmission)
        
        scenarios = [
            ('Homogeneous', lambda I, b, n: np.random.poisson(b * n / n * I)),
            ('10% Superspreaders', lambda I, b, n: np.random.poisson(b * n / n * I * 1.8))
        ]
        
        num_runs = 15
        
        for ax_idx, (scenario_name, trans_func) in enumerate(scenarios):
            ax = axes[ax_idx]
            
            for run in range(num_runs):
                S, I, R = N - 1, 1, 0
                I_hist = [I]
                
                for day in range(200):
                    if I == 0:
                        break
                    
                    new_infections = trans_func(I, beta, N)
                    new_infections = min(new_infections, S)
                    S -= new_infections
                    I += new_infections
                    
                    recoveries = np.random.poisson(gamma * I)
                    recoveries = min(recoveries, I)
                    I -= recoveries
                    R += recoveries
                    
                    I_hist.append(I)
                
                color = 'steelblue' if scenario_name == 'Homogeneous' else 'orange'
                ax.plot(I_hist, color=color, alpha=0.5, linewidth=1)
            
            ax.set_title(scenario_name)
            ax.set_xlabel('Days')
            ax.set_ylabel('Number Infected (I)')
            ax.grid(alpha=0.3)
        
        # Right column: Extinction probability comparison
        ax = axes[2]
        scenarios_names = ['Homogeneous', 'Superspreaders']
        ext_probs = []
        num_sims = 100
        
        for scenario_idx, (scenario_name, trans_func) in enumerate(scenarios):
            extinct = 0
            for _ in range(num_sims):
                S, I, R = N - 1, 1, 0
                for _ in range(500):
                    if I == 0:
                        extinct += 1
                        break
                    new_infections = trans_func(I, beta, N)
                    new_infections = min(new_infections, S)
                    S -= new_infections
                    I += new_infections
                    
                    recoveries = np.random.poisson(gamma * I)
                    recoveries = min(recoveries, I)
                    I -= recoveries
                    R += recoveries
            
            ext_probs.append(extinct / num_sims)
        
        colors = ['steelblue', 'orange']
        ax.bar(scenarios_names, ext_probs, color=colors, alpha=0.7)
        ax.set_ylabel('Extinction Probability')
        ax.set_title(f'Extinction Risk (R0={R0})')
        ax.set_ylim([0, 1])
        ax.grid(alpha=0.3, axis='y')
        
        # Mean outbreak size comparison
        ax = axes[3]
        outbreak_sizes = []
        
        for scenario_idx, (scenario_name, trans_func) in enumerate(scenarios):
            sizes = []
            for _ in range(num_sims):
                S, I, R = N - 1, 1, 0
                for _ in range(1000):
                    if I == 0:
                        sizes.append(R)
                        break
                    new_infections = trans_func(I, beta, N)
                    new_infections = min(new_infections, S)
                    S -= new_infections
                    I += new_infections
                    
                    recoveries = np.random.poisson(gamma * I)
                    recoveries = min(recoveries, I)
                    I -= recoveries
                    R += recoveries
            
            outbreak_sizes.append(np.mean(sizes))
        
        ax.bar(scenarios_names, outbreak_sizes, color=colors, alpha=0.7)
        ax.set_ylabel('Mean Final Size (R)')
        ax.set_title('Average Outbreak Size')
        ax.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()

def main():
    """Generate all Chapter 13 figures."""
    print("Generating Chapter 13 figures...")
    
    try:
        print("Generating Figure 13.1")
        generate_figure_13_1()
        print("✓ Saved figure: .../13.1.png")
        
        print("Generating Figure 13.2")
        generate_figure_13_2()
        print("✓ Saved figure: .../13.2.png")
        
        print("Generating Figure 13.3")
        generate_figure_13_3()
        print("✓ Saved figure: .../13.3.png")
        
        print("Generating Figure 13.4")
        generate_figure_13_4()
        print("✓ Saved figure: .../13.4.png")
        
        print("✓ All figures generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    main()
