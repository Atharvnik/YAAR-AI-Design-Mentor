from pathlib import Path

from backend.ai.result_merger import merge_results


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_result_merger():

    print("\nTesting Result Merger...")
    print("Image path:", IMAGE_PATH)

    # -----------------------------
    # Sample YOLO output
    # -----------------------------
    yolo_detections = [
        {
            "class": "button",
            "confidence": 0.87,
            "bbox": {
                "x1": 301.66,
                "y1": 77.34,
                "x2": 347.8,
                "y2": 115.48
            }
        },
        {
            "class": "field",
            "confidence": 0.83,
            "bbox": {
                "x1": 177.39,
                "y1": 172.36,
                "x2": 399.11,
                "y2": 211.28
            }
        }
    ]

    # -----------------------------
    # Sample OCR output
    # -----------------------------
    ocr_results = [
        {
            "text": "Select Payment Method",
            "confidence": 0.87
        },
        {
            "text": "Card number",
            "confidence": 0.99
        },
        {
            "text": "Cardholder",
            "confidence": 1.0
        }
    ]

    # -----------------------------
    # Sample CLIP output
    # -----------------------------
    clip_results = [
        {
            "label": "a payment interface",
            "confidence": 0.996
        },
        {
            "label": "a modern website UI",
            "confidence": 0.0025
        }
    ]

    # -----------------------------
    # Sample Accessibility output
    # -----------------------------
    accessibility_results = {
        "accessibility_score": 90,
        "contrast": 92.37,
        "detected_text_count": 11,
        "ui_elements": {
            "buttons": 2,
            "fields": 1,
            "images": 1,
            "headings": 1
        },
        "issues": [
            {
                "severity": "medium",
                "message": "Some text regions have low OCR confidence."
            }
        ]
    }

    # -----------------------------
    # Merge everything
    # -----------------------------
    result = merge_results(
        image_path=IMAGE_PATH,
        yolo_detections=yolo_detections,
        ocr_results=ocr_results,
        clip_results=clip_results,
        accessibility_results=accessibility_results
    )

    # -----------------------------
    # Display result
    # -----------------------------
    print("\nMerged Result:")
    print(result)

    # -----------------------------
    # Basic validation
    # -----------------------------
    assert "image" in result
    assert "yolo" in result
    assert "ocr" in result
    assert "clip" in result
    assert "accessibility" in result

    assert result["yolo"]["count"] == 2
    assert result["ocr"]["count"] == 3

    print("\nResult Merger successful!")


if __name__ == "__main__":
    test_result_merger()