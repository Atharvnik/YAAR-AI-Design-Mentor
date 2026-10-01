import numpy as np


def make_json_serializable(data):
    """
    Convert NumPy values into standard Python types
    so the result can be returned by FastAPI and sent to Gemini.
    """

    if isinstance(data, dict):
        return {
            key: make_json_serializable(value)
            for key, value in data.items()
        }

    elif isinstance(data, list):
        return [
            make_json_serializable(item)
            for item in data
        ]

    elif isinstance(data, tuple):
        return [
            make_json_serializable(item)
            for item in data
        ]

    elif isinstance(data, np.integer):
        return int(data)

    elif isinstance(data, np.floating):
        return float(data)

    elif isinstance(data, np.ndarray):
        return data.tolist()

    else:
        return data


def merge_results(
    image_path,
    yolo_detections,
    ocr_results,
    clip_results,
    accessibility_results
):
    """
    Combine YOLO, OCR, CLIP and Accessibility results
    into one unified structure for Gemini analysis.
    """

    # -----------------------------
    # YOLO results
    # -----------------------------

    yolo_summary = {
        "count": len(yolo_detections),
        "elements": yolo_detections
    }

    # -----------------------------
    # OCR results
    # -----------------------------

    if isinstance(ocr_results, list):
        ocr_summary = {
            "count": len(ocr_results),
            "text": ocr_results
        }
    else:
        ocr_summary = ocr_results

    # -----------------------------
    # CLIP results
    # -----------------------------

    if isinstance(clip_results, list):
        clip_summary = {
            "results": clip_results
        }
    else:
        clip_summary = clip_results

    # -----------------------------
    # Accessibility results
    # -----------------------------

    accessibility_summary = accessibility_results

    # -----------------------------
    # Final merged result
    # -----------------------------

    merged_result = {
        "image": str(image_path),

        "yolo": yolo_summary,

        "ocr": ocr_summary,

        "clip": clip_summary,

        "accessibility": accessibility_summary
    }

    # -----------------------------
    # Make result JSON safe
    # -----------------------------

    merged_result = make_json_serializable(merged_result)

    return merged_result