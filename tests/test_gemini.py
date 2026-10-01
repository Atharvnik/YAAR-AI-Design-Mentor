from pathlib import Path

from backend.ai.gemini_reviewer import review_ui


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_gemini():

    print("\nTesting Gemini UI/UX Review...")
    print("Image path:", IMAGE_PATH)

    # Sample merged result
    merged_result = {

        "image": str(IMAGE_PATH),

        "yolo": {
            "count": 2,
            "elements": [
                {
                    "class": "button",
                    "confidence": 0.87
                },
                {
                    "class": "field",
                    "confidence": 0.83
                }
            ]
        },

        "ocr": {
            "count": 3,
            "text": [
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
        },

        "clip": {
            "results": [
                {
                    "label": "a payment interface",
                    "confidence": 0.996
                },
                {
                    "label": "a modern website UI",
                    "confidence": 0.0025
                }
            ]
        },

        "accessibility": {
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
    }

    # Send to Gemini
    review = review_ui(merged_result)

    print("\n" + "=" * 60)
    print("GEMINI UI/UX REVIEW")
    print("=" * 60)

    print(review)

    print("\n" + "=" * 60)
    print("Gemini review successful!")
    print("=" * 60)


if __name__ == "__main__":
    test_gemini()