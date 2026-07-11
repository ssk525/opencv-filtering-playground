"""OpenCV blur, denoise, and sharpening filters."""

from __future__ import annotations

import cv2
import numpy as np

_SHARPEN_KERNEL = np.array(
    [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
    dtype=np.float32,
)


def _ensure_odd_kernel(ksize: int, name: str) -> int:
    if ksize <= 0 or ksize % 2 == 0:
        raise ValueError(f"{name} ksize must be a positive odd integer")
    return ksize


def apply_box_blur(image: np.ndarray, ksize: int = 5) -> np.ndarray:
    """Apply average (box) blur with a square kernel."""
    k = _ensure_odd_kernel(ksize, "box blur")
    return cv2.blur(image, (k, k))


def apply_gaussian_blur(image: np.ndarray, ksize: int = 5, sigma_x: float = 0) -> np.ndarray:
    """Apply Gaussian blur — smooth noise while weighting nearby pixels."""
    k = _ensure_odd_kernel(ksize, "Gaussian blur")
    return cv2.GaussianBlur(image, (k, k), sigmaX=sigma_x)


def apply_median_blur(image: np.ndarray, ksize: int = 5) -> np.ndarray:
    """Apply median blur — strong against salt-and-pepper noise."""
    k = _ensure_odd_kernel(ksize, "median blur")
    return cv2.medianBlur(image, k)


def apply_bilateral(
    image: np.ndarray,
    d: int = 9,
    sigma_color: float = 75,
    sigma_space: float = 75,
) -> np.ndarray:
    """Apply bilateral filter — smooth while preserving edges."""
    if d <= 0:
        raise ValueError("bilateral d must be positive")
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def apply_sharpen(image: np.ndarray) -> np.ndarray:
    """Sharpen image using a 3x3 Laplacian-style kernel."""
    return cv2.filter2D(image, ddepth=-1, kernel=_SHARPEN_KERNEL)
