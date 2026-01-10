# Figure Generation Guide

## Quick Start

Generate all figures for a chapter:

```bash
cd chapters/part-X-[name]/[chapter]-[name]/
python simulations.py --generate-figures
```

**Example: Chapter 1**
```bash
cd chapters/part-1-intuition/01-the-pattern-seeking-mind/
python simulations.py --generate-figures
```

This will create images like:
- `assets/images/1.1.1.png` (Part 1, Chapter 1, Figure 1)
- `assets/images/1.1.2.png` (Part 1, Chapter 1, Figure 2)
- `assets/images/1.1.3.png` (Part 1, Chapter 1, Figure 3)

## File Organization

Figure source code lives in each chapter's `simulations.py`:
- **Part 1, Chapter 1**: `chapters/part-1-intuition/01-the-pattern-seeking-mind/simulations.py`
- **Part 2, Chapter 4**: `chapters/part-2-movement/04-the-drunkards-walk/simulations.py`
- Etc.

Generated figures are centralized in:
- **Output**: `assets/images/` (all figures use naming scheme `{part}.{chapter}.{figure_num}.png`)

Configuration and utilities are in `shared/`:
- **[shared/figures.py](shared/figures.py)** — `FigureManager` class and `figure()` context manager
- **[shared/figure_config.py](shared/figure_config.py)** — Global styling config, margin settings, chapter registry
- **[shared/plotting.py](shared/plotting.py)** — Styled plotting utilities (`histogram()`, `line_plot()`, etc.)
- **[shared/FIGURES.md](shared/FIGURES.md)** — Complete documentation

## How to Create a New Figure

### 1. Write Generation Function

Add to chapter's `simulations.py`:

```python
def generate_figure_1_4(data, title):
    """
    Figure 1.1.4: My New Figure
    Brief description of what this figure shows.
    """
    from shared.figures import figure
    
    with figure(1, 1, 4) as fig:
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set_title(title)
        # ... more plotting code ...
```

### 2. Call from `generate_all_figures()`

```python
def generate_all_figures():
    print("Generating Chapter 1 figures...")
    generate_figure_1_1()
    generate_figure_1_2()
    generate_figure_1_3()
    generate_figure_1_4()  # ← Add your new figure
    print("✓ All figures generated!")
```

### 3. Update README

Add to chapter's README.md:

```markdown
## Generating Figures

To generate all figures:

```bash
python simulations.py --generate-figures
```

### Figure Index

| Figure | File | Description |
|--------|------|-------------|
| 1.1.1 | `1.1.1.png` | Description |
| 1.1.2 | `1.1.2.png` | Description |
| 1.1.3 | `1.1.3.png` | Description |
| 1.1.4 | `1.1.4.png` | Description |
```

And update image references:

```markdown
<img src="../../../assets/images/1.1.4.png" alt="Figure description" width="600">

**Figure 1.1.4:** Description of the figure.
```

## Styling & Configuration

### Global Settings

All figures use:
- **Style**: SciencePlots "science" style (professional, publication-ready)
- **Margin padding**: 1.5 inches (configurable)
- **DPI**: 300 (print-quality)
- **Default size**: 10" × 6"

### Customization

Per-figure overrides:

```python
with figure(1, 1, 5, figsize=(12, 8), margin_pad=2.0) as fig:
    # Larger figure with more margin space
```

Edit [shared/figure_config.py](shared/figure_config.py) to change global defaults:

```python
DEFAULT_MARGIN_PAD = 1.5      # tight_layout pad
SCIENCE_STYLE = "science"     # SciencePlots style
```

## Project Structure

```
├── assets/
│   └── images/          ← All generated figures go here
│       ├── 1.1.1.png
│       ├── 1.1.2.png
│       └── ...
├── chapters/
│   ├── part-1-intuition/
│   │   ├── 01-the-pattern-seeking-mind/
│   │   │   ├── simulations.py     ← Figure generation code lives here
│   │   │   ├── README.md          ← Links to generated figures
│   │   │   ├── exercises.md
│   │   │   └── data/
│   │   ├── 02-what-does-random-look-like/
│   │   │   ├── simulations.py
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── shared/
│   ├── figures.py           ← FigureManager and figure() context manager
│   ├── figure_config.py     ← Global config and chapter registry
│   ├── plotting.py          ← Styled plotting utilities
│   └── FIGURES.md           ← Full documentation
└── requirements.txt
```

## Naming Convention

Format: `{part}.{chapter}.{figure_num}.png`

Each chapter has its own figure numbering (starting at 1):
- **Part 1, Chapter 1, Figure 1**: `1.1.1.png`
- **Part 1, Chapter 1, Figure 2**: `1.1.2.png`
- **Part 1, Chapter 2, Figure 1**: `1.2.1.png` (new chapter, restarts at 1)
- **Part 2, Chapter 4, Figure 3**: `2.4.3.png`

To reference figure 1.1.3 in README:
```markdown
<img src="../../../assets/images/1.1.3.png" alt="Description">
**Figure 1.1.3:** My figure description.
```

## Testing

After generating figures, verify:

1. **Files exist**:
   ```bash
   ls -lh assets/images/1.1.*.png
   ```

2. **Files are valid images**:
   ```bash
   file assets/images/1.1.*.png
   ```

3. **Run demo code**:
   ```bash
   python chapters/part-1-intuition/01-the-pattern-seeking-mind/simulations.py
   ```

## Dependencies

Required packages (in requirements.txt):
- `matplotlib>=3.4.0` — Plotting
- `seaborn>=0.12.0` — Enhanced plots
- `scienceplots>=2.1.0` — Professional styling

Install with:
```bash
pip install -r requirements.txt
```

## For More Details

See [shared/FIGURES.md](shared/FIGURES.md) for:
- Complete API reference
- Configuration options
- Troubleshooting
- Best practices
- Architecture overview
