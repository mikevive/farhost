"""ASCII bar chart renderer for weekly reports."""

from __future__ import annotations


def generate_bar(value: float, max_value: float, width: int = 30) -> str:
    """Generate an ASCII bar using block characters.

    Args:
        value: The current value to represent.
        max_value: The maximum value (determines full bar width).
        width: Maximum character width of the bar.

    Returns:
        A string of block characters representing the value.
    """
    if max_value <= 0 or value <= 0:
        return ""

    ratio = min(value / max_value, 1.0)
    filled = int(ratio * width)
    return "\u2588" * filled


def format_hours(seconds: int) -> str:
    """Format seconds as a human-readable hours string (e.g., '6.5h')."""
    hours = seconds / 3600
    if hours == int(hours):
        return f"{int(hours)}.0h"
    return f"{hours:.1f}h"


def format_duration(seconds: int) -> str:
    """Format seconds as HH:MM:SS."""
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
