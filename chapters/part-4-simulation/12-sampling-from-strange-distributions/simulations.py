"""
Chapter 12: Sampling from Strange Distributions
Inverse transform sampling, rejection sampling, and their limits in high dimensions.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, gamma, binom


# ============================================================================
# Inverse Transform Sampling
# ============================================================================

def inverse_transform_exponential(n_samples, lam=1.0):
    """
    Generate exponential samples using inverse transform.
    
    X = -ln(U) / λ where U ~ Uniform(0, 1)
    
    Args:
        n_samples: Number of samples
        lam: Rate parameter λ
    
    Returns:
        Array of exponential samples
    """
    u = np.random.uniform(0, 1, n_samples)
    x = -np.log(u) / lam
    return x


def inverse_transform_weibull(n_samples, shape=1.0, scale=1.0):
    """
    Generate Weibull samples using inverse transform.
    
    X = scale * (-ln(U))^(1/shape)
    
    Args:
        n_samples: Number of samples
        shape: Shape parameter k
        scale: Scale parameter λ
    
    Returns:
        Array of Weibull samples
    """
    u = np.random.uniform(0, 1, n_samples)
    x = scale * (-np.log(u)) ** (1 / shape)
    return x


def inverse_transform_pareto(n_samples, min_val=1.0, alpha=1.0):
    """
    Generate Pareto samples using inverse transform.
    
    X = min_val * U^(-1/alpha)
    
    Args:
        n_samples: Number of samples
        min_val: Minimum value (location)
        alpha: Shape parameter
    
    Returns:
        Array of Pareto samples
    """
    u = np.random.uniform(0, 1, n_samples)
    x = min_val * u ** (-1 / alpha)
    return x


# ============================================================================
# Rejection Sampling
# ============================================================================

def rejection_sampling_normal_exp_proposal(n_samples, seed=None):
    """
    Sample from standard normal using rejection sampling with exponential proposal.
    
    Proposal: g(x) = exp(-|x|) (exponential)
    Envelope: M = sqrt(2/π) ≈ 0.798
    
    Args:
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility
    
    Returns:
        Tuple of (samples, acceptance_rate, n_proposals)
    """
    if seed is not None:
        np.random.seed(seed)
    
    samples = []
    n_proposals = 0
    
    while len(samples) < n_samples:
        # Sample from exponential
        x = np.random.exponential(1.0)
        
        # Randomly assign sign
        if np.random.rand() < 0.5:
            x = -x
        
        # Evaluate densities
        f_x = norm.pdf(x)
        g_x = expon.pdf(np.abs(x))
        M = np.sqrt(2 / np.pi)
        
        # Rejection test
        u = np.random.rand()
        if u <= f_x / (M * g_x):
            samples.append(x)
        
        n_proposals += 1
    
    acceptance_rate = n_samples / n_proposals
    return np.array(samples), acceptance_rate, n_proposals


def rejection_sampling_normal_uniform_proposal(n_samples, seed=None):
    """
    Sample from standard normal using rejection sampling with uniform proposal.
    
    Proposal: g(x) uniform on [-4, 4]
    Envelope: M = norm.pdf(0) * 8 / 1 ≈ 3.19
    
    Args:
        n_samples: Number of samples
        seed: Random seed
    
    Returns:
        Tuple of (samples, acceptance_rate, n_proposals)
    """
    if seed is not None:
        np.random.seed(seed)
    
    samples = []
    n_proposals = 0
    bound = 4.0
    
    while len(samples) < n_samples:
        # Sample uniformly from [-bound, bound]
        x = np.random.uniform(-bound, bound)
        
        # Evaluate densities
        f_x = norm.pdf(x)
        g_x = 1.0 / (2 * bound)  # Uniform density
        M = norm.pdf(0) * (2 * bound)  # Envelope
        
        # Rejection test
        u = np.random.rand()
        if u <= f_x / (M * g_x):
            samples.append(x)
        
        n_proposals += 1
    
    acceptance_rate = n_samples / n_proposals
    return np.array(samples), acceptance_rate, n_proposals


def rejection_sampling_normal_student_proposal(n_samples, df=1, seed=None):
    """
    Sample from standard normal using rejection sampling with Student's t proposal.
    
    Student's t has heavier tails than normal, useful as envelope.
    
    Args:
        n_samples: Number of samples
        df: Degrees of freedom for Student's t
        seed: Random seed
    
    Returns:
        Tuple of (samples, acceptance_rate, n_proposals)
    """
    if seed is not None:
        np.random.seed(seed)
    
    samples = []
    n_proposals = 0
    
    # Find M by numerical search
    x_test = np.linspace(-5, 5, 1000)
    f_test = norm.pdf(x_test)
    g_test = norm.pdf(x_test, scale=np.sqrt(df / (df - 2)))  # Approximate
    
    M = np.max(f_test / np.maximum(g_test, 1e-10))
    
    while len(samples) < n_samples:
        # Sample from Student's t
        x = np.random.standard_t(df)
        
        # Evaluate densities
        from scipy.stats import t
        f_x = norm.pdf(x)
        g_x = t.pdf(x, df)
        
        # Rejection test
        u = np.random.rand()
        if u <= f_x / (M * g_x):
            samples.append(x)
        
        n_proposals += 1
    
    acceptance_rate = n_samples / n_proposals
    return np.array(samples), acceptance_rate, n_proposals


# ============================================================================
# Rejection Sampling in High Dimensions
# ============================================================================

def rejection_sampling_normal_multivariate(d, n_samples=1000, seed=None):
    """
    Try rejection sampling for d-dimensional standard normal using uniform proposal.
    
    Args:
        d: Dimension
        n_samples: Number of samples
        seed: Random seed
    
    Returns:
        Tuple of (samples, acceptance_rate, n_proposals, avg_ratio)
    """
    if seed is not None:
        np.random.seed(seed)
    
    samples = []
    n_proposals = 0
    ratios = []
    
    # Use [-3, 3]^d as proposal domain
    bound = 3.0
    volume = (2 * bound) ** d
    
    max_proposals = n_samples * 10000  # Limit proposals to avoid infinite loops
    
    while len(samples) < n_samples and n_proposals < max_proposals:
        # Sample uniformly from [-bound, bound]^d
        x = np.random.uniform(-bound, bound, d)
        
        # Evaluate log-densities (to avoid underflow)
        log_f = -0.5 * np.sum(x ** 2) - 0.5 * d * np.log(2 * np.pi)
        log_g = -d * np.log(2 * bound)  # Uniform density
        
        # Compute ratio f/g (in log space, then exponentiate)
        log_ratio = log_f - log_g
        ratio = np.exp(log_ratio)
        ratios.append(ratio)
        
        # Rejection test (work in log space for stability)
        u = np.random.rand()
        if np.log(u) <= log_ratio - np.log(1.0):  # Rough envelope
            samples.append(x)
        
        n_proposals += 1
    
    acceptance_rate = len(samples) / n_proposals if n_proposals > 0 else 0
    avg_ratio = np.mean(ratios) if ratios else 0
    
    return (np.array(samples) if samples else np.array([]).reshape(0, d), 
            acceptance_rate, n_proposals, avg_ratio)


# ============================================================================
# Box-Muller Transform
# ============================================================================

def box_muller(n_samples):
    """
    Generate normal samples using Box-Muller transform.
    
    Generates pairs of independent normals from pairs of uniforms.
    
    Args:
        n_samples: Number of samples (will generate even number)
    
    Returns:
        Array of normal samples
    """
    # Ensure even number of samples
    n_pairs = (n_samples + 1) // 2
    
    u1 = np.random.uniform(0, 1, n_pairs)
    u2 = np.random.uniform(0, 1, n_pairs)
    
    r = np.sqrt(-2 * np.log(u1))
    theta = 2 * np.pi * u2
    
    z1 = r * np.cos(theta)
    z2 = r * np.sin(theta)
    
    samples = np.concatenate([z1, z2])
    return samples[:n_samples]


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_inverse_transform_exponential():
    """Plot inverse transform sampling for exponential."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Generate samples
    samples = inverse_transform_exponential(10000, lam=2.0)
    
    # Histogram
    ax = axes[0]
    ax.hist(samples, bins=50, density=True, alpha=0.7, label='Generated samples')
    
    # Overlay theoretical PDF
    x = np.linspace(0, np.max(samples), 100)
    ax.plot(x, expon.pdf(x, scale=0.5), 'r-', linewidth=2, label='Theory (λ=2)')
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    ax.set_title('Inverse Transform: Exponential(λ=2)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Q-Q plot
    ax = axes[1]
    theoretical = np.sort(expon.rvs(scale=0.5, size=10000))
    empirical = np.sort(samples)
    ax.scatter(theoretical, empirical, alpha=0.5, s=1)
    ax.plot([theoretical.min(), theoretical.max()], 
            [theoretical.min(), theoretical.max()], 'r--', linewidth=2)
    ax.set_xlabel('Theoretical Quantiles')
    ax.set_ylabel('Empirical Quantiles')
    ax.set_title('Q-Q Plot: Inverse Transform Exponential')
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_rejection_sampling_normal():
    """Plot rejection sampling for normal with different proposals."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Exponential proposal
    samples_exp, acc_exp, n_prop_exp = rejection_sampling_normal_exp_proposal(5000)
    ax = axes[0, 0]
    ax.hist(samples_exp, bins=50, density=True, alpha=0.7, label='Rejection samples')
    x = np.linspace(-4, 4, 100)
    ax.plot(x, norm.pdf(x), 'r-', linewidth=2, label='N(0,1)')
    ax.set_title(f'Exponential Proposal\nAcceptance Rate: {acc_exp:.1%}')
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Uniform proposal
    samples_unif, acc_unif, n_prop_unif = rejection_sampling_normal_uniform_proposal(5000)
    ax = axes[0, 1]
    ax.hist(samples_unif, bins=50, density=True, alpha=0.7, label='Rejection samples')
    ax.plot(x, norm.pdf(x), 'r-', linewidth=2, label='N(0,1)')
    ax.set_title(f'Uniform Proposal\nAcceptance Rate: {acc_unif:.1%}')
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Box-Muller
    samples_bm = box_muller(5000)
    ax = axes[1, 0]
    ax.hist(samples_bm, bins=50, density=True, alpha=0.7, label='Box-Muller')
    ax.plot(x, norm.pdf(x), 'r-', linewidth=2, label='N(0,1)')
    ax.set_title('Box-Muller Transform\n(Exact, no rejection)')
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Comparison
    ax = axes[1, 1]
    methods = ['Exponential\nProposal', 'Uniform\nProposal', 'Box-Muller']
    acceptance_rates = [acc_exp, acc_unif, 1.0]
    colors = ['blue', 'orange', 'green']
    ax.bar(methods, acceptance_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_ylabel('Acceptance Rate')
    ax.set_title('Sampling Efficiency Comparison')
    ax.set_ylim([0, 1.1])
    for i, rate in enumerate(acceptance_rates):
        ax.text(i, rate + 0.02, f'{rate:.1%}', ha='center', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_rejection_sampling_high_dimensional():
    """Plot rejection sampling acceptance rate degradation in high dimensions."""
    dimensions = [1, 2, 3, 5, 7, 10, 15, 20]
    acceptance_rates = []
    
    for d in dimensions:
        samples, acc_rate, n_prop, avg_ratio = rejection_sampling_normal_multivariate(d, n_samples=100)
        acceptance_rates.append(acc_rate)
        print(f"d = {d:>2}: acceptance rate = {acc_rate:.2e}, avg f/g = {avg_ratio:.2e}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Linear scale
    ax1.semilogy(dimensions, acceptance_rates, 'ro-', linewidth=2, markersize=8)
    ax1.set_xlabel('Dimension d')
    ax1.set_ylabel('Acceptance Rate')
    ax1.set_title('Rejection Sampling in High Dimensions')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_ylim(ymin=1e-5)
    
    # Compare to theoretical exponential decay
    ax2.semilogy(dimensions, acceptance_rates, 'ro-', linewidth=2, markersize=8, label='Empirical')
    
    # Fit exponential decay: a * exp(-b*d)
    valid_indices = [i for i, rate in enumerate(acceptance_rates) if rate > 0]
    if len(valid_indices) > 1:
        from scipy.optimize import curve_fit
        
        def decay(d, a, b):
            return a * np.exp(-b * d)
        
        try:
            popt, _ = curve_fit(decay, 
                               np.array(dimensions)[valid_indices], 
                               np.array(acceptance_rates)[valid_indices],
                               p0=[1, 0.1])
            d_theory = np.linspace(dimensions[0], dimensions[-1], 100)
            ax2.plot(d_theory, decay(d_theory, *popt), 'b--', linewidth=2, label=f'Fit: {popt[0]:.2f} exp(-{popt[1]:.2f}d)')
        except:
            pass
    
    ax2.set_xlabel('Dimension d')
    ax2.set_ylabel('Acceptance Rate (log scale)')
    ax2.set_title('Exponential Decay of Acceptance Rate')
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend()
    ax2.set_ylim(ymin=1e-5)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 12: Sampling from Strange Distributions")
    print("=" * 60)
    
    # Inverse transform
    print("\n--- Inverse Transform Sampling (Exponential) ---")
    samples = inverse_transform_exponential(10000, lam=2.0)
    print(f"Sample mean: {np.mean(samples):.3f} (theory: {0.5:.3f})")
    print(f"Sample std:  {np.std(samples):.3f} (theory: {0.5:.3f})")
    
    # Rejection sampling comparison
    print("\n--- Rejection Sampling for Normal ---")
    
    samples_exp, acc_exp, n_prop_exp = rejection_sampling_normal_exp_proposal(1000)
    print(f"Exponential proposal: acceptance rate = {acc_exp:.1%} ({n_prop_exp} proposals for 1000 samples)")
    print(f"  Sample mean: {np.mean(samples_exp):.3f} (theory: 0)")
    print(f"  Sample std:  {np.std(samples_exp):.3f} (theory: 1)")
    
    samples_unif, acc_unif, n_prop_unif = rejection_sampling_normal_uniform_proposal(1000)
    print(f"Uniform proposal: acceptance rate = {acc_unif:.1%} ({n_prop_unif} proposals for 1000 samples)")
    print(f"  Sample mean: {np.mean(samples_unif):.3f} (theory: 0)")
    print(f"  Sample std:  {np.std(samples_unif):.3f} (theory: 1)")
    
    samples_bm = box_muller(1000)
    print(f"Box-Muller: acceptance rate = 100% (exact method, no rejection)")
    print(f"  Sample mean: {np.mean(samples_bm):.3f} (theory: 0)")
    print(f"  Sample std:  {np.std(samples_bm):.3f} (theory: 1)")
    
    # High-dimensional rejection sampling
    print("\n--- Rejection Sampling in High Dimensions ---")
    print("Dim | Acceptance Rate | Proposals per Sample")
    print("-" * 45)
    
    for d in [1, 2, 3, 5, 10, 15, 20]:
        samples_hd, acc_rate, n_prop, avg_ratio = rejection_sampling_normal_multivariate(d, n_samples=100)
        ppd = n_prop / 100 if acc_rate > 0 else np.inf
        print(f"{d:>3} | {acc_rate:>15.2e} | {ppd:>19.1f}")
    
    print("\nNote: acceptance rate collapses exponentially with dimension!")
    print("This is why simple rejection sampling fails in high-D Bayesian inference.")
    
    print("\nDone!")
