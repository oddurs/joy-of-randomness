# Chapter 18: Fitting Models to Messy Data

## The Central Question

You have data. You have a story about how the data was generated. The story has parameters you don't know.

Your job: figure out what parameter values are consistent with what you observed.

This is the beating heart of data science.

## The Central Question

You have data. You have a story about how the data was generated. The story has parameters you don't know.

Your job: figure out what parameter values are consistent with what you observed.

This is the beating heart of data science.

## Real Data: Recovery Time After Surgery

```
Patient   1   2   3   4   5   6   7   8   9   10
Days      12  15  8   18  11  14  13  9   16  12
```

Your story: recovery time depends on patient age. Older patients take longer.

Your model:
$$\text{recovery\_time}_i = β_0 + β_1 \cdot \text{age}_i + ε_i$$

where $ε_i \sim N(0, σ^2)$ is measurement noise.

Unknown parameters: $β_0$ (intercept), $β_1$ (age slope), $σ$ (noise std dev)

Your job: infer these parameters from the data.

---

## The Complete Workflow

### 1. Draw the Generative Story

Before touching data, write down your model mathematically and conceptually.

**What generates the data?**
- Each patient has an age (observed)
- Recovery time depends linearly on age (linear assumption)
- There's random variation around the line (noise)

**Mathematical form:**
$$y_i \sim N(β_0 + β_1 x_i, σ^2)$$

where $y_i$ is recovery time, $x_i$ is age.

### 2. Write the Likelihood

The likelihood is the probability of observing the data given parameters:

$$P(\text{data} \mid β_0, β_1, σ) = \prod_{i=1}^n \frac{1}{\sqrt{2πσ^2}} \exp\left(-\frac{(y_i - (β_0 + β_1 x_i))^2}{2σ^2}\right)$$

Or in log form:

$$\log P(\text{data} \mid θ) = -\sum_i \frac{(y_i - μ_i)^2}{2σ^2} - n \log σ$$

### 3. Specify Priors

What do you believe about the parameters before seeing data?

**Prior on $β_0$ (intercept):**
- Weak prior: $N(0, 100)$ (very uncertain)
- Or informative: based on domain knowledge

**Prior on $β_1$ (slope):**
- Same: $N(0, 100)$

**Prior on $σ$ (noise):**
- Exponential(1) (favors smaller noise, but allows large)

These priors are weakly informative: they don't strongly prejudge the answer.

### 4. Run MCMC

Use Metropolis-Hastings or a more sophisticated algorithm to sample from the posterior:

$$P(θ \mid \text{data}) \propto P(\text{data} \mid θ) \times P(θ)$$

Result: thousands of plausible parameter values.

### 5. Check, Criticize, and Improve

- Do trace plots show convergence?
- Do posterior samples make sense (e.g., $β_1 > 0$)?
- Do simulated predictions match real data?
- Could a different model fit better?

---

## Patterns Emerge: What We Learn

From the posterior samples, you can compute:

**Point estimates:**
- Posterior mean: average parameter value
- Posterior median: middle value
- Maximum a posteriori (MAP): peak of posterior

**Credible intervals:**
- 95% credible interval: range containing 95% of posterior mass
- Interpretation: "we're 95% confident the true value is in this range"

**Model predictions:**
- For a new patient of age 50, what's the expected recovery time?
- Credible interval on the prediction?

### Example Results

Suppose MCMC gives:

- $β_0$: posterior mean 8.2 days, 95% CI [5.1, 11.3]
- $β_1$: posterior mean 0.35 days/year, 95% CI [0.12, 0.58]
- $σ$: posterior mean 2.1 days, 95% CI [1.2, 3.5]

