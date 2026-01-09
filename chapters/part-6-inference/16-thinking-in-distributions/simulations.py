"""
Chapter 16: Thinking in Distributions
Bayesian inference: updating beliefs from data as probability distributions.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import beta, comb
from scipy.stats import binom, beta as beta_dist


# ============================================================================
# Beta-Binomial Conjugacy
# ============================================================================

def binomial_likelihood(k, n, theta):
    """
    Likelihood of observing k successes in n trials with probability theta.
    
    Args:
        k: number of successes
        n: number of trials
        theta: probability of success (array)
    
    Returns:
        Likelihood for each theta value
    """
    return comb(n, k, exact=True) * (theta ** k) * ((1 - theta) ** (n - k))


def beta_prior(theta, alpha, beta_param):
    """
    Beta distribution prior.
    
    Args:
        theta: parameter value (array)
        alpha, beta_param: shape parameters
    
    Returns:
        Prior density for each theta value
    """
    return (theta ** (alpha - 1)) * ((1 - theta) ** (beta_param - 1)) / beta(alpha, beta_param)


def beta_posterior(k, n, alpha, beta_param):
    """
    Posterior distribution (conjugate).
    
    Args:
        k: observed successes
        n: observed trials
        alpha, beta_param: prior shape parameters
    
    Returns:
        Posterior Beta distribution parameters
    """
    alpha_post = alpha + k
    beta_post = beta_param + (n - k)
    return alpha_post, beta_post


def posterior_density(theta, k, n, alpha, beta_param):
    """Posterior density (unnormalized version)."""
    likelihood = binomial_likelihood(k, n, theta)
    prior = beta_prior(theta, alpha, beta_param)
    return likelihood * prior


# ============================================================================
# Credible Intervals
# ============================================================================

def credible_interval(alpha, beta_param, credible_level=0.95):
    """
    Compute credible interval for Beta distribution.
    
    Args:
        alpha, beta_param: Beta distribution parameters
        credible_level: credibility level (e.g., 0.95 for 95%)
    
    Returns:
        lower, upper bounds of credible interval
    """
    lower = beta_dist.ppf((1 - credible_level) / 2, alpha, beta_param)
    upper = beta_dist.ppf(1 - (1 - credible_level) / 2, alpha, beta_param)
    return lower, upper


def posterior_mean(alpha, beta_param):
    """Mean of Beta distribution."""
    return alpha / (alpha + beta_param)


def posterior_median(alpha, beta_param):
    """Median of Beta distribution."""
    return beta_dist.median(alpha, beta_param)


def posterior_mode(alpha, beta_param):
    """Mode of Beta distribution."""
    if alpha > 1 and beta_param > 1:
        return (alpha - 1) / (alpha + beta_param - 2)
    else:
        return np.nan


# ============================================================================
# Sequential Bayesian Updating
# ============================================================================

def sequential_bayesian_update(observations, alpha=1, beta_param=1):
    """
    Update posterior sequentially as observations arrive.
    
    Args:
        observations: array of 0s and 1s (failures and successes)
        alpha, beta_param: prior parameters
    
    Returns:
        List of (alpha, beta) at each step
    """
    posteriors = [(alpha, beta_param)]
    alpha_curr = alpha
    beta_curr = beta_param
    
    for obs in observations:
        if obs == 1:
            alpha_curr += 1
        else:
            beta_curr += 1
        posteriors.append((alpha_curr, beta_curr))
    
    return posteriors


# ============================================================================
# Multiple Priors
# ============================================================================

def compare_priors(k, n, priors_dict):
    """
    Compare posteriors under different priors.
    
    Args:
        k: observed successes
        n: observed trials
        priors_dict: dict of {name: (alpha, beta)} prior parameters
    
    Returns:
        dict of {name: (alpha_post, beta_post)} posterior parameters
    """
    posteriors = {}
    for name, (alpha, beta_param) in priors_dict.items():
        alpha_post, beta_post = beta_posterior(k, n, alpha, beta_param)
        posteriors[name] = (alpha_post, beta_post)
    return posteriors


# ============================================================================
# Bayesian A/B Testing
# ============================================================================

def ab_test_comparison(n_a, k_a, n_b, k_b, n_samples=10000):
    """
    Bayesian A/B test: compare two conversion rates.
    
    Args:
        n_a, k_a: trials and successes for variant A
        n_b, k_b: trials and successes for variant B
        n_samples: number of posterior samples
    
    Returns:
        p_b_better: P(θ_B > θ_A)
        mean_diff: posterior mean difference
        credible_interval: credible interval on difference
    """
    # Posteriors (Beta(1,1) priors)
    alpha_a, beta_a = beta_posterior(k_a, n_a, 1, 1)
    alpha_b, beta_b = beta_posterior(k_b, n_b, 1, 1)
    
    # Sample from posteriors
    samples_a = np.random.beta(alpha_a, beta_a, n_samples)
    samples_b = np.random.beta(alpha_b, beta_b, n_samples)
    
    # P(θ_B > θ_A)
    p_b_better = np.mean(samples_b > samples_a)
    
    # Difference
    diffs = samples_b - samples_a
    mean_diff = np.mean(diffs)
    ci_lower = np.percentile(diffs, 2.5)
    ci_upper = np.percentile(diffs, 97.5)
    
    return p_b_better, mean_diff, (ci_lower, ci_upper)


def medical_diagnosis(sensitivity=0.95, specificity=0.95, prevalence=0.01):
    """
    Bayesian update for medical diagnosis.
    
    P(disease | positive) = P(positive | disease) * P(disease) / P(positive)
    
    Args:
        sensitivity: P(positive | disease)
        specificity: P(negative | no disease) = 1 - P(positive | no disease)
        prevalence: P(disease) prior
    
    Returns:
        P(disease | positive)
    """
    # P(positive | disease)
    p_pos_given_disease = sensitivity
    
    # P(positive | no disease)
    p_pos_given_no_disease = 1 - specificity
    
    # P(positive) using law of total probability
    p_positive = (p_pos_given_disease * prevalence + 
                  p_pos_given_no_disease * (1 - prevalence))
    
    # Bayes' theorem
    p_disease_given_positive = (p_pos_given_disease * prevalence) / p_positive
    
    return p_disease_given_positive


# ============================================================================
# Visualization
# ============================================================================

def plot_beta_prior_posterior(k, n, alpha, beta_param, ax=None):
    """Plot prior, likelihood, and posterior."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    theta = np.linspace(0, 1, 1000)
    
    # Prior
    prior = beta_prior(theta, alpha, beta_param)
    
    # Likelihood
    likelihood = binomial_likelihood(k, n, theta)
    likelihood = likelihood / np.max(likelihood)  # Normalize for visualization
    
    # Posterior
    alpha_post, beta_post = beta_posterior(k, n, alpha, beta_param)
    posterior = beta_prior(theta, alpha_post, beta_post)
    
    # Plot
    ax.plot(theta, prior, 'b-', linewidth=2, label=f'Prior: Beta({alpha}, {beta_param})')
    ax.plot(theta, likelihood, 'g--', linewidth=2, label=f'Likelihood (rescaled): {k}/{n} successes')
    ax.plot(theta, posterior, 'r-', linewidth=2, label=f'Posterior: Beta({alpha_post}, {beta_post})')
    
    ax.set_xlabel('θ (probability of success)')
    ax.set_ylabel('Density')
    ax.set_title(f'Bayesian Update: Prior × Likelihood → Posterior')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


