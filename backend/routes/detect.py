from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from ultralytics import YOLO


router = APIRouter()


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------
# Trained YOLO model
# --------------------------------------------------

MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "website_ui_detector"
    / "weights"
    / "best.pt"
)


# Load model once when API starts
model = YOLO(str(MODEL_PATH))


# --------------------------------------------------
# YOLO Detection API
# --------------------------------------------------

@router.post("/detect")
async def detect_ui(file: UploadFile = File(...)):

    # --------------------------------------------------
    # 1. Save uploaded image
    # --------------------------------------------------

    upload_dir = (
        PROJECT_ROOT
        / "backend"
        / "uploads"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    image_path = upload_dir / file.filename

    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())


    # --------------------------------------------------
    # 2. Annotated image folder
    # --------------------------------------------------

    annotated_dir = (
        PROJECT_ROOT
        / "backend"
        / "uploads"
        / "annotated"
        / "results"
    )

    annotated_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------
    # 3. Run YOLO detection
    # --------------------------------------------------

    results = model.predict(
        source=str(image_path),
        conf=0.25,
        verbose=False,
        save=False
    )


    detections = []


    # --------------------------------------------------
    # 4. Extract detections + save annotation
    # --------------------------------------------------

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class": str(model.names[class_id]),
                "confidence": round(confidence, 4),
                "bbox": {
                    "x1": round(float(x1), 2),
                    "y1": round(float(y1), 2),
                    "x2": round(float(x2), 2),
                    "y2": round(float(y2), 2)
                }
            })


        # --------------------------------------------------
        # Save YOLO annotated image
        # --------------------------------------------------

        annotated_image = annotated_dir / file.filename

        result.save(
            filename=str(annotated_image)
        )


    # --------------------------------------------------
    # 5. Return API response
    # --------------------------------------------------

    return {
        "filename": file.filename,
        "detections": detections,
        "count": len(detections),
        "annotated_image": str(annotated_image)
    }