# Chapter 18 Exercises: Fitting Models to Messy Data

## Warm-up Exercises

**1. Fit a normal distribution to data**

Generate 50 random samples from N(5, 2) (mean=5, std=2). Treat mean and std as unknowns.

Use MCMC to estimate the posterior of (mean, std).

Report:
- Posterior means
- 95% credible intervals
- Do they match the true values?

---

**2. Recovery time regression**

Use `simulations.py` to generate recovery time data (age vs. recovery days).

Fit the linear regression model via MCMC:
$$y_i = β_0 + β_1 \cdot \text{age}_i + ε_i$$

Report:
- Posterior mean and 95% CI for intercept β₀
- Posterior mean and 95% CI for slope β₁
- Interpret: does age affect recovery? By how much?

---

**3. Posterior predictive check**

After fitting the regression model, generate predictions for new ages (e.g., 30, 50, 70).

For each age, compute the posterior predictive distribution (using `posterior_predictive_regression`).

Plot:
- Observed data
- Posterior mean line
- 95% predictive interval shaded

Does the model fit the data well?

---

**4. Prior sensitivity**

Refit the regression model with different priors:

**Weak prior**: N(0, 100) on β₀, β₁
**Strong prior**: N(0, 1) on β₁ (expects small slope)

Compare posteriors. How much does the prior change the inference?

(Hint: the data should dominate, so posteriors should be similar.)

---

## Exploration Exercises

**5. Quadratic regression**

Extend the recovery model to include age squared:
$$y_i = β_0 + β_1 \cdot \text{age}_i + β_2 \cdot \text{age}_i^2 + ε_i$$

Fit via MCMC.

Compare to linear model:
- Which has better fit (lower residual std dev)?
- Do the credible intervals on β₂ include 0?
- Use posterior predictive check: which model fits better?

---

**6. Change point detection**

Use `generate_changepoint_data` to create a time series with a known change point.

Implement MCMC for the change point model. Sample the unknown changepoint location τ and means μ₁, μ₂.

Result: posterior distribution of τ. Does it locate the true change point?

Visualize: trace plot of τ and histogram of posterior.

---

**7. Robust regression**

Real data often has outliers. Standard normal errors assume symmetric, light-tailed distribution.

Use Student-t errors instead:
$$y_i \sim t_{ν}(μ_i, σ)$$

where ν is the degrees of freedom (lower ν = heavier tails).

Fit a regression with:
- Normal errors (your baseline)
- t-distributed errors with ν = 3

Compare:
- Are slope estimates similar?
- How does the posterior of σ change?
- Which model is more robust to outliers?

---

**8. Missing data**

Generate regression data, then "lose" some y values (mark them as NA).

Treat missing values as unknown parameters to sample in MCMC.

For each MCMC iteration:
- Sample the missing y values from their predictive distribution
- Sample β₀, β₁, σ given all y values (including sampled missing ones)

Result: posterior inference despite missing data.

---

## Challenge Exercises

**9. Hierarchical regression**

You have data from multiple hospitals. Each hospital has its own regression line (different intercept).

Model:
$$y_{ij} = α_i + β \cdot \text{age}_{ij} + ε_{ij}$$

where α_i is hospital i's intercept, β is shared slope.

Hospital intercepts share structure:
$$α_i \sim N(α_{\text{global}}, τ^2)$$

Implement hierarchical MCMC (or use Stan/PyMC).

Compare to:
- Fitting each hospital independently
- Fitting a pooled model (all hospitals the same)

Hierarchical should be in between: borrows strength across hospitals.

---

**10. Prior-posterior distance**

After fitting a model, compute the KL divergence between prior and posterior for each parameter.

High divergence = data strongly shaped the posterior = informative data.
Low divergence = prior was already close = data didn't change belief much.

Interpret: which parameters did the data inform most?

---

**11. Model comparison: AIC vs. Bayes factor**

Fit two competing models (e.g., linear vs. quadratic regression).

Compute:
- **AIC**: $-2 \log L + 2k$ (smaller is better)
- **Bayes factor**: ratio of marginal likelihoods (harder to compute, but conceptually cleaner)

Do they agree on which model is better?

---

**12. Leave-one-out cross-validation**

For each observation:
1. Fit the model excluding that observation
2. Predict the left-out observation
3. Compute prediction error

Average prediction error: estimates out-of-sample predictive accuracy.

Compare models via LOO-CV. Which is more predictive?

---

## Thought Experiments

**13. Complexity vs. fit**

You have a choice:
- **Simple model**: y = β₀ + ε (just a constant)
- **Complex model**: y = β₀ + β₁ x + β₂ x² + β₃ x³ + ... (many terms)

The complex model always fits the data better (lower residuals). But why might you prefer the simple model?

Consider:
- Interpretation
- Generalization to new data
- Computational cost
- Prior on complexity

---

**14. Informative vs. uninformative priors**

When should you use informative priors?

**For**: you have domain knowledge, small data, want to incorporate expert opinion
**Against**: priors can bias results, hard to justify, less objective

Discuss:
- When is a weak prior "uninformative"? (Answer: it depends on parameterization)
- How do you choose between priors?
- How do you report sensitivity to prior choice?

---

**15. The model checking loop**

The workflow isn't linear: model → fit → done. It's iterative.

1. Fit model
2. Check: does it fit? Are assumptions violated?
3. Improve: refine the model
4. Repeat

Example workflow for regression:
- Fit linear model
- Check posterior predictive: simulated data matches reality?
- If not, try quadratic
- If still not, try robust errors (Student-t)
- Continue until satisfied

Discuss: when do you stop improving?

---

## Open-Ended Exploration

**Choose your own data**

Find a real dataset you care about (UCI ML repository, Kaggle, your own data).

Complete workflow:
1. **Exploratory analysis**: plot data, compute summaries
2. **Model building**: propose a generative model
3. **Inference**: implement and run MCMC
4. **Diagnosis**: trace plots, posterior predictive checks
5. **Interpretation**: what did you learn? What's uncertain?
6. **Comparison**: try alternative models, compare
7. **Reporting**: write up findings with credible intervals and diagnostics

Document each step. This is the real work of data science.

---

**Probabilistic programming**

Learn Stan or PyMC (beyond hand-coded MCMC).

Refit your chosen model using one of these languages.

Advantages:
- Automatic differentiation (HMC)
- Less code, fewer bugs
- Built-in diagnostics and model comparison
- Easier to extend

Document:
- Model specification in code
- Results compared to hand-coded MCMC
- Advantages and disadvantages of each approach

---

**Sensitivity and robustness**

For your model:
1. Refit with different priors (weak, strong, informative)
2. Refit with different data subsets
3. Refit with outliers removed

How much do results change?
- Robust (stable): results don't depend on priors or minor data details
- Fragile (sensitive): small changes cause big shifts

Discuss: what makes an analysis robust?
