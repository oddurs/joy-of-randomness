"""
Chapter 18: Fitting Models to Messy Data
Complete Bayesian workflow: model specification, MCMC inference, diagnosis, and interpretation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t as tdist


# ============================================================================
# Synthetic Data Generation
# ============================================================================

def generate_recovery_data(n=50, beta0=8, beta1=0.3, sigma=2.5, seed=42):
    """
    Generate synthetic recovery time data.
    
    Args:
        n: number of patients
        beta0: intercept
        beta1: slope (effect of age)
        sigma: noise std dev
        seed: random seed
    
    Returns:
        age, recovery_time
    """
    np.random.seed(seed)
    age = np.random.uniform(30, 80, n)
    recovery = beta0 + beta1 * age + np.random.normal(0, sigma, n)
    return age, recovery


def generate_changepoint_data(n=100, mu1=10, mu2=5, changepoint=40, sigma=2, seed=42):
    """
    Generate data with a change point.
    
    Args:
        n: number of observations
        mu1: mean before change point
        mu2: mean after change point
        changepoint: day of change
        sigma: noise std dev
        seed: random seed
    
    Returns:
        data: observations
        true_changepoint: true changepoint location
    """
    np.random.seed(seed)
    data = np.zeros(n)
    
    # Before change point
    data[:changepoint] = mu1 + np.random.normal(0, sigma, changepoint)
    
    # After change point
    data[changepoint:] = mu2 + np.random.normal(0, sigma, n - changepoint)
    
    return data, changepoint


def generate_hierarchical_data(n_groups=5, n_per_group=20, global_mean=10, group_sigma=2, within_sigma=1.5, seed=42):
    """
    Generate hierarchical data (multiple groups sharing information).
    
    Args:
        n_groups: number of groups
        n_per_group: observations per group
        global_mean: global mean
        group_sigma: std dev of group means
        within_sigma: std dev within groups
        seed: random seed
    
    Returns:
        data: hierarchical observations
        true_group_means: true mean of each group
    """
    np.random.seed(seed)
    
    true_group_means = global_mean + np.random.normal(0, group_sigma, n_groups)
    data = []
    
    for j in range(n_groups):
        group_data = true_group_means[j] + np.random.normal(0, within_sigma, n_per_group)
        data.append(group_data)
    
    return np.array(data), true_group_means


# ============================================================================
# Linear Regression Model
# ============================================================================

def log_posterior_linear_regression(theta, x, y):
    """
    Log posterior for linear regression.
    
    Model: y = beta0 + beta1 * x + noise
    
    Args:
        theta: [beta0, beta1, log_sigma]
        x, y: observed data
    
    Returns:
        log posterior (up to constant)
    """
    beta0, beta1, log_sigma = theta
    sigma = np.exp(log_sigma)
    
    # Likelihood
    mu = beta0 + beta1 * x
    log_lik = -0.5 * np.sum(((y - mu) / sigma)**2) - len(y) * log_sigma
    
    # Weakly informative priors
    log_prior = (
        -0.5 * (beta0 / 10)**2 +  # N(0, 10)
        -0.5 * (beta1 / 10)**2 +  # N(0, 10)
        log_sigma  # Exponential(1)
    )
    
    return log_lik + log_prior


# ============================================================================
# Change Point Model
# ============================================================================

def log_posterior_changepoint(theta, data):
    """
    Log posterior for change point model.
    
    Model: mean is mu1 before changepoint, mu2 after.
    
    Args:
        theta: [mu1, mu2, log_sigma, changepoint] (changepoint is integer)
        data: observed time series
    
    Returns:
        log posterior
    """
    mu1, mu2, log_sigma = theta[:3]
    changepoint = int(round(theta[3]))
    sigma = np.exp(log_sigma)
    
    # Ensure changepoint is in valid range
    changepoint = np.clip(changepoint, 0, len(data) - 1)
    
    # Likelihood
    before = data[:changepoint]
    after = data[changepoint:]
    
    log_lik = -0.5 * np.sum((before - mu1)**2) / sigma**2 - 0.5 * np.sum((after - mu2)**2) / sigma**2
    log_lik -= len(data) * log_sigma
    
    # Priors
    log_prior = (
        -0.5 * (mu1 / 10)**2 +
        -0.5 * (mu2 / 10)**2 +
        log_sigma
    )
    
    return log_lik + log_prior


# ============================================================================
# Hierarchical Model
# ============================================================================

def log_posterior_hierarchical(theta, data):
    """
    Log posterior for hierarchical model.
    
    Model: each group has mean ~ N(global_mean, group_var)
    
    Args:
        theta: [global_mean, log_group_sigma, log_within_sigma]
        data: hierarchical data (list of group arrays)
    
    Returns:
        log posterior
    """
    global_mean, log_group_sigma, log_within_sigma = theta
    group_sigma = np.exp(log_group_sigma)
    within_sigma = np.exp(log_within_sigma)
    
    log_lik = 0
    
    # For each group, integrate over the group mean
    for group_data in data:
        # Group sample mean and size
        n = len(group_data)
        sample_mean = np.mean(group_data)
        sample_var = np.var(group_data, ddof=1) if n > 1 else 0
        
        # Likelihood of group data
        # Marginalizing over group mean (closed form for normal model)
        tau2 = group_sigma**2
        sigma2 = within_sigma**2
        
        # Posterior variance of group mean given global mean
        post_var = 1 / (n / sigma2 + 1 / tau2)
        post_mean = post_var * (n * sample_mean / sigma2 + global_mean / tau2)
        
        # Log marginal likelihood
        log_marginal = -0.5 * np.sum((group_data - post_mean)**2) / sigma2
        log_marginal -= 0.5 * len(data) * n * np.log(sigma2)
        
        log_lik += log_marginal
    
    # Priors
    log_prior = (
        -0.5 * (global_mean / 10)**2 +
        log_group_sigma +
        log_within_sigma
    )
    
    return log_lik + log_prior


# ============================================================================
# Posterior Predictive Checks
# ============================================================================

def posterior_predictive_regression(samples_post_burnin, x):
    """
    Generate posterior predictive samples for new x values.
    
    Args:
        samples_post_burnin: posterior MCMC samples (n_samples, 3)
        x: new x values
    
    Returns:
        predictions: (n_samples, len(x)) predictive samples
    """
    n_samples = samples_post_burnin.shape[0]
    predictions = np.zeros((n_samples, len(x)))
    
    for i in range(n_samples):
        beta0, beta1, log_sigma = samples_post_burnin[i]
        sigma = np.exp(log_sigma)
        mu = beta0 + beta1 * x
        predictions[i] = mu + np.random.normal(0, sigma, len(x))
    
    return predictions


def posterior_predictive_summary(predictions):
    """
    Summarize posterior predictive distribution.
    
    Args:
        predictions: (n_samples, n_points) array
    
    Returns:
        mean, lower_ci, upper_ci
    """
    mean = np.mean(predictions, axis=0)
    lower_ci = np.percentile(predictions, 2.5, axis=0)
    upper_ci = np.percentile(predictions, 97.5, axis=0)
    
    return mean, lower_ci, upper_ci


# ============================================================================
# Visualization
# ============================================================================

def plot_regression_fit(x, y, samples_post_burnin):
    """
    Plot regression with posterior predictive interval.
    
    Args:
        x, y: observed data
        samples_post_burnin: posterior MCMC samples
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Observed data
    ax.scatter(x, y, alpha=0.6, s=50, label='Observed data')
    
    # Posterior predictive
    x_pred = np.linspace(x.min() - 5, x.max() + 5, 100)
    predictions = posterior_predictive_regression(samples_post_burnin, x_pred)
    mean_pred, lower_pred, upper_pred = posterior_predictive_summary(predictions)
    
    ax.plot(x_pred, mean_pred, 'r-', linewidth=2, label='Posterior mean')
    ax.fill_between(x_pred, lower_pred, upper_pred, alpha=0.3, label='95% predictive interval')
    
    ax.set_xlabel('Age')
    ax.set_ylabel('Recovery time')
    ax.set_title('Linear Regression with Posterior Predictive Interval')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_changepoint_posterior(data, samples_changepoint):
    """
    Plot inferred change point distribution.
    
    Args:
        data: time series
        samples_changepoint: posterior samples of changepoint (discrete)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Time series
    ax1.plot(data, 'k-', alpha=0.6, linewidth=1)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Observation')
    ax1.set_title('Time Series')
    ax1.grid(True, alpha=0.3)
    
    # Posterior of changepoint
    ax2.hist(samples_changepoint, bins=range(0, len(data) + 1), density=True, 
            edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Change point day')
    ax2.set_ylabel('Probability')
    ax2.set_title('Posterior Distribution of Change Point')
    ax2.grid(True, alpha=0.3, axis='y')
    
    return fig


def plot_hierarchical_comparison(group_means_obs, true_means, hierarchical_means):
    """
    Plot hierarchical vs. naive estimates.
    
    Args:
        group_means_obs: observed group sample means
        true_means: true group means
        hierarchical_means: hierarchical posterior means
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(group_means_obs))
    
    ax.scatter(x - 0.15, group_means_obs, s=100, alpha=0.7, label='Observed (sample mean)', marker='s')
    ax.scatter(x, hierarchical_means, s=100, alpha=0.7, label='Hierarchical (posterior)', marker='o')
    ax.scatter(x + 0.15, true_means, s=100, alpha=0.7, label='True', marker='^')
    
    ax.set_xlabel('Group')
    ax.set_ylabel('Mean')
    ax.set_title('Hierarchical Model: Partial Pooling')
    ax.set_xticks(x)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig


