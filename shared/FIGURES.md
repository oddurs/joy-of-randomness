# Figure Management System

The current approach for generating publication-quality figures across all chapters.

## Overview

All figures are generated using **Python with Matplotlib and SciencePlots styling**. This provides:
- **Consistent styling**: SciencePlots "science" style applied globally
- **Simplified naming**: Figures named `X.Y.png` (chapter.figure_num)
- **Decentralized generation**: Each chapter manages its own figures
- **Local storage**: Figures stored in each chapter's `src/figures/` directory
- **Publication quality**: 300 DPI PNG export suitable for print/web

## Quick Start

### Generate figures for a chapter:

```bash
cd chapters/part-X/YY-chapter-name/
python src/generate_figures.py
```

This generates PNG files in `src/figures/` with names like `1.1.png`, `1.2.png`, etc.

## Architecture

### Directory Structure

```
chapters/
├── part-1-intuition/
│   ├── 01-the-pattern-seeking-mind/
│   │   ├── src/
│   │   │   ├── generate_figures.py    (* Figure generation script *)
│   │   │   └── figures/
│   │   │       ├── 1.1.png            (* Chapter 1, Figure 1 *)
│   │   │       ├── 1.2.png            (* Chapter 1, Figure 2 *)
│   │   │       ├── 1.3.png
│   │   │       ├── 1.4.png
│   │   │       └── 1.5.png
│   │   └── README.md
│   └── 02-what-does-random-look-like/
│       ├── src/
│       │   ├── generate_figures.py
│       │   └── figures/
│       │       ├── 2.1.png
│       │       ├── 2.2.png
│       │       ├── 2.3.png
│       │       ├── 2.4.png
│       │       └── 2.5.png
│       └── README.md
```

### Figure Naming Convention

Figures use simple naming: `X.Y.png`

- **X** = Chapter number (1, 2, 3, etc.)
- **Y** = Figure number within chapter (1, 2, 3, etc.)

**Examples:**
- `1.1.png` — Chapter 1, Figure 1
- `1.5.png` — Chapter 1, Figure 5
- `2.3.png` — Chapter 2, Figure 3
- `15.7.png` — Chapter 15, Figure 7

This simplified naming replaces the previous scheme `part.chapter.figure` (e.g., `1.2.1.png`), which was redundant.

## Creating Figures: Standard Template

### Basic Structure

Each chapter's `src/generate_figures.py` follows this pattern:

```python
import matplotlib.pyplot as plt
import matplotlib
import random
import statistics
import os

# Configure matplotlib with SciencePlots
matplotlib.style.use('science')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

OUTPUT_DIR = 'src/figures'

def save_figure(fig, filename):
    """Save figure with consistent settings."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.tight_layout(pad=1.5)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {filepath}")
    plt.close(fig)


def generate_figure_X_Y():
    """
    Figure X.Y: [Figure Title]
    [Brief description of what this visualization shows]
    """
    # Generate or load data
    # ... your simulation/data code ...
    
    # Create figure
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    # ... plotting code ...
    
    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_title("Figure Title")
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "X.Y.png")


def generate_all_figures():
    """Generate all figures for this chapter."""
    print("Generating Chapter X figures...")
    print()
    
    print("Generating Figure X.1: [Title]")
    generate_figure_X_1()
    
    print("Generating Figure X.2: [Title]")
    generate_figure_X_2()
    
    # ... more figures ...
    
    print()
    print("All figures generated successfully!")


if __name__ == "__main__":
    generate_all_figures()
```

## Styling Standards

All figures use consistent styling via **SciencePlots**:

- **Style:** `science` (from SciencePlots package)
- **DPI:** 300 (publication quality)
- **Default figsize:** (10, 6) inches
- **Font size:** 11pt (auto-scaled by SciencePlots)
- **Margins:** `tight_layout(pad=1.5)` by default
- **Grid:** Light gray with alpha=0.3 when helpful

### Customizing Figure Size

```python
# Larger figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
# ... plotting code ...
save_figure(fig, "X.Y.png")

# Multi-panel layout
fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# ... plotting code ...
save_figure(fig, "X.Y.png")
```

## Common Figure Patterns

### Histogram with Distribution Overlay

```python
def generate_figure_X_Y():
    """Figure X.Y: Histogram with overlay"""
    data = [random.random() for _ in range(10000)]
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    ax.hist(data, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    ax.axvline(statistics.mean(data), color='red', linestyle='--', 
               linewidth=2, label=f"Mean: {statistics.mean(data):.2f}")
    
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_figure(fig, "X.Y.png")
```

### Multi-Panel Layout

```python
def generate_figure_X_Y():
    """Figure X.Y: Two related plots"""
    fig = plt.figure(figsize=(14, 5))
    
    # Left panel
    ax1 = fig.add_subplot(121)
    ax1.plot([1, 2, 3, 4], [1, 4, 9, 16], linewidth=2)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("Panel 1")
    ax1.grid(True, alpha=0.3)
    
    # Right panel
    ax2 = fig.add_subplot(122)
    ax2.scatter([1, 2, 3, 4], [1, 4, 9, 16], s=100, alpha=0.6)
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_title("Panel 2")
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle("Two Panel Figure", fontsize=14, y=1.02)
    
    save_figure(fig, "X.Y.png")
```

