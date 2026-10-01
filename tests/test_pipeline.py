from pathlib import Path

from backend.ai.pipeline import analyze_ui


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_full_pipeline():

    print("\n")
    print("==============================")
    print("Testing YAAR AI Pipeline")
    print("==============================")

    print("Image path:", IMAGE_PATH)

    result = analyze_ui(
        IMAGE_PATH,
        run_gemini=False
    )

    assert result is not None
    assert "image" in result
    assert "analysis" in result

    analysis = result["analysis"]

    assert "yolo" in analysis
    assert "ocr" in analysis
    assert "clip" in analysis
    assert "accessibility" in analysis

    print("\nPipeline Result:")
    print("------------------------------")

    print(
        "YOLO detections:",
        analysis["yolo"]["count"]
    )

    print(
        "OCR text:",
        analysis["ocr"]["count"]
    )

    print(
        "Accessibility score:",
        analysis["accessibility"]["accessibility_score"]
    )

    print("\nFull pipeline successful!")


if __name__ == "__main__":
    test_full_pipeline()