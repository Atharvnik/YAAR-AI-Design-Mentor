from database.connection import get_connection


def test_database_connection():
    try:
        connection = get_connection()

        print("================================")
        print("PostgreSQL connection successful!")
        print("================================")

        connection.close()

    except Exception as e:
        print("PostgreSQL connection failed:")
        print(e)


if __name__ == "__main__":
    test_database_connection()