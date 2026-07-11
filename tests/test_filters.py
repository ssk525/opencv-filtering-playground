"""Tests for opencv-filtering-playground."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from image_filters import (  # noqa: E402
    add_gaussian_noise,
    apply_bilateral,
    apply_box_blur,
    apply_gaussian_blur,
    apply_median_blur,
    apply_sharpen,
    create_demo_image,
    load_image,
    save_filter_grid,
)


def test_create_demo_image_shape():
    img = create_demo_image(300, 200)
    assert img.shape == (200, 300, 3)


def test_add_noise_changes_pixels():
    np.random.seed(0)
    img = create_demo_image()
    noisy = add_gaussian_noise(img, sigma=20)
    assert noisy.shape == img.shape
    assert not np.array_equal(noisy, img)


def test_box_blur_preserves_shape():
    img = create_demo_image()
    blurred = apply_box_blur(img)
    assert blurred.shape == img.shape


def test_gaussian_blur_odd_kernel_required():
    img = create_demo_image()
    with pytest.raises(ValueError):
        apply_gaussian_blur(img, ksize=4)


def test_median_blur():
    img = create_demo_image()
    assert apply_median_blur(img, ksize=3).shape == img.shape


def test_bilateral_preserves_shape():
    img = create_demo_image()
    assert apply_bilateral(img).shape == img.shape


def test_sharpen_preserves_shape():
    img = create_demo_image()
    assert apply_sharpen(img).shape == img.shape


def test_save_filter_grid(tmp_path):
    np.random.seed(1)
    noisy = add_gaussian_noise(create_demo_image())
    out = save_filter_grid(noisy, tmp_path / "grid.png")
    assert out.exists()
    assert out.stat().st_size > 0


def test_load_image_missing_file():
    with pytest.raises(FileNotFoundError):
        load_image("missing.png")