# ============================================================================
# Demo / Main
# ============================================================================

if __name__ == '__main__':
    print("Chapter 18: Fitting Models to Messy Data")
    print("=" * 60)
    
    # Example 1: Linear regression
    print("\n--- Example 1: Linear Regression ---")
    
    x, y = generate_recovery_data(n=30)
    
    print(f"Data: {len(x)} observations")
    print(f"Age range: {x.min():.1f} - {x.max():.1f} years")
    print(f"Recovery range: {y.min():.1f} - {y.max():.1f} days")
    print(f"Correlation (age, recovery): {np.corrcoef(x, y)[0, 1]:.3f}")
    
    # Simple OLS for comparison
    coeffs = np.polyfit(x, y, 1)
    print(f"\nOLS estimates: intercept={coeffs[1]:.3f}, slope={coeffs[0]:.3f}")
    
    # Example 2: Change point
    print("\n--- Example 2: Change Point Detection ---")
    
    data, true_cp = generate_changepoint_data(n=100)
    
    print(f"Data: {len(data)} observations")
    print(f"True change point: day {true_cp}")
    print(f"Mean before: {data[:true_cp].mean():.2f}")
    print(f"Mean after: {data[true_cp:].mean():.2f}")
    
    # Example 3: Hierarchical
    print("\n--- Example 3: Hierarchical Model ---")
    
    data_hier, true_means = generate_hierarchical_data(n_groups=5, n_per_group=15)
    
    print(f"Data: {len(data_hier)} groups, {len(data_hier[0])} per group")
    print(f"Observed group means: {[f'{m:.2f}' for m in data_hier.mean(axis=1)]}")
    print(f"True group means: {[f'{m:.2f}' for m in true_means]}")
    
    print("\nDone!")