## Integrating Figures into Chapter README

### Proper HTML Structure

All images in chapter READMEs should follow this format:

```markdown
<div align="center">

<img src="./src/figures/X.Y.png" alt="[Description of what the figure shows]" width="600">

**Figure X.Y:** [Complete caption describing what is shown, what to observe, and why it matters.]

</div>
```

**Important:**
- Image path must be `./src/figures/` (relative, not absolute)
- All images must have `width="600"` attribute
- Wrapped in `<div align="center">` for centering
- Descriptive captions with pedagogical value
- Alt text for accessibility

### Example

```markdown
<div align="center">

<img src="./src/figures/2.1.png" alt="Distribution of longest streaks in 100 coin flips" width="600">

**Figure 2.1:** Distribution of longest streaks across 10,000 sequences of 100 coin flips. Notice how most sequences have their longest streak between 6 and 8 flips. This is the signature of a fair coin: expect a run of about 7 in 100 flips.

</div>
```

## Workflow: Adding a New Figure

### Step 1: Add Function to `src/generate_figures.py`

```python
def generate_figure_X_Y():
    """
    Figure X.Y: [Title]
    [Description]
    """
    # ... implementation ...
    save_figure(fig, "X.Y.png")
```

### Step 2: Register in `generate_all_figures()`

```python
def generate_all_figures():
    print("Generating Chapter X figures...")
    print()
    
    # ... existing figures ...
    
    print("Generating Figure X.Y: [Title]")
    generate_figure_X_Y()
    
    print()
    print("All figures generated successfully!")
```

### Step 3: Generate and Verify

```bash
cd chapters/part-X/YY-chapter-name/
python src/generate_figures.py
# Check that src/figures/X.Y.png was created
```

### Step 4: Add to Chapter README

```markdown
<div align="center">

<img src="./src/figures/X.Y.png" alt="[Description]" width="600">

**Figure X.Y:** [Caption]

</div>
```

### Step 5: Commit

```bash
git add chapters/part-X/YY-chapter-name/src/
git commit -m "feat(chapter-X): add Figure X.Y [description]"
git push
```

## Troubleshooting

### SciencePlots not installed

```bash
pip install scienceplots
```

### Figures not being saved

Check:
1. Is `src/figures/` directory writable?
2. Is `OUTPUT_DIR` set correctly?
3. Are part/chapter/figure numbers valid?

### Styling not applied

Verify SciencePlots is imported:
```python
import matplotlib
matplotlib.style.use('science')
import matplotlib.pyplot as plt
```

### Figure text too small/large

Adjust font size:
```python
plt.rcParams['font.size'] = 12  # Default is 11
```

Or adjust individual elements:
```python
ax.set_xlabel("Label", fontsize=13)
ax.set_title("Title", fontsize=14)
```

### Labels getting cut off

Increase margin padding:
```python
fig.tight_layout(pad=2.0)  # Increase from default 1.5
```

## Export Standards

### PNG (Standard Format)

- **Resolution:** 300 DPI (publication quality)
- **Format:** 8-bit RGB with lossless compression
- **Typical width:** 1200–1600px
- **Location:** `chapters/part-X/YY-chapter-name/src/figures/X.Y.png`

Saved via `save_figure()`:
```python
def save_figure(fig, filename):
    fig.tight_layout(pad=1.5)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
```

## Checklist: Before Committing a Figure

- [ ] Figure function implemented in `src/generate_figures.py`
- [ ] Function added to `generate_all_figures()`
- [ ] Script runs without errors
- [ ] PNG file generated at `src/figures/X.Y.png`
- [ ] Image link in README uses `./src/figures/X.Y.png`
- [ ] Image tag includes `width="600"` attribute
- [ ] Image wrapped in `<div align="center">` with caption
- [ ] Caption is clear and pedagogically useful
- [ ] Alt text is descriptive
- [ ] Both script and PNG files committed to git
- [ ] Commit message follows pattern: `feat(chapter-X): add Figure X.Y [description]`

## Best Practices

1. **Clear function names:** Use `generate_figure_X_Y_description()`
2. **Docstrings:** Document what each figure shows
3. **Consistent sizing:** Keep related figures at same size
4. **Test locally:** Verify appearance before committing
5. **Version control:** Commit both script and PNG files
6. **Update README:** Always link figures in chapter content
7. **Descriptive captions:** Explain what to observe and why it matters

## Resources

- **SciencePlots:** https://github.com/garrettj403/SciencePlots
- **Matplotlib:** https://matplotlib.org/stable/users/index.html
- **Matplotlib Color Maps:** https://matplotlib.org/stable/tutorials/colors/colormaps.html
