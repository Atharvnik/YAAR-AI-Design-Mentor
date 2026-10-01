from ultralytics import YOLO
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset configuration
DATASET_CONFIG = PROJECT_ROOT / "dataset" / "data.yaml"

# Output directory
OUTPUT_DIR = PROJECT_ROOT / "backend" / "models"


def train_model():
    print("Starting Website UI Detection model training...")
    print(f"Dataset: {DATASET_CONFIG}")
    print(f"Output: {OUTPUT_DIR}")

    # YOLOv8 small model
    model = YOLO("yolov8n.pt")

    model.train(
        data=str(DATASET_CONFIG),
        epochs=50,
        imgsz=640,
        batch=16,
        project=str(OUTPUT_DIR),
        name="website_ui_detector",
        exist_ok=True
    )

    print("\nTraining completed!")

    # Best trained model
    best_model = OUTPUT_DIR / "website_ui_detector" / "weights" / "best.pt"

    print(f"Best model saved at:")
    print(best_model)


if __name__ == "__main__":
    train_model()