def plot_multiple_posteriors(k, n, priors_dict):
    """Compare posteriors under different priors."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    theta = np.linspace(0, 1, 1000)
    
    posteriors = compare_priors(k, n, priors_dict)
    colors = plt.cm.tab10(np.linspace(0, 1, len(posteriors)))
    
    for (name, (alpha_post, beta_post)), color in zip(posteriors.items(), colors):
        post_density = beta_prior(theta, alpha_post, beta_post)
        ax.plot(theta, post_density, linewidth=2, label=name, color=color)
    
    ax.set_xlabel('θ (probability of success)')
    ax.set_ylabel('Posterior Density')
    ax.set_title(f'Effect of Prior on Posterior (data: {k}/{n})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_sequential_updating(observations, priors_dict):
    """Visualize sequential Bayesian updating."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    theta = np.linspace(0, 1, 1000)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(observations) + 1))
    
    # Plot sequential updates for each prior
    for idx, (name, (alpha, beta_param)) in enumerate(priors_dict.items()):
        if idx >= 4:
            break
        
        ax = axes[idx]
        
        # Posterior at each step
        alpha_curr = alpha
        beta_curr = beta_param
        
        # Initial prior
        prior_density = beta_prior(theta, alpha_curr, beta_curr)
        ax.plot(theta, prior_density, linewidth=2, label='Prior', color=colors[0])
        
        # Update sequentially
        for step, obs in enumerate(observations):
            if obs == 1:
                alpha_curr += 1
            else:
                beta_curr += 1
            
            if step % 5 == 4:  # Plot every 5 observations
                post_density = beta_prior(theta, alpha_curr, beta_curr)
                ax.plot(theta, post_density, linewidth=1.5, 
                       label=f'After {step+1} obs', color=colors[step // 5 + 1])
        
        # Final posterior
        post_density = beta_prior(theta, alpha_curr, beta_curr)
        ax.plot(theta, post_density, linewidth=2.5, label=f'Final ({alpha_curr}, {beta_curr})', 
               color='red')
        
        ax.set_xlabel('θ')
        ax.set_ylabel('Density')
        ax.set_title(f'{name}: Prior Beta({alpha}, {beta_param})')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_credible_intervals(k, n, priors_dict, credible_level=0.95):
    """Plot credible intervals under different priors."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    posteriors = compare_priors(k, n, priors_dict)
    names = list(posteriors.keys())
    
    means = []
    intervals = []
    
    for name, (alpha_post, beta_post) in posteriors.items():
        mean = posterior_mean(alpha_post, beta_post)
        lower, upper = credible_interval(alpha_post, beta_post, credible_level)
        means.append(mean)
        intervals.append((lower, upper))
    
    # Plot
    for i, (name, (lower, upper), mean) in enumerate(zip(names, intervals, means)):
        ax.barh(i, upper - lower, left=lower, height=0.3, alpha=0.6, label=name)
        ax.plot(mean, i, 'ro', markersize=8)
    
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel('θ (probability of success)')
    ax.set_title(f'{credible_level*100:.0f}% Credible Intervals\n(red dot = posterior mean, {k}/{n} observed)')
    ax.grid(True, alpha=0.3, axis='x')
    
    return fig


def plot_ab_test(n_a, k_a, n_b, k_b):
    """Visualize A/B test results."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Posteriors
    alpha_a, beta_a = beta_posterior(k_a, n_a, 1, 1)
    alpha_b, beta_b = beta_posterior(k_b, n_b, 1, 1)
    
    theta = np.linspace(0, 1, 1000)
    
    # Plot posteriors
    ax = axes[0]
    ax.plot(theta, beta_prior(theta, alpha_a, beta_a), 'b-', linewidth=2, label='Variant A')
    ax.plot(theta, beta_prior(theta, alpha_b, beta_b), 'r-', linewidth=2, label='Variant B')
    ax.set_xlabel('Conversion Rate')
    ax.set_ylabel('Density')
    ax.set_title('Posterior Distributions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Samples from posteriors
    n_samples = 10000
    samples_a = np.random.beta(alpha_a, beta_a, n_samples)
    samples_b = np.random.beta(alpha_b, beta_b, n_samples)
    
    # Plot difference distribution
    ax = axes[1]
    diffs = samples_b - samples_a
    ax.hist(diffs, bins=50, density=True, alpha=0.6, edgecolor='black')
    ax.axvline(0, color='k', linestyle='--', linewidth=2)
    ax.set_xlabel('Difference (B - A)')
    ax.set_ylabel('Density')
    ax.set_title('Posterior Difference')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Probability that B is better
    ax = axes[2]
    p_b_better = np.mean(samples_b > samples_a)
    ax.bar(['B Better', 'A Better'], [p_b_better, 1 - p_b_better], 
           color=['green', 'red'], alpha=0.7, edgecolor='black')
    ax.set_ylabel('Probability')
    ax.set_title(f'P(B > A) = {p_b_better:.1%}')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_medical_diagnosis(sensitivity=0.95, specificity=0.95):
    """Visualize medical diagnosis updating."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Vary prevalence
    prevalences = np.linspace(0.001, 0.1, 50)
    posteriors = []
    
    for prev in prevalences:
        p_disease_given_pos = medical_diagnosis(sensitivity, specificity, prev)
        posteriors.append(p_disease_given_pos)
    
    # Plot
    ax = axes[0]
    ax.plot(prevalences * 100, np.array(posteriors) * 100, linewidth=2)
    ax.fill_between(prevalences * 100, 0, np.array(posteriors) * 100, alpha=0.3)
    ax.set_xlabel('Disease Prevalence (%)')
    ax.set_ylabel('P(Disease | Positive Test) (%)')
    ax.set_title(f'Medical Test (Sensitivity={sensitivity*100:.0f}%, Specificity={specificity*100:.0f}%)')
    ax.grid(True, alpha=0.3)
    
    # Vary test accuracy
    accuracies = np.linspace(0.5, 1.0, 50)
    posteriors = []
    prev = 0.01
    
    for acc in accuracies:
        p_disease_given_pos = medical_diagnosis(acc, acc, prev)
        posteriors.append(p_disease_given_pos)
    
    ax = axes[1]
    ax.plot(accuracies * 100, np.array(posteriors) * 100, linewidth=2)
    ax.fill_between(accuracies * 100, 0, np.array(posteriors) * 100, alpha=0.3)
    ax.set_xlabel('Test Accuracy (%)')
    ax.set_ylabel('P(Disease | Positive Test) (%)')
    ax.set_title(f'Effect of Test Accuracy (Prevalence={prev*100:.1f}%)')
    ax.grid(True, alpha=0.3)
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 16: Thinking in Distributions")
    print("=" * 60)
    
    # Example: Coin flip
    k = 7
    n = 10
    alpha = 1
    beta_param = 1
    
    print(f"\nBeta-Binomial Model")
    print(f"  Data: {k} heads in {n} flips")
    print(f"  Prior: Beta({alpha}, {beta_param}) (uniform)")
    
    # Posterior
    alpha_post, beta_post = beta_posterior(k, n, alpha, beta_param)
    print(f"  Posterior: Beta({alpha_post}, {beta_post})")
    
    # Point estimates
    mean = posterior_mean(alpha_post, beta_post)
    median = posterior_median(alpha_post, beta_post)
    mode = posterior_mode(alpha_post, beta_post)
    
    print(f"\nPoint Estimates:")
    print(f"  Mean: {mean:.3f}")
    print(f"  Median: {median:.3f}")
    print(f"  Mode: {mode:.3f}")
    
    # Credible interval
    ci_lower, ci_upper = credible_interval(alpha_post, beta_post, 0.95)
    print(f"\n95% Credible Interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
    
    # Multiple priors
    print(f"\n--- Effect of Different Priors ---")
    priors = {
        'Uniform': (1, 1),
        'Skeptical (fair)': (10, 10),
        'Biased toward tails': (0.5, 0.5)
    }
    
    posteriors = compare_priors(k, n, priors)
    for name, (a_post, b_post) in posteriors.items():
        mean_post = posterior_mean(a_post, b_post)
        print(f"  {name}: mean = {mean_post:.3f}")
    
    # Medical diagnosis
    print(f"\n--- Medical Diagnosis ---")
    p_disease = medical_diagnosis(0.95, 0.95, 0.01)
    print(f"  P(disease | positive test) = {p_disease:.1%}")
    print(f"  (Despite high test accuracy, prior is very low)")
    
    print("\nDone!")
