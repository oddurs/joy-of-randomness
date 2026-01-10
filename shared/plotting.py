"""
Plotting utilities and visualization helpers with consistent styling.

Integrates with FigureManager for seamless figure generation and export.
"""

import matplotlib.pyplot as plt
import seaborn as sns


def histogram(data, bins=30, title=None, xlabel=None, ylabel="Frequency", **kwargs):
    """
    Create a styled histogram with seaborn integration.
    
    Args:
        data: Data to plot
        bins: Number of bins (default 30)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label (default "Frequency")
        **kwargs: Additional kwargs passed to plt.hist()
    
    Returns:
        axes object
    """
    ax = plt.gca()
    ax.hist(data, bins=bins, **kwargs)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return ax


def line_plot(x, y, title=None, xlabel=None, ylabel=None, label=None, **kwargs):
    """
    Create a styled line plot.
    
    Args:
        x: X-axis data
        y: Y-axis data
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        label: Line label for legend
        **kwargs: Additional kwargs passed to plt.plot()
    
    Returns:
        axes object
    """
    ax = plt.gca()
    ax.plot(x, y, label=label, **kwargs)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    if label:
        ax.legend()
    return ax


def scatter_plot(x, y, title=None, xlabel=None, ylabel=None, **kwargs):
    """
    Create a styled scatter plot.
    
    Args:
        x: X-axis data
        y: Y-axis data
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        **kwargs: Additional kwargs passed to plt.scatter()
    
    Returns:
        axes object
    """
    ax = plt.gca()
    ax.scatter(x, y, **kwargs)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    return ax