Interpretation:
- Baseline recovery (age=0) is about 8 days (unrealistic, but priors could fix this)
- Each additional year of age adds 0.35 days recovery time on average
- Variability around the line is about 2.1 days
- The slope is uncertain but definitely positive (doesn't include 0)

---

## The Theory: Building Blocks

### The Modeling Workflow

The steps above form a complete cycle:

1. **Generative model**: story + math
2. **Likelihood**: P(data | parameters)
3. **Priors**: P(parameters)
4. **Inference**: P(parameters | data) via MCMC
5. **Criticism**: does the model fit? Are assumptions violated?
6. **Iteration**: refine the model

This is **Bayesian workflow**. It's not linear; you cycle through, improving each time.

### Posterior Predictive Checks

A key diagnostic: **generate fake data from the posterior and compare to real data.**

Algorithm:
1. Sample parameter values from the posterior
2. For each sample, generate predicted data
3. Compare summaries (mean, variance, histogram shape, etc.)

If simulations match reality, the model is plausible. If they diverge, the model is misspecified.

Example: if real data has more outliers than simulated data, the model underestimates noise variance.

### Model Comparison

You have two models:
- Model A: linear effect of age
- Model B: quadratic effect of age

Which is better? Three approaches:

**1. Information criteria:**
- AIC: $-2 \log L + 2k$ (k = number of parameters)
- Smaller AIC is better
- Penalizes complexity

**2. Bayes factor:**
- Ratio of marginal likelihoods: $\frac{P(\text{data} \mid \text{Model A})}{P(\text{data} \mid \text{Model B})}$
- Favors the simpler model if data don't support complexity

**3. Cross-validation:**
- Fit Model A to 80% of data, test on 20%
- Repeat for Model B
- Compare prediction error

---

## Going Deeper

### Hierarchical Models: Partial Pooling

Suppose you have data from multiple hospitals. Each has its own patient outcomes:

- Hospital A: mean recovery = 10.2 days
- Hospital B: mean recovery = 12.1 days
- Hospital C: mean recovery = 10.8 days

**Naive approach**: estimate each mean independently.

**Problem**: Hospital C has only 2 patients. The sample mean is noisy.

**Hierarchical Bayesian approach**:
- Hospitals share information: their means come from a common distribution
- Hospital means: $\mu_j \sim N(\mu_{\text{global}}, τ^2)$
- Global mean: $\mu_{\text{global}} \sim N(11, 5)$

Result: Hospital C's estimate is "shrunken" toward the global mean, borrowing strength from other hospitals. This is **partial pooling**.

### Missing Data

Real data has missing values. Don't discard the observation; treat the missing value as an unknown parameter.

Example: you measure age for 8 patients but one record is lost. Include it as an unknown in MCMC:

- The missing age is sampled from its conditional distribution P(age | recovery time, other parameters)
- Over MCMC iterations, you estimate the posterior of the missing age

This is **multiple imputation** in a Bayesian framework.

### Model Misspecification

All models are wrong. The question is: which are useful?

Common violations:
- **Linearity**: relationship is actually curved
- **Normality**: errors have heavy tails (outliers)
- **Independence**: observations are correlated (e.g., patients from same hospital)
- **Homogeneity**: noise variance changes with covariates

**Robustness**: use models that are less sensitive to violations. For example, replace normal noise with student-t (heavier tails to handle outliers).

### Domain Knowledge

Good models incorporate expert knowledge:

- What's the range of plausible parameter values?
- Are there biological/physical constraints?
- Have similar studies been done?

Informative priors encode this knowledge. The prior + data = posterior that combines both.

A prior saying "$β_1$ is probably positive" doesn't force the conclusion but incorporates domain belief.

---

## A Complete Case Study: Change Point Detection

Suppose you monitor daily defects in a factory. Early on, production quality varies randomly. Then (unknown date) a new process starts, and defects drop.

Your data: defects per day for 100 days. You want to find the change point.

**Model:**
$$y_i = \begin{cases} \mu_1 + ε_i & \text{if } i < τ \\ \mu_2 + ε_i & \text{if } i ≥ τ \end{cases}$$

where $τ$ is the unknown change point day, $μ_1$ and $μ_2$ are mean defects before/after, $ε_i \sim N(0, σ^2)$ is noise.

**Unknowns**: $\mu_1, \mu_2, σ, τ$ (where $τ \in \{1, 2, ..., 100\}$ is discrete).

**Inference**:
1. Specify priors: $\mu_1, \mu_2 \sim N(0, 10)$ (weak), $σ \sim \text{Exponential}(1)$, $τ \sim \text{Uniform}(1, 100)$
2. Run MCMC
3. Posterior of $τ$: a probability distribution over possible change points
4. Maybe it peaks at day 47 with credible interval [42, 52]

**Result**: "We estimate the process changed around day 47, with 95% confidence between days 42-52. Before the change, mean defects were about 15/day; after, about 8/day."

---

## Real-World Considerations

### Computational Issues

- **Slow MCMC**: if proposals have low acceptance, run longer
- **Multimodal posteriors**: use multiple chains, tempering
- **High dimensions**: gradient-based methods (HMC) help

### Software

Modern probabilistic programming languages automate most of this:
- **Stan**: specify the model, it runs HMC for you
- **PyMC**: Python-based, similar
- **Pyro**: for more complex inference

But understanding the mechanics (Chapters 16-17) is essential for diagnosis and improvement.

### Reporting Results

When publishing findings:
- Report posterior means and credible intervals (not p-values)
- Show trace plots (diagnostics)
- Posterior predictive checks (does the model fit?)
- Sensitivity analysis: how much do results change with different priors?
- Compare to simpler models

---

## Rabbit Holes

### The Box-Box Loop

George Box said: "All models are wrong, but some are useful" and "Essentially, all models are wrong, but some are useful."

He also proposed the **Box-Box loop**: model criticism and iteration.

1. Build a model
2. Check it against reality
3. Identify failures
4. Improve the model
5. Repeat

This isn't a path to "the true model" but to progressively better approximations.

### Bayesian Workflow in Practice

Modern Bayesian practice involves:
- Prior predictive simulation: does your prior generate realistic data?
- Posterior predictive checks: does the fitted model generate realistic data?
- Sensitivity analysis: robustness to prior choice
- Model comparison: can you improve the fit?
- Calibration: if you say 95% credible interval, does the true value lie in it 95% of the time?

### Probabilistic Programming Languages

Stan, PyMC, and Pyro let you specify models as programs. The software automatically computes gradients, runs HMC, and handles much of the complexity.

But they're tools. Understanding the workflow (model → likelihood → prior → inference) is more important than memorizing syntax.

---

## Summary

Fitting models to data synthesizes everything in this course:

- **Probability** (Chapter 2): formalize uncertainty
- **Simulation** (Chapter 10): generate fake data from the model
- **Markov chains** (Chapter 8): structure for inference
- **Bayesian reasoning** (Chapter 16): combine prior and data
- **MCMC** (Chapter 17): sample from intractable posteriors

The workflow is:
1. Tell a generative story
2. Write math: likelihood + priors
3. Run MCMC to sample the posterior
4. Check the model against data
5. Improve and iterate

This isn't magic. But it's a rigorous way to learn from data, quantify uncertainty, and make decisions.

The goal isn't to find the "true" model (it doesn't exist). The goal is to build useful ones that reveal what the data is telling you.

---

**Next Steps:** [Exercises](exercises.md) · [Solutions](solutions.md)

**Previous Chapter:** [Chapter 17: Markov Chain Monte Carlo](../17-markov-chain-monte-carlo/README.md)

---

*This is the final chapter of Part 6: Inference. You've learned to think probabilistically, build models, and extract signal from noise.*
- Exploration: Add predictors, hierarchical structure
- Challenge: Full workflow on a real dataset
- Thought experiments: Model complexity, priors, practical tradeoffs
