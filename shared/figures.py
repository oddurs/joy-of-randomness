"""
Figure management system for consistent, reproducible figure generation and export.

Handles naming conventions, SciencePlots styling, and automatic export to custom directories.
"""

import os
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401 - imported to register styles
from pathlib import Path
from contextlib import contextmanager
from .figure_config import (
    DEFAULT_MARGIN_PAD,
    DEFAULT_FIGSIZE,
    DEFAULT_TITLE_FONTSIZE,
    SCIENCE_STYLE,
    validate_figure_reference,
)


class FigureManager:
    """
    Manages figure creation, styling, and export with consistent naming conventions.
    
    Naming convention: {part}.{chapter}.{figure_num}.png
    Example: 1.1.1.png (Part 1, Chapter 1, Figure 1)
    """

    def __init__(self, margin_pad=DEFAULT_MARGIN_PAD, figsize=DEFAULT_FIGSIZE, output_dir=None):
        """
        Initialize FigureManager with global styling configuration.
        
        Args:
            margin_pad: Padding for tight_layout (default 2.8 ≈ 40px)
            figsize: Default figure size as (width, height) (default 12x7)
            output_dir: Optional custom output directory (default: assets/images/)
        """
        self.margin_pad = margin_pad
        self.figsize = figsize
        self._setup_styling()
        
        if output_dir is None:
            self.assets_dir = Path(__file__).parent.parent / "assets" / "images"
        else:
            self.assets_dir = Path(output_dir)

    def _setup_styling(self):
        """Apply SciencePlots styling with custom margins and font sizes."""
        # Apply SciencePlots style first
        plt.style.use(SCIENCE_STYLE)
        # Then override with our custom settings to ensure they take precedence
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.titlesize'] = DEFAULT_TITLE_FONTSIZE
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['figure.autolayout'] = False
        plt.rcParams['axes.linewidth'] = 1.2
        plt.rcParams['grid.linewidth'] = 0.8

    @contextmanager
    def figure(
        self,
        part,
        chapter,
        figure_num,
        figsize=None,
        margin_pad=None,
        **kwargs
    ):
        """
        Context manager for creating and managing figures.
        
        Args:
            part: Part number (1-6)
            chapter: Chapter number (1-18)
            figure_num: Figure number within chapter (starting at 1)
            figsize: Optional figure size override, defaults to self.figsize
            margin_pad: Optional margin padding override, defaults to self.margin_pad
            **kwargs: Additional kwargs passed to plt.figure()
        
        Yields:
            matplotlib figure object
        
        Example:
            with fm.figure(1, 1, 1) as fig:
                plt.plot([1, 2, 3], [1, 4, 9])
                plt.title("My Figure")
        """
        # Validate figure reference
        validate_figure_reference(part, chapter, figure_num)

        # Apply defaults
        if figsize is None:
            figsize = self.figsize
        if margin_pad is None:
            margin_pad = self.margin_pad

        # Create figure
        fig = plt.figure(figsize=figsize, **kwargs)
        filename = f"{part}.{chapter}.{figure_num}.png"

        try:
            yield fig
        finally:
            # Save and close figure
            self.save(fig, part, chapter, figure_num, margin_pad=margin_pad)
            plt.close(fig)

    def _generate_filename(self, part, chapter, figure_num):
        """
        Generate filename from part, chapter, and figure number.
        
        Uses format: {chapter}.{figure_num}.png
        where chapter is the global chapter number (1-18)
        
        Args:
            part: Part number (1-6)
            chapter: Chapter number (1-18)
            figure_num: Figure number within chapter (starting at 1)
        
        Returns:
            Filename string (e.g., "1.1.png" for chapter 1 figure 1)
        """
        return f"{chapter}.{figure_num}.png"

    def save(self, fig, part, chapter, figure_num, margin_pad=None):
        """
        Save a figure with the naming convention {part}.{figure_num}.png
        
        Args:
            fig: matplotlib figure object
            part: Part number (1-6)
            chapter: Chapter number (1-18)
            figure_num: Figure number within chapter (starting at 1)
            margin_pad: Optional margin padding override
        """
        # Validate figure reference
        validate_figure_reference(part, chapter, figure_num)

        if margin_pad is None:
            margin_pad = self.margin_pad

        # Use subplots_adjust to set explicit margins around all content
        # margin_pad value directly converts to figure fraction
        margin_fraction = margin_pad * 0.05  # 4.0 pad -> 0.20 (20%) margins
        
        fig.subplots_adjust(
            left=margin_fraction,
            right=1 - margin_fraction,
            top=1 - margin_fraction * 0.9,
            bottom=margin_fraction * 0.9,
            wspace=0.3,
            hspace=0.4
        )

        # Create assets directory if needed
        self.assets_dir.mkdir(parents=True, exist_ok=True)

        # Save figure
        filename = self._generate_filename(part, chapter, figure_num)
        filepath = self.assets_dir / filename
        fig.savefig(filepath, dpi=300)
        print(f"✓ Saved figure: {filepath}")

    def get_figure_path(self, part, chapter, figure_num):
        """Get the path where a figure will be saved."""
        validate_figure_reference(part, chapter, figure_num)
        filename = self._generate_filename(part, chapter, figure_num)
        return self.assets_dir / filename


# Global instances for convenience (one per output directory)
_managers = {}


def get_manager(margin_pad=DEFAULT_MARGIN_PAD, figsize=DEFAULT_FIGSIZE, output_dir=None):
    """Get or create FigureManager instance (cached per output_dir)."""
    global _managers
    
    # Use output_dir as cache key (None for default assets/images)
    cache_key = output_dir if output_dir is not None else "default"
    
    if cache_key not in _managers:
        _managers[cache_key] = FigureManager(margin_pad=margin_pad, figsize=figsize, output_dir=output_dir)
    return _managers[cache_key]


def figure(part, chapter, figure_num, figsize=None, margin_pad=None, output_dir=None, **kwargs):
    """
    Convenience function for creating figures with global manager.
    
    Usage:
        with figure(1, 1, 1, output_dir="./src/figures") as fig:
            plt.plot([1, 2, 3])
            plt.title("My Figure")
    
    Args:
        part: Part number (1-6)
        chapter: Chapter number (1-18)
        figure_num: Figure number within chapter (starting at 1)
        figsize: Optional figure size override
        margin_pad: Optional margin padding override
        output_dir: Optional custom output directory (default: assets/images/)
        **kwargs: Additional kwargs passed to plt.figure()
    """
    manager = get_manager(output_dir=output_dir)
    return manager.figure(
        part, chapter, figure_num, figsize=figsize, margin_pad=margin_pad, **kwargs
    )
