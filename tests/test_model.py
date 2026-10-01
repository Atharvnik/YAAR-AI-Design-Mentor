from ultralytics import YOLO
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "website_ui_detector"
    / "weights"
    / "best.pt"
)

TEST_IMAGES = PROJECT_ROOT / "dataset" / "test" / "images"

OUTPUT_DIR = PROJECT_ROOT / "backend" / "models" / "predictions"


def test_model():
    print("Loading trained model...")
    print(f"Model: {MODEL_PATH}")

    model = YOLO(str(MODEL_PATH))

    print("\nRunning detection on test images...")

    model.predict(
        source=str(TEST_IMAGES),
        conf=0.25,
        save=True,
        project=str(OUTPUT_DIR),
        name="test_results",
        exist_ok=True
    )

    print("\nDetection completed!")
    print(f"Results saved in: {OUTPUT_DIR / 'test_results'}")


if __name__ == "__main__":
    test_model()