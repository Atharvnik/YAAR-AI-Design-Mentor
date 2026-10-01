from database.repository import save_ui_review


def test_save_review():

    test_result = {
        "filename": "test_ui.png",
        "image_path": "backend/uploads/test_ui.png",
        "overall_score": 78,
        "summary": "Test UI review",
        "strengths": [
            "Clear layout",
            "Good visual structure"
        ],
        "issues": [
            "Some text is difficult to read"
        ],
        "accessibility": {
            "score": 78
        },
        "recommendations": [
            "Improve text readability"
        ],
        "yolo": {
            "count": 5,
            "elements": []
        },
        "ocr": {
            "count": 2,
            "text": []
        },
        "clip": {
            "results": []
        }
    }

    review_id = save_ui_review(test_result)

    print("================================")
    print("Review saved successfully!")
    print("Review ID:", review_id)
    print("================================")


if __name__ == "__main__":
    test_save_review()