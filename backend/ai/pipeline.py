from pathlib import Path

from backend.ai.yolo_detector import detect_objects
from backend.utils.ocr import extract_text
from backend.ai.clip_analyzer import analyze_image
from backend.ai.accessibility import analyze_accessibility
from backend.ai.result_merger import merge_results
from backend.ai.gemini_reviewer import review_ui
from database.repository import save_ui_review


def analyze_ui(image_path: Path, run_gemini=False):
    """
    Run the complete YAAR AI Design Mentor analysis pipeline.

    Pipeline:
        YOLO → OCR → CLIP → Accessibility
        → Result Merger → Gemini → PostgreSQL
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    print("\n==============================")
    print("YAAR AI DESIGN MENTOR PIPELINE")
    print("==============================")

    # ---------------------------------
    # 1. YOLO
    # ---------------------------------

    print("\n[1/5] Running YOLO detection...")

    yolo_results = detect_objects(image_path)

    print(
        f"YOLO detected "
        f"{len(yolo_results)} elements."
    )

    # ---------------------------------
    # 2. OCR
    # ---------------------------------

    print("\n[2/5] Running EasyOCR...")

    ocr_results = extract_text(image_path)

    print(
        f"OCR detected "
        f"{len(ocr_results)} text regions."
    )

    # ---------------------------------
    # 3. CLIP
    # ---------------------------------

    print("\n[3/5] Running CLIP analysis...")

    clip_results = analyze_image(image_path)

    print("CLIP analysis completed.")

    # ---------------------------------
    # 4. Accessibility
    # ---------------------------------

    print("\n[4/5] Running accessibility analysis...")

    accessibility_results = analyze_accessibility(
        image_path=image_path,
        yolo_detections=yolo_results,
        ocr_results=ocr_results
    )

    print(
        "Accessibility score:",
        accessibility_results["accessibility_score"]
    )

    # ---------------------------------
    # 5. Merge results
    # ---------------------------------

    print("\n[5/5] Merging analysis results...")

    merged_result = merge_results(
        image_path=image_path,
        yolo_detections=yolo_results,
        ocr_results=ocr_results,
        clip_results=clip_results,
        accessibility_results=accessibility_results
    )

    print("Result merger completed.")

    # ---------------------------------
    # Gemini UI/UX review
    # ---------------------------------

    gemini_review = None
    gemini_error = False

    if run_gemini:

        print("\nRunning Gemini UI/UX review...")

        try:

            gemini_review = review_ui(
                merged_result
            )

            print("Gemini review completed.")

            print(
                "Gemini overall score:",
                gemini_review["overall_score"]
            )

        except Exception as error:

            print("\n================================")
            print("GEMINI REVIEW FAILED")
            print("================================")

            print(error)

            print(
                "\nContinuing with YOLO/OCR/CLIP/"
                "Accessibility results..."
            )

            gemini_review = None
            gemini_error = True

    # ---------------------------------
    # Prepare PostgreSQL data
    # ---------------------------------

    print("\nPreparing review for PostgreSQL...")

    review_data = {
        "filename": image_path.name,

        "image_path": str(image_path),

        # ---------------------------------
        # Gemini review fields
        # ---------------------------------

        "overall_score": (
            gemini_review.get("overall_score")
            if gemini_review
            else None
        ),

        "summary": (
            gemini_review.get("summary")
            if gemini_review
            else None
        ),

        "strengths": (
            gemini_review.get("strengths", [])
            if gemini_review
            else []
        ),

        "issues": (
            gemini_review.get("issues", [])
            if gemini_review
            else []
        ),

        "recommendations": (
            gemini_review.get("recommendations", [])
            if gemini_review
            else []
        ),

        # ---------------------------------
        # Accessibility
        # ---------------------------------

        "accessibility": merged_result.get(
            "accessibility",
            {}
        ),

        # ---------------------------------
        # Multimodal analysis results
        # ---------------------------------

        "yolo": merged_result.get(
            "yolo",
            {}
        ),

        "ocr": merged_result.get(
            "ocr",
            {}
        ),

        "clip": merged_result.get(
            "clip",
            {}
        )
    }

    # ---------------------------------
    # Save to PostgreSQL
    # ---------------------------------

    print("\nSaving review to PostgreSQL...")

    review_id = save_ui_review(
        review_data
    )

    print(
        f"Review saved successfully. "
        f"Review ID: {review_id}"
    )

    # ---------------------------------
    # Final result
    # ---------------------------------

    return {
        "image": str(image_path),

        "analysis": merged_result,

        "gemini_review": gemini_review,

        "gemini_error": gemini_error,

        "review_id": review_id
    }