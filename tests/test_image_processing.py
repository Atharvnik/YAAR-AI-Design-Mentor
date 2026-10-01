from pathlib import Path

from backend.utils.image_processing import preprocess_image


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Test image
IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_image_processing():

    print("\nTesting OpenCV image preprocessing...")
    print("Image path:", IMAGE_PATH)

    original, gray, edges = preprocess_image(IMAGE_PATH)

    print("Original shape:", original.shape)
    print("Gray shape:", gray.shape)
    print("Edges shape:", edges.shape)

    assert original is not None
    assert gray is not None
    assert edges is not None

    print("OpenCV preprocessing successful!")


if __name__ == "__main__":
    test_image_processing()