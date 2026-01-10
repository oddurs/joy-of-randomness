# Figure Management System

A centralized, configuration-driven system for generating, styling, and exporting publication-quality figures for the "Joy of Randomness" project.

## Overview

This system provides:
- **Consistent styling**: Global SciencePlots styling (science style) applied to all figures
- **Automatic naming**: Figures automatically named `{part}.{chapter}.{figure_num}.png` (e.g., `1.1.1.png`, `2.3.2.png`)
- **Central configuration**: Margin and styling settings managed in one place
- **Easy integration**: Simple context manager API for figure creation
- **Organized output**: All figures exported to `assets/images/`

## Architecture

### Key Modules

**[shared/figures.py](figures.py)**
- `FigureManager` class: Handles figure creation, styling, and export
- `figure()` context manager: Convenient API for creating figures
- Global manager instance for simplicity

**[shared/figure_config.py](figure_config.py)**
- `DEFAULT_MARGIN_PAD`: Global margin padding (default 1.5)
- `SCIENCE_STYLE`: SciencePlots style to use (set to "science")
- `CHAPTER_METADATA`: Registry of all chapters in the project
- `validate_figure_reference()`: Ensures figures are registered before use

**[shared/plotting.py](plotting.py)**
- `histogram()`: Styled histogram plotting
- `line_plot()`: Styled line plot
- `scatter_plot()`: Styled scatter plot

## Usage

### Basic Usage

```python
from shared.figures import figure
import matplotlib.pyplot as plt

# Create and save a figure
with figure(1, 1, 1) as fig:
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("My Figure")
    ax.set_xlabel("X-axis")
```

This automatically:
- Creates a figure with SciencePlots styling
- Saves it to `assets/images/1.1.1.png` (300 DPI)
- Applies margin padding (1.5 by default)
- Cleans up resources

### With Custom Sizing and Margins

```python
with figure(1, 1, 2, figsize=(12, 8), margin_pad=2.0) as fig:
    ax = fig.add_subplot(111)
    # ... plot code ...
```

### Using Plotting Utilities

```python
from shared.figures import figure
from shared.plotting import histogram, line_plot
import matplotlib.pyplot as plt

with figure(2, 4, 3) as fig:
    ax = fig.add_subplot(111)
    
    # Using utility function
    histogram([1, 2, 2, 3, 3, 3, 4], title="My Histogram", xlabel="Value")
```

## Naming Convention

Figures follow the pattern: `{part}.{chapter}.{figure_num}.png`

Examples:
- Part 1, Chapter 1, Figure 1: `1.1.1.png`
- Part 2, Chapter 4, Figure 2: `2.4.2.png`
- Part 6, Chapter 18, Figure 5: `6.18.5.png`

**Key points:**
- Each chapter starts counting at figure 1
- Figure numbering restarts for each chapter
- Parts and chapters must be registered in `CHAPTER_METADATA`

## Configuration

### Global Settings

Edit [shared/figure_config.py](figure_config.py):

```python
# Margin padding (tight_layout pad)
DEFAULT_MARGIN_PAD = 1.5

# SciencePlots style
SCIENCE_STYLE = "science"

# Figure size (width, height in inches)
# Note: Not in config, but in FigureManager.__init__()
figsize = (10, 6)
```

### Per-Figure Overrides

```python
# Larger figure with more margin
with figure(1, 1, 4, figsize=(14, 10), margin_pad=2.5) as fig:
    # ... plot code ...
```

## Chapter Integration

### Pattern for Adding Figures to a Chapter

1. **Add generation function** to `simulations.py`:
   ```python
   def generate_figure_X_Y(arg1, arg2):
       """Figure X.Y.Z: Description"""
       # ... generate data ...
       with figure(x, y, z) as fig:
           ax = fig.add_subplot(111)
           # ... plot code ...
   ```

2. **Add to generation script**:
   ```python
   def generate_all_figures():
       print("Generating Chapter X figures...")
       generate_figure_X_Y()
       # ... more figures ...
   ```

