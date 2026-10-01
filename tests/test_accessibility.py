from pathlib import Path

from backend.ai.accessibility import analyze_accessibility
from backend.utils.ocr import extract_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_accessibility():

    print("\nTesting Accessibility Analysis...")
    print("Image path:", IMAGE_PATH)

    # Get OCR results
    ocr_results = extract_text(IMAGE_PATH)

    # For this first test, we don't need YOLO results yet
    yolo_detections = []

    # Run accessibility analysis
    results = analyze_accessibility(
        image_path=IMAGE_PATH,
        yolo_detections=yolo_detections,
        ocr_results=ocr_results
    )

    print("\nAccessibility Results:")
    print("Accessibility Score:", results["accessibility_score"])

    print(
        "Contrast:",
        results["contrast"]["value"],
        "-",
        results["contrast"]["status"]
    )

    print(
        "Detected Text Count:",
        results["text_analysis"]["text_count"]
    )

    print("\nUI Elements:")
    print(results["ui_elements"])

    print("\nAccessibility Issues:")

    for issue in results["issues"]:
        print(
            f"- [{issue['severity']}] "
            f"{issue['message']}"
        )

    assert results is not None
    assert "accessibility_score" in results
    assert "issues" in results

    print("\nAccessibility analysis successful!")


if __name__ == "__main__":
    test_accessibility()