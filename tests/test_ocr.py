from pathlib import Path

from backend.utils.ocr import extract_text


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Test image
IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_ocr():

    print("\nTesting OCR...")
    print("Image path:", IMAGE_PATH)

    results = extract_text(IMAGE_PATH)

    print("\nDetected text:")

    for item in results:
        print(
            f"Text: {item['text']} | "
            f"Confidence: {item['confidence']}"
        )

    assert results is not None

    print("\nOCR extraction successful!")


if __name__ == "__main__":
    test_ocr()