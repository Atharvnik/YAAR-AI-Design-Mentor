from pathlib import Path

from backend.ai.clip_analyzer import analyze_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_clip():

    print("\nTesting CLIP...")
    print("Image path:", IMAGE_PATH)

    results = analyze_image(IMAGE_PATH)

    print("\nCLIP analysis:")

    for result in results:
        print(
            f"Label: {result['label']} | "
            f"Confidence: {result['confidence']}"
        )

    assert results is not None
    assert len(results) > 0

    print("\nCLIP analysis successful!")


if __name__ == "__main__":
    test_clip()