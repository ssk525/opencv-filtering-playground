#!/usr/bin/env python3
"""CLI entry point for opencv-filtering-playground."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from image_filters import (  # noqa: E402
    add_gaussian_noise,
    create_demo_image,
    load_image,
    save_filter_grid,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare OpenCV blur, denoise, and sharpening filters."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Path to input image. If omitted, a demo pattern is generated.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("output/filters.png"),
        help="Path for filter grid (default: output/filters.png)",
    )
    parser.add_argument(
        "--noise",
        type=float,
        default=25.0,
        help="Gaussian noise sigma for demo (default: 25)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Force demo pattern even if --input is set.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible noise (default: 42)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    import numpy as np

    np.random.seed(args.seed)

    if args.input is None or args.demo:
        image = create_demo_image()
        source = "synthetic demo pattern"
    else:
        image = load_image(args.input)
        source = str(args.input)

    noisy = add_gaussian_noise(image, sigma=args.noise)

    print(f"Loaded: {source}")
    print(f"Shape: {image.shape}  noise sigma: {args.noise}")

    out = save_filter_grid(noisy, args.output)
    print(f"Saved filter grid: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
