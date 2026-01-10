"""
Global configuration for figure generation and management.

Defines figure metadata, naming conventions, and default styling settings.
"""

# Default margin/padding for figures (tight_layout pad parameter)
# Higher values = more space around content
# Typical range: 0.5 (minimal) to 3.0+ (generous)
DEFAULT_MARGIN_PAD = 4.0

# SciencePlots style to use globally
SCIENCE_STYLE = "science"

# Default figure size (scaled up for better readability)
DEFAULT_FIGSIZE = (14, 8)

# Title font size for headers
DEFAULT_TITLE_FONTSIZE = 14

# Chapter metadata: (part, chapter) -> {metadata}
CHAPTER_METADATA = {
    (1, 1): {"title": "The Pattern-Seeking Mind", "part": "Intuition"},
    (1, 2): {"title": "What Does Random Look Like?", "part": "Intuition"},
    (1, 3): {"title": "The Long Run", "part": "Intuition"},
    (2, 4): {"title": "The Drunkard's Walk", "part": "Movement"},
    (2, 5): {"title": "Wandering in Two Dimensions", "part": "Movement"},
    (2, 6): {"title": "Random Walks in the Wild", "part": "Movement"},
    (3, 7): {"title": "What Comes Next?", "part": "Memory"},
    (3, 8): {"title": "Chains Everywhere", "part": "Memory"},
    (3, 9): {"title": "The Chain That Ranked the Internet", "part": "Memory"},
    (4, 10): {"title": "Throwing Darts at Pi", "part": "Simulation"},
    (4, 11): {"title": "When Exact is Impossible", "part": "Simulation"},
    (4, 12): {"title": "Sampling from Strange Distributions", "part": "Simulation"},
    (5, 13): {"title": "Epidemics", "part": "Modeling"},
    (5, 14): {"title": "Queues and Waiting", "part": "Modeling"},
    (5, 15): {"title": "Populations", "part": "Modeling"},
    (6, 16): {"title": "Thinking in Distributions", "part": "Inference"},
    (6, 17): {"title": "Markov Chain Monte Carlo", "part": "Inference"},
    (6, 18): {"title": "Fitting Models to Messy Data", "part": "Inference"},
}


def get_chapter_metadata(part, chapter):
    """Get metadata for a chapter."""
    return CHAPTER_METADATA.get((part, chapter), {})


def validate_figure_reference(part, chapter, figure_num):
    """
    Validate that a figure reference is properly registered.
    
    Args:
        part: Part number (1-6)
        chapter: Chapter number (1-18)
        figure_num: Figure number within chapter (starting at 1)
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if (part, chapter) not in CHAPTER_METADATA:
        raise ValueError(f"Chapter ({part}, {chapter}) not registered in CHAPTER_METADATA")
    return True
