from flask import Flask, jsonify, request
from db_connection import get_connection

app = Flask(__name__)

# Endpoint: Subscription Metrics
@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT s.name, COUNT(*) AS user_count
            FROM users u
            JOIN subscriptions s ON u.subscription_id = s.subscription_id
            GROUP BY s.name;
        """
        cursor.execute(query)
        result = [{"subscription": row[0], "user_count": row[1]} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

# Endpoint: Top Content
@app.route('/api/top-content', methods=['GET'])
def get_top_content():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT title, genre, rating FROM content ORDER BY rating DESC LIMIT 10;"
        cursor.execute(query)
        result = [{"title": row[0], "genre": row[1], "rating": row[2]} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
