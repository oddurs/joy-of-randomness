# The Joy of Randomness: A Hands-On Journey Through Stochastic Thinking

An interactive, narrative-driven exploration of probability, simulation, and stochastic processes. Designed to be discovered, not memorized.
## Quick Start

```bash
# Clone the repository
git clone https://github.com/oddurs/the-joy-of-randomness.git
cd the-joy-of-randomness

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Explore! Start with Part 1
jupyter notebook chapters/part-1-intuition/
```

See [Appendix A: Python Environment Setup](appendices/a-python-environment-setup.md) for detailed installation options (conda, Docker, etc.).

## Course Structure

The course is organized into **6 parts** spanning **18 chapters**, plus **3 interludes** and **3 appendices**.

### Part 1: Intuition
Build the mental models before formalism.

1. [The Pattern-Seeking Mind](chapters/part-1-intuition/01-the-pattern-seeking-mind/) — Why randomness feels structured
2. [What Does Random Look Like?](chapters/part-1-intuition/02-what-does-random-look-like/) — Developing intuition for randomness
3. [The Long Run](chapters/part-1-intuition/03-the-long-run/) — How frequencies stabilize over time

### Part 2: Movement
Random walks and diffusion processes.

4. [The Drunkard's Walk](chapters/part-2-movement/04-the-drunkards-walk/) — 1D random walks and absorption probabilities
5. [Wandering in Two Dimensions](chapters/part-2-movement/05-wandering-in-two-dimensions/) — 2D random walks and return probabilities
6. [Random Walks in the Wild](chapters/part-2-movement/06-random-walks-in-the-wild/) — Applications in physics, finance, and biology

### Part 3: Memory
Markov chains and temporal dependence.

7. [What Comes Next?](chapters/part-3-memory/07-what-comes-next/) — Conditional probability and prediction
8. [Chains Everywhere](chapters/part-3-memory/08-chains-everywhere/) — Markov chains in natural systems
9. [The Chain That Ranked the Internet](chapters/part-3-memory/09-the-chain-that-ranked-the-internet/) — PageRank and the power of Markov chains

### Part 4: Simulation
Monte Carlo methods and numerical approximation.

10. [Throwing Darts at Pi](chapters/part-4-simulation/10-throwing-darts-at-pi/) — Estimating constants through simulation
11. [When Exact Is Impossible](chapters/part-4-simulation/11-when-exact-is-impossible/) — Complex probability calculations via sampling
12. [Sampling from Strange Distributions](chapters/part-4-simulation/12-sampling-from-strange-distributions/) — Rejection sampling and inverse transform methods

### Part 5: Modeling
Building stochastic models of real systems.

13. [Epidemics](chapters/part-5-modeling/13-epidemics/) — Disease spread as a stochastic process
14. [Queues and Waiting](chapters/part-5-modeling/14-queues-and-waiting/) — Service systems and arrival processes
15. [Populations](chapters/part-5-modeling/15-populations/) — Birth-death processes and population dynamics

### Part 6: Inference
Extracting signal from noisy data.

16. [Thinking in Distributions](chapters/part-6-inference/16-thinking-in-distributions/) — Bayesian reasoning and posterior inference
17. [Markov Chain Monte Carlo](chapters/part-6-inference/17-markov-chain-monte-carlo/) — MCMC for complex posteriors
18. [Fitting Models to Messy Data](chapters/part-6-inference/18-fitting-models-to-messy-data/) — Bayesian model fitting in practice

## Interludes: Randomness Beyond Statistics

Standalone explorations of randomness in unexpected places.

- [Noise as Music](interludes/noise-as-music/) — Spectral properties of randomness, white/pink/brown noise, algorithmic composition
- [Randomness in Cryptography](interludes/randomness-in-cryptography/) — Key generation, one-time pads, RSA, real-world vulnerabilities
- [Randomness in Games](interludes/randomness-in-games/) — Game theory, mixed strategies, skill vs. luck, procedural generation

## Appendices: Reference & Setup

- [Appendix A: Python Environment Setup](appendices/a-python-environment-setup.md) — Installation guides (Quick Start, Conda, Docker, troubleshooting)
- [Appendix B: Probability Refresher](appendices/b-probability-refresher.md) — Definitions, formulas, common distributions, Bayes' theorem
- [Appendix C: Further Reading](appendices/c-further-reading.md) — Curated books and resources by topic

## Philosophy

This course follows the **Feynman spirit**: curiosity first, formalism second. Every concept is introduced through intuition and exploration before moving to mathematical precision. You'll build understanding through code, simulation, and visualization.

### What You'll Learn

- **How to think probabilistically** about the world
- **When and why** randomness matters in practical problems
- **How to write** clean, runnable simulations in Python
- **How to reason** about uncertainty using Bayesian methods
- **How to apply** stochastic thinking to real systems

### Prerequisites

- Basic Python (loops, functions, lists)
- Comfort with high school algebra
- Curiosity about how the world works

No probability background required—we build it from scratch.

## How to Use This Course

**For Self-Study:**
Start with Part 1. Read narratives first, explore code examples interactively in Jupyter notebooks, then work through exercises. Skip theory sections if you're already comfortable—they're always collapsible.

**For Teaching:**
Each chapter has exercises (progressively harder) and solutions. Use simulations.py modules as reference implementations. The narrative-first structure works well for in-person discussion.

**For Reference:**
Jump directly to any chapter. Each is self-contained with links to dependencies. Use Appendix B for probability definitions.

## Repository Structure

```
the-joy-of-randomness/
├── chapters/               # 18 core chapters organized by part
│   ├── part-1-intuition/
│   ├── part-2-movement/
│   ├── part-3-memory/
│   ├── part-4-simulation/
│   ├── part-5-modeling/
│   └── part-6-inference/
├── interludes/            # 3 explorations beyond statistics
│   ├── noise-as-music/
│   ├── randomness-in-cryptography/
│   └── randomness-in-games/
├── appendices/            # 3 reference guides
│   ├── a-python-environment-setup.md
│   ├── b-probability-refresher.md
│   └── c-further-reading.md
├── shared/                # Shared utilities (distributions, plotting, etc.)
└── requirements.txt       # Python dependencies
```

## Running Examples

Each chapter includes runnable code examples. To execute them:

```bash
# Navigate to a chapter
cd chapters/part-1-intuition/01-the-pattern-seeking-mind

# Launch Jupyter
jupyter notebook

# Open simulations.ipynb or run simulations.py directly
python simulations.py
```

All examples use NumPy, SciPy, and Matplotlib. See [Appendix A](appendices/a-python-environment-setup.md) for installation.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Creative Commons Attribution 4.0 International License. See [LICENSE](LICENSE) for details.

## Citation

If you use this course in your work or teaching, please cite it as:

```bibtex
@online{oddurs2026joyofrandomness,
  title={The Joy of Randomness: A Hands-On Journey Through Stochastic Thinking},
  author={Oddur, Oddursson},
  year={2026},
  url={https://github.com/oddurs/the-joy-of-randomness}
}
```

---

**Ready to begin?** Start with [Part 1: Intuition](chapters/part-1-intuition/) or [set up your environment](appendices/a-python-environment-setup.md).