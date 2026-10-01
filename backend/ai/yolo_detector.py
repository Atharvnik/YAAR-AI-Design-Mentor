from pathlib import Path

from ultralytics import YOLO


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Trained YOLO model
MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "website_ui_detector"
    / "weights"
    / "best.pt"
)

ANNOTATED_DIR = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "annotated"
    / "results"
)


# Load YOLO model once
model = YOLO(str(MODEL_PATH))


def detect_objects(image_path: Path):
    """
    Run YOLO detection on a UI screenshot.

    Returns:
        List of detected UI elements.
    """

    image_path = Path(image_path)
    ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)

    results = model.predict(
        source=str(image_path),
        conf=0.25,
        verbose=False
    )

    detections = []

    for result in results:

        result.save(
            filename=str(ANNOTATED_DIR / image_path.name)
        )

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class": model.names[class_id],
                "confidence": round(confidence, 4),
                "bbox": {
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "x2": round(x2, 2),
                    "y2": round(y2, 2)
                }
            })

    return detections