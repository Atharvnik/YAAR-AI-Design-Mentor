import cv2
import numpy as np


def preprocess_image(image_path):
    """
    Basic OpenCV preprocessing for UI screenshots.

    Returns:
        original: Original image
        gray: Grayscale image
        edges: Edge-detected image
    """

    # Read image
    original = cv2.imread(str(image_path))

    if original is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Reduce small noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges
    edges = cv2.Canny(blurred, 50, 150)

    return original, gray, edges