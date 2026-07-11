"""Visualization — save a grid of filter results."""

from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from .filters import (
    apply_bilateral,
    apply_box_blur,
    apply_gaussian_blur,
    apply_median_blur,
    apply_sharpen,
)


def _to_rgb(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_filter_grid(
    noisy_image: np.ndarray,
    output_path: str | Path,
    title: str = "OpenCV Filtering Playground",
) -> Path:
    """Save a 2x3 panel comparing five filters on a noisy input."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    panels = [
        ("Noisy input", noisy_image),
        ("Box blur", apply_box_blur(noisy_image)),
        ("Gaussian blur", apply_gaussian_blur(noisy_image)),
        ("Median blur", apply_median_blur(noisy_image)),
        ("Bilateral filter", apply_bilateral(noisy_image)),
        ("Sharpen", apply_sharpen(noisy_image)),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle(title, fontsize=14)

    for ax, (label, panel) in zip(axes.flat, panels):
        ax.imshow(_to_rgb(panel))
        ax.set_title(label)
        ax.axis("off")

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path
