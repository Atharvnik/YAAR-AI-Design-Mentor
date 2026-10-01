from database.connection import get_connection
import json


class DatabaseError(Exception):
    """Raised when a review cannot be saved to PostgreSQL."""


def save_ui_review(result):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO ui_reviews (
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
                accessibility_results
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
            """,
            (
                result.get("filename"),
                result.get("image_path"),
                result.get("overall_score"),
                result.get("summary"),
                json.dumps(result.get("strengths", [])),
                json.dumps(result.get("issues", [])),
                json.dumps(result.get("accessibility", {})),
                json.dumps(result.get("recommendations", [])),
                json.dumps(result.get("yolo", {})),
                json.dumps(result.get("ocr", {})),
                json.dumps(result.get("clip", {})),
                json.dumps(result.get("accessibility", {}))
            )
        )

        review_id = cursor.fetchone()[0]
        connection.commit()

        return review_id

    except Exception as error:
        if connection is not None:
            connection.rollback()
        raise DatabaseError("Unable to save UI review") from error

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()