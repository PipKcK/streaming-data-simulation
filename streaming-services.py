import os
import psycopg2

# Connection function
def get_connection():
    try:
        # Use DATABASE_URL from environment variables for secure connection
        return psycopg2.connect(os.environ["DATABASE_URL"])
    except KeyError:
        raise Exception("DATABASE_URL environment variable not set.")

def test_connection():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT now()")
        result = cursor.fetchone()
        print("Connection successful. Current time:", result)
    except Exception as e:
        print(f"Error testing connection: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Call the test function
test_connection()
