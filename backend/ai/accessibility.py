from pathlib import Path

import cv2
import numpy as np


def calculate_contrast(gray_image):
    """
    Calculate basic image contrast using standard deviation.
    Higher value generally means stronger visual variation.
    """

    return float(np.std(gray_image))


def analyze_accessibility(
    image_path: Path,
    yolo_detections=None,
    ocr_results=None
):
    """
    Perform basic accessibility analysis using:
    - OpenCV image information
    - YOLO UI element detections
    - EasyOCR text results
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------------------------
    # 1. Basic image contrast
    # --------------------------------------------------

    contrast_value = calculate_contrast(gray)

    if contrast_value < 40:
        contrast_status = "Low visual contrast"
    else:
        contrast_status = "Acceptable visual contrast"

    # --------------------------------------------------
    # 2. OCR analysis
    # --------------------------------------------------

    text_count = 0
    low_confidence_text = []

    if ocr_results:

        text_count = len(ocr_results)

        for item in ocr_results:

            confidence = item.get("confidence", 0)

            if confidence < 0.5:
                low_confidence_text.append({
                    "text": item.get("text", ""),
                    "confidence": confidence
                })

    # --------------------------------------------------
    # 3. YOLO UI element analysis
    # --------------------------------------------------

    buttons = []
    fields = []
    images = []
    headings = []

    if yolo_detections:

        for detection in yolo_detections:

            class_name = detection.get("class", "").lower()

            if class_name == "button":
                buttons.append(detection)

            elif class_name == "field":
                fields.append(detection)

            elif class_name == "image":
                images.append(detection)

            elif class_name == "heading":
                headings.append(detection)

    # --------------------------------------------------
    # 4. Check for very small UI elements
    # --------------------------------------------------

    small_elements = []

    if yolo_detections:

        for detection in yolo_detections:

            bbox = detection.get("bbox")

            if not bbox:
                continue

            element_width = bbox["x2"] - bbox["x1"]
            element_height = bbox["y2"] - bbox["y1"]

            if element_width < 30 or element_height < 20:

                small_elements.append({
                    "class": detection.get("class"),
                    "width": round(element_width, 2),
                    "height": round(element_height, 2)
                })

    # --------------------------------------------------
    # 5. Generate accessibility issues
    # --------------------------------------------------

    issues = []

    if contrast_value < 40:

        issues.append({
            "type": "contrast",
            "severity": "medium",
            "message": "The interface may contain low visual contrast."
        })

    if low_confidence_text:

        issues.append({
            "type": "text",
            "severity": "medium",
            "message": "Some text regions have low OCR confidence and may need better readability.",
            "items": low_confidence_text
        })

    if small_elements:

        issues.append({
            "type": "element_size",
            "severity": "low",
            "message": "Some UI elements appear very small and may be difficult to interact with.",
            "items": small_elements
        })

    if fields and not text_count:

        issues.append({
            "type": "form_labels",
            "severity": "medium",
            "message": "Form fields were detected, but no readable text was extracted."
        })

    # --------------------------------------------------
    # 6. Accessibility score
    # --------------------------------------------------

    score = 100

    if contrast_value < 40:
        score -= 20

    if low_confidence_text:
        score -= min(20, len(low_confidence_text) * 5)

    if small_elements:
        score -= min(15, len(small_elements) * 3)

    if score < 0:
        score = 0

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    return {
        "image": str(image_path),
        "image_size": {
            "width": width,
            "height": height
        },
        "contrast": {
            "value": round(contrast_value, 2),
            "status": contrast_status
        },
        "text_analysis": {
            "text_count": text_count,
            "low_confidence_text": low_confidence_text
        },
        "ui_elements": {
            "buttons": len(buttons),
            "fields": len(fields),
            "images": len(images),
            "headings": len(headings)
        },
        "small_elements": small_elements,
        "issues": issues,
        "accessibility_score": score
    }