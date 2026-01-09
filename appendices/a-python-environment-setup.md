# Appendix A: Python Environment Setup

Before diving into simulations and code, you need a working Python environment. This appendix walks you through setup, from zero to ready.

## Why This Matters

Python has many versions, and packages have dependencies. A casual install can leave you with conflicts: this library needs version 3.9, that one needs 3.11. Nothing works. You curse computers.

A proper setup—using virtual environments and package managers—keeps projects isolated. Each project has exactly what it needs. Nothing interferes with anything else.

Think of it like kitchen prep. You can cook with dirty utensils, but setup time includes a dish. You can share tools with other projects, but then you're washing between recipes. Better: have a dedicated workspace for this course.

## Quick Start (macOS & Linux)

If you just want to get started quickly:

### Prerequisites

You need:
- Python 3.9 or later (check with `python3 --version`)
- pip (usually comes with Python)
- Git (for cloning the repository)

### Installation

```bash
# Clone the course repository
git clone https://github.com/username/the-joy-of-randomness.git
cd the-joy-of-randomness

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or on Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Test it:

```bash
python3 -c "import numpy; print('Success!')"
```

If you see "Success!", you're ready. Skip to "Running the Code" section.

---

## Full Setup with Condaonment, use Conda. It handles both Python and binary dependencies better than pip alone.

### Install Conda

Download Miniconda (lighter than Anaconda):
- **macOS/Linux:** [https://docs.conda.io/en-us/latest/miniconda.html](https://docs.conda.io/en-us/latest/miniconda.html)
- **Windows:** Same link

Run the installer and follow prompts. Then:

```bash
# Verify installation
conda --version
```

### Create an Environment for This Course

```bash
# Create a new environment with Python 3.11
conda create -n randomness python=3.11

# Activate it
conda activate randomness

# Install packages
pip install -r requirements.txt
```

### What's in requirements.txt?

The course uses:

- **numpy**: Numerical computing (arrays, random number generation)
- **scipy**: Scientific computing (statistics, signal processing)
- **matplotlib**: Plotting (visualization)
- **jupyter**: Interactive notebooks (optional, for exploration)

You can see the full list and versions:

```bash
cat requirements.txt
```

---

## Option 3: Docker (Maximum Isolation)

##
# Build the image
docker build -t randomness-course .

# Run a container
docker run -it -v $(pwd):/work randomness-course bash

# Inside the container, you're isolated
python3 code/chapter-01/simulation.py
```

