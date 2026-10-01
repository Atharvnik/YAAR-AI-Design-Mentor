import cv2
import easyocr


# Load OCR model once
reader = easyocr.Reader(["en"], gpu=False)


def extract_text(image_path):
    """
    Extract text from a UI screenshot using EasyOCR.

    The screenshot is upscaled while preserving color information.
    Bounding boxes are converted back to the original image scale.

    Returns:
        List of detected text with confidence and bounding box.
    """

    # --------------------------------------------------
    # 1. Read original image
    # --------------------------------------------------
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Could not read image: {image_path}"
        )

    original_height, original_width = image.shape[:2]

    # --------------------------------------------------
    # 2. Upscale image
    # --------------------------------------------------
    scale = 2

    enlarged = cv2.resize(
        image,
        (original_width * scale, original_height * scale),
        interpolation=cv2.INTER_CUBIC
    )

    # --------------------------------------------------
    # 3. Run EasyOCR on the color image
    # --------------------------------------------------
    results = reader.readtext(
        enlarged,
        detail=1,
        paragraph=False
    )

    detections = []

    # --------------------------------------------------
    # 4. Convert bounding boxes back to original scale
    # --------------------------------------------------
    for bbox, text, confidence in results:

        original_bbox = []

        for point in bbox:
            x = point[0] / scale
            y = point[1] / scale

            original_bbox.append([
                round(x, 2),
                round(y, 2)
            ])

        detections.append({
            "text": text,
            "confidence": round(float(confidence), 4),
            "bbox": original_bbox
        })

    return detections