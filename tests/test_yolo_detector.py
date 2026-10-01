from pathlib import Path
from types import SimpleNamespace

from backend.ai import yolo_detector


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Test image
IMAGE_PATH = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
    / "payment.png"
)


def test_yolo():

    print("\nTesting YOLO UI detection...")
    print("Image path:", IMAGE_PATH)

    detections = yolo_detector.detect_objects(IMAGE_PATH)

    print("\nYOLO Detections:")

    for detection in detections:
        print(
            f"Class: {detection['class']} | "
            f"Confidence: {detection['confidence']} | "
            f"BBox: {detection['bbox']}"
        )

    print("\nTotal detections:", len(detections))

    assert detections is not None

    print("\nYOLO detection successful!")


def test_detect_objects_saves_annotated_image(tmp_path, monkeypatch):
    image_path = tmp_path / "shopease.png"
    image_path.touch()
    annotated_dir = tmp_path / "annotated" / "results"

    def save_annotation(filename):
        Path(filename).write_bytes(b"annotated image")

    box = SimpleNamespace(
        cls=[2],
        conf=[0.9],
        xyxy=[SimpleNamespace(tolist=lambda: [1, 2, 3, 4])],
    )
    result = SimpleNamespace(
        boxes=[box],
        save=save_annotation,
    )

    monkeypatch.setattr(yolo_detector, "ANNOTATED_DIR", annotated_dir)
    monkeypatch.setattr(
        yolo_detector,
        "model",
        SimpleNamespace(
            names={2: "button"},
            predict=lambda **kwargs: [result],
        ),
    )

    detections = yolo_detector.detect_objects(image_path)

    assert detections[0]["class"] == "button"
    assert (annotated_dir / "shopease.png").read_bytes() == b"annotated image"


if __name__ == "__main__":
    test_yolo()