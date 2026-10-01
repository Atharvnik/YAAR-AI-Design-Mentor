import logging
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.ai.pipeline import analyze_ui
from database.repository import DatabaseError


router = APIRouter()

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg"}


def has_valid_image_signature(contents):
    return (
        contents.startswith(b"\x89PNG\r\n\x1a\n")
        or contents.startswith(b"\xff\xd8\xff")
    )


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@router.post("/review")
async def review_ui(file: UploadFile = File(...)):

    raw_filename = file.filename or ""
    safe_filename = Path(raw_filename).name

    if not safe_filename or safe_filename != raw_filename:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_image",
                "message": "Please upload a PNG, JPG, or JPEG image with a safe filename."
            }
        )

    if Path(safe_filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_image",
                "message": "Please upload a PNG, JPG, or JPEG image."
            }
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_image",
                "message": "The uploaded file is not a supported image type."
            }
        )

    contents = await file.read(MAX_FILE_SIZE + 1)

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail={
                "code": "file_too_large",
                "message": "Please upload an image smaller than 10 MB."
            }
        )

    if not has_valid_image_signature(contents):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_image",
                "message": "The uploaded file is not a valid PNG or JPEG image."
            }
        )

    # -----------------------------
    # Save uploaded image
    # -----------------------------

    upload_dir = PROJECT_ROOT / "backend" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    image_path = upload_dir / safe_filename

    with open(image_path, "wb") as buffer:
        buffer.write(contents)

    # -----------------------------
    # Run complete AI pipeline
    # -----------------------------

    try:
        result = analyze_ui(
            image_path,
            run_gemini=True
        )
    except DatabaseError as error:
        logger.exception("Database failure while saving review")
        raise HTTPException(
            status_code=503,
            detail={
                "code": "database_error",
                "message": "We couldn't save your review. Please try again."
            }
        ) from error
    except Exception as error:
        logger.exception("Review analysis failed")
        raise HTTPException(
            status_code=500,
            detail={
                "code": "analysis_error",
                "message": "We couldn't complete the design analysis. Please try again."
            }
        ) from error

    # -----------------------------
    # Return result
    # -----------------------------

    return {
        "filename": safe_filename,
        "result": result
    }