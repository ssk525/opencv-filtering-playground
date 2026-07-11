"""Image loading and synthetic noisy demo patterns."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def load_image(path: str | Path) -> np.ndarray:
    """Load an image from disk in BGR format (OpenCV default)."""
    image_path = Path(path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported extension '{image_path.suffix}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"OpenCV could not decode image: {image_path}")

    return image


def create_demo_image(width: int = 320, height: int = 240) -> np.ndarray:
    """Create a synthetic BGR pattern with edges for filter demos."""
    image = np.zeros((height, width, 3), dtype=np.uint8)

    half_h, half_w = height // 2, width // 2
    image[:half_h, :half_w] = (0, 0, 255)
    image[:half_h, half_w:] = (0, 255, 0)
    image[half_h:, :half_w] = (255, 0, 0)
    image[half_h:, half_w:] = (0, 255, 255)

    cv2.rectangle(image, (40, 30), (width - 40, height - 30), (255, 255, 255), 2)
    cv2.circle(image, (half_w, half_h), min(half_w, half_h) // 3, (255, 255, 255), 2)
    cv2.line(image, (0, 0), (width, height), (200, 200, 200), 1)

    return image


def add_gaussian_noise(image: np.ndarray, sigma: float = 25.0) -> np.ndarray:
    """Add Gaussian noise to a BGR image for filter comparison demos."""
    if sigma < 0:
        raise ValueError("sigma must be non-negative")

    noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
    noisy = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return noisy