3. **Update README** with:
   - Quick-start instructions
   - Figure index table
   - Image links using new naming scheme

4. **Update figure_config.py** if needed:
   - Add chapter to `CHAPTER_METADATA` if not present

### Example: Chapter 1

See [chapters/part-1-intuition/01-the-pattern-seeking-mind/](../chapters/part-1-intuition/01-the-pattern-seeking-mind/) for a complete reference implementation.

Running figures:
```bash
cd chapters/part-1-intuition/01-the-pattern-seeking-mind/
python simulations.py --generate-figures
```

## Styling Details

### SciencePlots Configuration

The system uses the **"science"** style from [SciencePlots](https://github.com/garrettj403/SciencePlots), which provides:
- Professional typography
- Optimized colors
- Clean grid lines
- Proper figure proportions

Style applied globally in `FigureManager._setup_styling()`:
```python
plt.style.use("science")
```

### Margin Configuration

Margins are controlled via matplotlib's `tight_layout(pad=...)`:
- `pad=1.0`: Minimal margins (1 inch spacing)
- `pad=1.5`: Default (moderate spacing)
- `pad=2.0+`: Extra space around plots

Larger margins useful for:
- Figures with long axis labels
- Multi-subplot layouts
- Dense legend boxes

## API Reference

### `figure(part, chapter, figure_num, figsize=None, margin_pad=None, **kwargs)`

Context manager for creating figures.

**Parameters:**
- `part` (int): Part number (1-6)
- `chapter` (int): Chapter number (1-18)
- `figure_num` (int): Figure number within chapter (≥1)
- `figsize` (tuple): Optional (width, height), defaults to (10, 6)
- `margin_pad` (float): Optional padding override
- `**kwargs`: Passed to `plt.figure()`

**Returns:**
- matplotlib Figure object

**Raises:**
- `ValueError`: If (part, chapter) not in CHAPTER_METADATA

### `FigureManager.save(fig, part, chapter, figure_num, margin_pad=None)`

Manually save a figure (usually called automatically by context manager).

**Parameters:**
- `fig`: matplotlib Figure object
- `part`, `chapter`, `figure_num`: Figure identification
- `margin_pad`: Optional override of default padding

### `get_chapter_metadata(part, chapter)`

Retrieve metadata for a chapter.

**Returns:**
- Dict with keys: `title`, `part` (name)

## Troubleshooting

### Figure not being saved

Check:
1. Is the chapter registered in `CHAPTER_METADATA`?
2. Is `assets/images/` writable?
3. Are part/chapter/figure numbers valid integers?

```python
# Debug: Check if chapter is registered
from shared.figure_config import validate_figure_reference
validate_figure_reference(1, 1, 1)  # Raises ValueError if not registered
```

### Styling not applied

Ensure SciencePlots is installed:
```bash
pip install scienceplots
```

Verify in Python:
```python
import scienceplots
import matplotlib.pyplot as plt
plt.style.use("science")
print(plt.style.available)  # Should include "science"
```

### Figures too small or too large

Adjust `figsize` parameter:
```python
with figure(1, 1, 1, figsize=(16, 10)) as fig:
    # 16 inches wide, 10 inches tall
```

### Labels getting cut off

Increase margin padding:
```python
with figure(1, 1, 1, margin_pad=2.5) as fig:
    # More space around content
```

## Best Practices

1. **Use descriptive figure function names**: `generate_figure_X_Y_description()`
2. **Add docstrings**: Document what each figure shows
3. **Use consistent sizing**: Keep similar figures same size
4. **Test locally**: Generate figures and verify appearance before committing
5. **Version control**: Commit `.png` files to preserve publication state
6. **Update README**: Link new figures with updated asset names

## Future Enhancements

Potential improvements:
- SVG export option for scalability
- Figure metadata sidecar files (JSON with description, source data, etc.)
- Automated figure gallery generation
- Cross-chapter figure references
- Figure caching to avoid re-rendering