(Requires Docker to be installed. If you don't know Docker, skip this.)

---

## Troubleshooting

### "Python not found"

## Common Issues and Solutions

# If nothing, install from python.org or your package manager
# macOS: brew install python3
# Ubuntu: sudo apt-get install python3
```

### "pip not found"

```bash
# pip usually comes with Python 3.9+
# If not, install it:
python3 -m ensurepip --upgrade
```

### "Module X not found when I import it"

```bash
# Make sure you activated your environment
source venv/bin/activate  # or: conda activate randomness

# Then install the missing module
pip install module_name
```

### "Different Python each time I run code"

```bash
# Check which Python you're using
which python3

# Make sure your virtual environment is activated
# (Your prompt should show the environment name)
```

---

## Running the Code

Once your environment is ready, the chapters are self-contained.

### From the command line

## Running Code from the Command Line and Notebooksintuition/01-the-pattern-seeking-mind

# Run a simulation
python3 simulations.py
```

### In Jupyter (optional, for exploration)

```bash
# Start Jupyter
jupyter notebook

# Navigate to a chapter directory
# Open a notebook file and run cells
```

### Copy-paste from the course

All code examples in the course are standalone. You can copy a block and run it:

```python
import numpy as np

# This code from Chapter 2
data = np.random.normal(0, 1, 1000)
print(f"Mean: {np.mean(data):.3f}")
```

Paste into a file and run it with `python3 filename.py`.

---

## Recommended Editor Setup

### VS Code (Free, Popular)

1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install Python extension (Microsoft)
3. Install Pylance (for smart autocomplete)

## Choosing Your Editor
```

### PyCharm (Free Community Edition)

Download from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm). A bit heavier but excellent for Python.

### Jupyter Notebooks (For Exploration)

Great for trying ideas quickly:

```bash
# In your activated environment
pip install jupyter

# Start the server
jupyter notebook

# Opens in your browser
```

---

## Upgrading Packages

As time passes, packages update. To refresh:

```bash
# Activate your environment
conda activate randomness  # or: source venv/bin/activate

# Upgrade everything
pip install --upgrade -r requirements.txt
## Keeping Packages Up to Datee:

```bash
pip install --upgrade numpy
```

---

## Managing Multiple Environments

You might have other Python projects. Keep them separate:

```bash
# Create another environment for a different project
conda create -n other-project python=3.10

# Switch between them
conda activate randomness   # This project
conda activate other-project  # That project

## Isolating Multiple Projec

Each environment is isolated. One project's dependency doesn't affect another.

---

## Performance Notes

### If simulations are slow

Some chapters run millions of iterations. This is intentional—you're seeing probability converge. But if you want faster feedback:

1. **Reduce iterations** (in code)
2. **Use NumPy operations** instead of Python loops (NumPy is ~100x faster)
3. **Upgrade your Python** to 3.11+ (inherently faster)
4. **Switch to PyPy** (alternative Python, often faster)

```bash
# Using PyPy (if you want to experiment)
pip install pypy3
## Speed Tips for Simulation
Most code in this course is already optimized (using NumPy), so don't worry.

### If Jupyter is slow

Jupyter notebooks can accumulate state. If things feel sluggish:

```python
# In a Jupyter cell
%reset  # Clear all variables

# Or restart the kernel (menu: Kernel > Restart)
```

---

## Common Workflows

### Workflow 1: Running a chapter's code

```bash
# Activate environment
conda activate randomness

# Navigate to chapter
cd chapters/part-2-movement/04-the-drunkards-walk

# Run simulations
python3 simulations.py

# Edit and experiment
# (Open README.md to follow along)
## Working with Code in Chapterploring interactively

```bash
# Open Jupyter
jupyter notebook

# Navigate to interludes/noise-as-music/

# Copy code blocks into a new cell, run, modify
```

### Workflow 3: Running solutions

```bash
# Check your understanding
cd chapters/part-1-intuition/01-the-pattern-seeking-mind

# Look at solutions
python3 -c "
import solutions
solutions.warm_up_1()  # Run specific exercise
"
```

---

## Final Check

Before starting Chapter 1, verify everything works:

```bash
# Activate your environment
conda activate randomness

# Run this verification script
python3 << 'EOF'
import numpy as np
import scipy
import matplotlib.pyplot as plt

print("✓ NumPy version:", np.__version__)
print("✓ SciPy version:", scipy.__version__)
print("✓ Matplotlib version:", plt.matplotlib.__version__)

# Quick simulation
data = np.random.normal(0, 1, 10000)
print(f"✓ Random data generated: mean={np.mean(data):.3f}, std={np.std(data):.3f}")

print("\nEverything ready. Start Chapter 1!")
EOF
```

If you see checkmarks, you're good. If you see errors, revisit the troubleshooting section.

---

## When to Ask for Help

Common issues and where to find help:

| Problem | Try this |
|---------|----------|
| Module not found | Check environment activated, then `pip install module` |
| Python version conflicts | Use `conda` not `pip` (handles binary dependencies better) |
| Permission errors | Don't use `sudo` with pip. Check virtualenv activation. |
| Slow simulations | Normal for large iterations. Reduce count if testing. |
| Different results each run | That's randomness! Fix seed with `np.random.seed(42)` |

Google your error message. Usually someone's solved it. Stack Overflow is your friend.

---

## Going Deeper (Optional)

### Poetry (Advanced Dependency Management)

For serious projects, Poetry is better than pip:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# In the course directory
poetry install
poetry run python simulations.py
```

### Conda-lock (Reproducibility)

For exact environment reproduction:
## Advanced Dependency Management

<details>
<summary><strong>Poetry and Conda-lock for Reproducibility</strong></summary>ments.txt
```

Ensures everyone gets identical package versions.

### Virtual Environment Best Practices

- Always activate before installing
- Always activate before running code
- Name environments by project
- Delete unused environments (`conda env remove -n name`)

---

## Congratulations

You now have a proper Python environment. This setup will serve you well beyond this course.

You're ready. Let's begin.
</details>

## You're Ready

---

**Return to:** [Table of Contents](../../README.md)