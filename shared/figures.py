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
    SCIENCE_STYLE,
    validate_figure_reference,
)


class FigureManager:
    """
    Manages figure creation, styling, and export with consistent naming conventions.
    
    Naming convention: {part}.{chapter}.{figure_num}.png
    Example: 1.1.1.png (Part 1, Chapter 1, Figure 1)
    """

    def __init__(self, margin_pad=DEFAULT_MARGIN_PAD, figsize=(10, 6), output_dir=None):
        """
        Initialize FigureManager with global styling configuration.
        
        Args:
            margin_pad: Padding for tight_layout (default 1.5)
            figsize: Default figure size as (width, height)
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
        """Apply SciencePlots styling globally."""
        plt.style.use(SCIENCE_STYLE)

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

    def save(self, fig, part, chapter, figure_num, margin_pad=None):
        """
        Save a figure with the naming convention {part}.{chapter}.{figure_num}.png
        
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

        # Apply tight layout
        fig.tight_layout(pad=margin_pad)

        # Create assets directory if needed
        self.assets_dir.mkdir(parents=True, exist_ok=True)

        # Save figure
        filename = f"{part}.{chapter}.{figure_num}.png"
        filepath = self.assets_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches="tight")
        print(f"✓ Saved figure: {filepath}")

    def get_figure_path(self, part, chapter, figure_num):
        """Get the path where a figure will be saved."""
        validate_figure_reference(part, chapter, figure_num)
        filename = f"{part}.{chapter}.{figure_num}.png"
        return self.assets_dir / filename


# Global instance for convenience
_manager = None


def get_manager(margin_pad=DEFAULT_MARGIN_PAD, figsize=(10, 6), output_dir=None):
    """Get or create global FigureManager instance."""
    global _manager
    if _manager is None:
        _manager = FigureManager(margin_pad=margin_pad, figsize=figsize, output_dir=output_dir)
    return _manager


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
