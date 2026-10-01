from fastapi import APIRouter
from database.connection import get_connection


router = APIRouter()


# =========================================================
# GET ALL REVIEWS
# =========================================================

@router.get("/reviews")
def get_reviews():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                filename,
                image_path,
                overall_score,
                summary,
                strengths,
                issues,
                accessibility,
                recommendations,
                yolo_results,
                ocr_results,
                clip_results,
                accessibility_results,
                created_at
            FROM ui_reviews
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        reviews = []

        for row in rows:
            reviews.append({
                "id": row[0],
                "filename": row[1],
                "image_path": row[2],
                "overall_score": row[3],
                "summary": row[4],
                "strengths": row[5],
                "issues": row[6],
                "accessibility": row[7],
                "recommendations": row[8],
                "yolo_results": row[9],
                "ocr_results": row[10],
                "clip_results": row[11],
                "accessibility_results": row[12],
                "created_at": row[13]
            })

        return {
            "count": len(reviews),
            "reviews": reviews
        }

    finally:
        cursor.close()
        connection.close()


# =========================================================
# GET SINGLE REVIEW
# =========================================================

@router.get("/reviews/{review_id}")
def get_review(review_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                filename,
                image_path,
                overall_score,
                summary,
                strengths,
                issues,
                accessibility,
                recommendations,
                yolo_results,
                ocr_results,
                clip_results,
                accessibility_results,
                created_at
            FROM ui_reviews
            WHERE id = %s
        """, (review_id,))

        row = cursor.fetchone()

        if row is None:
            return {
                "error": "Review not found"
            }

        return {
            "id": row[0],
            "filename": row[1],
            "image_path": row[2],
            "overall_score": row[3],
            "summary": row[4],
            "strengths": row[5],
            "issues": row[6],
            "accessibility": row[7],
            "recommendations": row[8],
            "yolo_results": row[9],
            "ocr_results": row[10],
            "clip_results": row[11],
            "accessibility_results": row[12],
            "created_at": row[13]
        }

    finally:
        cursor.close()
        connection.close()