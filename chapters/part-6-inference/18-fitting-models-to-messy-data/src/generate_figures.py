"""Generate figures for Chapter 18: Fitting Models to Messy Data."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'
matplotlib.rcParams['font.family'] = 'sans-serif'
import matplotlib.pyplot as plt
from scipy.stats import norm, t
from scipy.optimize import minimize
from pathlib import Path
import sys

# Add shared module to path
chapter_dir = Path(__file__).parent.parent
repo_root = chapter_dir.parent.parent.parent
sys.path.insert(0, str(repo_root))

from shared.figures import figure

np.random.seed(42)

OUTPUT_DIR = Path(__file__).parent / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================================
# Figure 18.1: Linear Regression with Uncertainty
# ============================================================================

def generate_figure_18_1():
    """Figure 18.1: Bayesian linear regression with posterior uncertainty."""
    
    # Generate synthetic recovery time data
    np.random.seed(42)
    n_patients = 10
    ages = np.array([25, 35, 45, 30, 50, 40, 55, 32, 48, 42])
    recovery_times = np.array([12, 15, 18, 14, 22, 16, 25, 13, 20, 17])
    
    # Fit simple linear regression
    X = np.vstack([np.ones(len(ages)), ages]).T
    params = np.linalg.lstsq(X, recovery_times, rcond=None)[0]
    intercept, slope = params
    predictions = intercept + slope * ages
    residuals = recovery_times - predictions
    sigma = np.std(residuals)
    
    # Simulate posterior samples via simple bootstrap
    n_samples = 2000
    posterior_intercepts = []
    posterior_slopes = []
    posterior_sigmas = []
    
    for _ in range(n_samples):
        idx = np.random.choice(len(ages), len(ages), replace=True)
        X_boot = np.vstack([np.ones(len(ages)), ages[idx]]).T
        y_boot = recovery_times[idx]
        try:
            params_boot = np.linalg.lstsq(X_boot, y_boot, rcond=None)[0]
            posterior_intercepts.append(params_boot[0])
            posterior_slopes.append(params_boot[1])
            sigma_boot = np.std(y_boot - (params_boot[0] + params_boot[1] * ages[idx]))
            posterior_sigmas.append(sigma_boot)
        except:
            posterior_intercepts.append(intercept)
            posterior_slopes.append(slope)
            posterior_sigmas.append(sigma)
    
    posterior_intercepts = np.array(posterior_intercepts)
    posterior_slopes = np.array(posterior_slopes)
    
    with figure(6, 18, 1, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Bayesian Linear Regression: Recovery Time vs Age', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Regression with uncertainty bands
        ax1 = plt.subplot(2, 2, 1)
        ax1_age_range = np.linspace(ages.min() - 5, ages.max() + 5, 100)
        
        # Plot posterior predictive samples
        for i in range(0, n_samples, 20):
            pred = posterior_intercepts[i] + posterior_slopes[i] * ax1_age_range
            ax1.plot(ax1_age_range, pred, alpha=0.01, color='blue')
        
        # Plot observed data
        ax1.scatter(ages, recovery_times, s=60, color='red', zorder=5, label='Observed')
        
        # Plot fitted line
        fitted_line = intercept + slope * ax1_age_range
        ax1.plot(ax1_age_range, fitted_line, 'r-', linewidth=2, label='Mean fit')
        ax1.set_xlabel('Age (years)')
        ax1.set_ylabel('Recovery time (days)')
        ax1.set_title('Fitted Line with Posterior Samples')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Plot 2: Posterior distribution of slope
        ax2 = plt.subplot(2, 2, 2)
        ax2.hist(posterior_slopes, bins=40, density=True, alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(posterior_slopes), color='red', linestyle='--', linewidth=2, label='Mean')
        ax2.axvline(np.percentile(posterior_slopes, 2.5), color='green', linestyle=':', linewidth=2, label='95% CI')
        ax2.axvline(np.percentile(posterior_slopes, 97.5), color='green', linestyle=':', linewidth=2)
        ax2.set_xlabel('Slope (days/year)')
        ax2.set_ylabel('Density')
        ax2.set_title('Posterior: Age Effect on Recovery')
        ax2.legend(fontsize=8)
        
        # Plot 3: Posterior distribution of intercept
        ax3 = plt.subplot(2, 2, 3)
        ax3.hist(posterior_intercepts, bins=40, density=True, alpha=0.7, edgecolor='black')
        ax3.axvline(np.mean(posterior_intercepts), color='red', linestyle='--', linewidth=2, label='Mean')
        ax3.axvline(np.percentile(posterior_intercepts, 2.5), color='green', linestyle=':', linewidth=2)
        ax3.axvline(np.percentile(posterior_intercepts, 97.5), color='green', linestyle=':', linewidth=2)
        ax3.set_xlabel('Intercept (days)')
        ax3.set_ylabel('Density')
        ax3.set_title('Posterior: Baseline Recovery Time')
        ax3.legend(fontsize=8)
        
        # Plot 4: Residuals
        ax4 = plt.subplot(2, 2, 4)
        ax4.scatter(predictions, residuals, s=50, alpha=0.6)
        ax4.axhline(0, color='red', linestyle='--', linewidth=2)
        ax4.fill_between(ax4.get_xlim(), -2*sigma, 2*sigma, alpha=0.2, color='green', label='±2SD')
        ax4.set_xlabel('Fitted values (days)')
        ax4.set_ylabel('Residuals (days)')
        ax4.set_title('Residual Plot')
        ax4.legend()
        ax4.grid(alpha=0.3)

# ============================================================================
# Figure 18.2: Prior vs Posterior
# ============================================================================

def generate_figure_18_2():
    """Figure 18.2: How data updates beliefs (prior to posterior)."""
    
    # Simulated scenario: slope prior and posterior
    prior_slope_mean = 0
    prior_slope_std = 5  # Weak prior
    
    # Posterior (tighter, updated by data)
    posterior_slope_mean = 0.28
    posterior_slope_std = 0.15
    
    with figure(6, 18, 2, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Bayesian Updating: Prior to Posterior', fontsize=14, fontweight='bold')
        
        # Plot 1: Prior on slope
        ax1 = plt.subplot(2, 2, 1)
        x = np.linspace(-15, 15, 200)
        prior = norm.pdf(x, prior_slope_mean, prior_slope_std)
        ax1.fill_between(x, prior, alpha=0.5, color='blue', label='Prior')
        ax1.axvline(prior_slope_mean, color='blue', linestyle='--', linewidth=2, label='Prior mean')
        ax1.set_xlabel('Slope (days/year)')
        ax1.set_ylabel('Density')
        ax1.set_title('Prior: Weak belief (SD=5)')
        ax1.set_xlim(-15, 15)
        ax1.legend()
        
        # Plot 2: Likelihood (data information)
        ax2 = plt.subplot(2, 2, 2)
        likelihood = norm.pdf(x, 0.28, 0.08)  # Likelihood peaked at ~0.28
        ax2.fill_between(x, likelihood, alpha=0.5, color='orange', label='Likelihood')
        ax2.axvline(0.28, color='orange', linestyle='--', linewidth=2, label='Data suggests')
        ax2.set_xlabel('Slope (days/year)')
        ax2.set_ylabel('Likelihood')
        ax2.set_title('Likelihood: Data Information')
        ax2.set_xlim(-15, 15)
        ax2.legend()
        
        # Plot 3: Posterior
        ax3 = plt.subplot(2, 2, 3)
        posterior = norm.pdf(x, posterior_slope_mean, posterior_slope_std)
        ax3.fill_between(x, posterior, alpha=0.5, color='green', label='Posterior')
        ax3.axvline(posterior_slope_mean, color='green', linestyle='--', linewidth=2, label='Posterior mean')
        ci_lower = posterior_slope_mean - 1.96 * posterior_slope_std
        ci_upper = posterior_slope_mean + 1.96 * posterior_slope_std
        ax3.axvline(ci_lower, color='green', linestyle=':', linewidth=1.5, label='95% CI')
        ax3.axvline(ci_upper, color='green', linestyle=':', linewidth=1.5)
        ax3.set_xlabel('Slope (days/year)')
        ax3.set_ylabel('Density')
        ax3.set_title('Posterior: Data Updated Belief')
        ax3.set_xlim(-15, 15)
        ax3.legend()
        
        # Plot 4: Overlay
        ax4 = plt.subplot(2, 2, 4)
        ax4.fill_between(x, prior, alpha=0.4, color='blue', label='Prior (weak)')
        ax4.fill_between(x, posterior, alpha=0.4, color='green', label='Posterior (tight)')
        ax4.axvline(prior_slope_mean, color='blue', linestyle='--', linewidth=1)
        ax4.axvline(posterior_slope_mean, color='green', linestyle='--', linewidth=2)
        ax4.set_xlabel('Slope (days/year)')
        ax4.set_ylabel('Density')
        ax4.set_title('Prior vs Posterior Comparison')
        ax4.set_xlim(-4, 2)
        ax4.legend()

# ============================================================================
# Figure 18.3: Posterior Predictive Checks
# ============================================================================

def generate_figure_18_3():
    """Figure 18.3: Posterior predictive checks (simulated vs real data)."""
    
    # Real data
    np.random.seed(42)
    real_data = np.array([12, 15, 18, 14, 22, 16, 25, 13, 20, 17])
    
    # Simulate from posterior (generate predicted data under the model)
    np.random.seed(43)
    n_samples = 1000
    simulated_samples = []
    for _ in range(n_samples):
        # Sample from posterior of intercept, slope, sigma
        b0 = np.random.normal(8.5, 2)
        b1 = np.random.normal(0.28, 0.12)
        sigma = np.random.exponential(2)
        
        # Generate 10 new observations
        ages_new = np.linspace(25, 55, 10)
        y_sim = b0 + b1 * ages_new + np.random.normal(0, sigma, 10)
        simulated_samples.append(y_sim)
    
    simulated_samples = np.array(simulated_samples)
    
    with figure(6, 18, 3, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Posterior Predictive Checks: Model Simulation vs Data', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Data histogram vs simulated
        ax1 = plt.subplot(2, 2, 1)
        ax1.hist(real_data, bins=8, alpha=0.6, density=True, label='Real data', color='red')
        all_sims = simulated_samples.flatten()
        ax1.hist(all_sims, bins=30, alpha=0.3, density=True, label='Simulated samples', color='blue')
        ax1.set_xlabel('Recovery time (days)')
        ax1.set_ylabel('Density')
        ax1.set_title('Distribution: Real vs Simulated')
        ax1.legend()
        
        # Plot 2: Mean comparison
        ax2 = plt.subplot(2, 2, 2)
        real_mean = np.mean(real_data)
        sim_means = np.array([np.mean(s) for s in simulated_samples])
        ax2.hist(sim_means, bins=50, alpha=0.6, edgecolor='black', label='Posterior samples')
        ax2.axvline(real_mean, color='red', linestyle='--', linewidth=3, label='Real data mean')
        ax2.set_xlabel('Mean recovery time (days)')
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'Mean Check: Real={real_mean:.1f} vs Sim={np.mean(sim_means):.1f}')
        ax2.legend()
        
        # Plot 3: SD comparison
        ax3 = plt.subplot(2, 2, 3)
        real_sd = np.std(real_data, ddof=1)
        sim_sds = np.array([np.std(s, ddof=1) for s in simulated_samples])
        ax3.hist(sim_sds, bins=50, alpha=0.6, edgecolor='black', label='Posterior samples')
        ax3.axvline(real_sd, color='red', linestyle='--', linewidth=3, label='Real data SD')
        ax3.set_xlabel('SD of recovery time (days)')
        ax3.set_ylabel('Frequency')
        ax3.set_title(f'SD Check: Real={real_sd:.2f} vs Sim={np.mean(sim_sds):.2f}')
        ax3.legend()
        
        # Plot 4: Max value comparison
        ax4 = plt.subplot(2, 2, 4)
        real_max = np.max(real_data)
        sim_maxes = np.array([np.max(s) for s in simulated_samples])
        ax4.hist(sim_maxes, bins=40, alpha=0.6, edgecolor='black', label='Posterior samples')
        ax4.axvline(real_max, color='red', linestyle='--', linewidth=3, label='Real data max')
        ax4.set_xlabel('Maximum recovery time (days)')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Max Check: Model fits well if line overlaps')
        ax4.legend()

# ============================================================================
# Figure 18.4: Change Point Detection
# ============================================================================

def generate_figure_18_4():
    """Figure 18.4: Change point detection in quality data."""
    
    # Generate data with a known change point
    np.random.seed(42)
    n_days = 100
    change_day = 47
    
    # Before change: higher defect rate
    y_before = np.random.poisson(15, change_day)
    # After change: lower defect rate
    y_after = np.random.poisson(8, n_days - change_day)
    y = np.concatenate([y_before, y_after])
    
    with figure(6, 18, 4, output_dir=OUTPUT_DIR) as fig:
        fig.suptitle('Change Point Detection: When Did Quality Improve?', 
                     fontsize=14, fontweight='bold')
        
        # Plot 1: Raw data with true change point
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(y, 'o-', markersize=4, linewidth=0.8, alpha=0.7)
        ax1.axvline(change_day, color='green', linestyle='--', linewidth=2, label=f'True change: day {change_day}')
        ax1.axhline(15, xmin=0, xmax=change_day/n_days, color='orange', linestyle=':', linewidth=2, label='Before (mean=15)')
        ax1.axhline(8, xmin=change_day/n_days, xmax=1, color='blue', linestyle=':', linewidth=2, label='After (mean=8)')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Defects per day')
        ax1.set_title('Observed Data with True Change Point')
        ax1.legend(fontsize=9)
        ax1.grid(alpha=0.3)
        
        # Plot 2: Posterior probability of change point
        ax2 = plt.subplot(2, 2, 2)
        
        # Compute likelihood for each possible change point
        likelihoods = []
        for tau in range(1, n_days):
            # Likelihood if change is at tau
            before_mean = np.mean(y[:tau])
            after_mean = np.mean(y[tau:])
            
            # Poisson likelihood
            ll_before = np.sum(y[:tau] * np.log(before_mean + 1e-10) - before_mean)
            ll_after = np.sum(y[tau:] * np.log(after_mean + 1e-10) - after_mean)
            ll_total = ll_before + ll_after
            likelihoods.append(ll_total)
        
        likelihoods = np.array(likelihoods)
        likelihoods = np.exp(likelihoods - np.max(likelihoods))  # Normalize
        likelihoods = likelihoods / np.sum(likelihoods)  # Make probability
        
        ax2.plot(range(1, n_days), likelihoods, linewidth=2)
        ax2.fill_between(range(1, n_days), likelihoods, alpha=0.3)
        ax2.axvline(change_day, color='green', linestyle='--', linewidth=2, label='True')
        best_estimate = np.argmax(likelihoods) + 1
        ax2.axvline(best_estimate, color='red', linestyle=':', linewidth=2, label=f'Posterior mode: {best_estimate}')
        ax2.set_xlabel('Hypothesized change day')
        ax2.set_ylabel('Posterior probability')
        ax2.set_title('Where Did Process Change?')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        # Plot 3: Posterior estimates of means
        ax3 = plt.subplot(2, 2, 3)
        best_tau = best_estimate
        before_y = y[:best_tau]
        after_y = y[best_tau:]
        
        before_samples = np.random.poisson(np.mean(before_y), 1000)
        after_samples = np.random.poisson(np.mean(after_y), 1000)
        
        ax3.hist(before_samples, bins=30, alpha=0.5, density=True, label='Before change', color='orange')
        ax3.hist(after_samples, bins=30, alpha=0.5, density=True, label='After change', color='blue')
        ax3.axvline(np.mean(before_y), color='orange', linestyle='--', linewidth=2)
        ax3.axvline(np.mean(after_y), color='blue', linestyle='--', linewidth=2)
        ax3.set_xlabel('Mean defects per day')
        ax3.set_ylabel('Density')
        ax3.set_title('Estimated Quality Before and After')
        ax3.legend()
        
        # Plot 4: Credible interval on change point
        ax4 = plt.subplot(2, 2, 4)
        cumsum_ll = np.cumsum(likelihoods)
        ci_lower = np.where(cumsum_ll >= 0.025)[0][0] + 1
        ci_upper = np.where(cumsum_ll >= 0.975)[0][0] + 1
        
        ax4.fill_between(range(ci_lower, ci_upper+1), 0, 1, alpha=0.3, color='gray', label='95% credible interval')
        ax4.plot(range(1, n_days), likelihoods, linewidth=2, color='black')
        ax4.axvline(best_estimate, color='red', linestyle='-', linewidth=2, label=f'Estimate: day {best_estimate}')
        ax4.axvline(change_day, color='green', linestyle='--', linewidth=2, label=f'True: day {change_day}')
        ax4.set_xlabel('Day')
        ax4.set_ylabel('Posterior probability')
        ax4.set_title(f'95% CI: [{ci_lower}, {ci_upper}]')
        ax4.legend()
        ax4.grid(alpha=0.3)

if __name__ == '__main__':
    print('Generating Chapter 18 figures...')
    
    print('Generating Figure 18.1')
    generate_figure_18_1()
    print('✓ Saved figure: figures/18.1.png')
    
    print('Generating Figure 18.2')
    generate_figure_18_2()
    print('✓ Saved figure: figures/18.2.png')
    
    print('Generating Figure 18.3')
    generate_figure_18_3()
    print('✓ Saved figure: figures/18.3.png')
    
    print('Generating Figure 18.4')
    generate_figure_18_4()
    print('✓ Saved figure: figures/18.4.png')
    
    print('✓ All figures generated successfully!')
