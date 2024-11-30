from flask import Flask, jsonify, request
import awsgi
from db_connection import get_connection
from flask_cors import CORS
import logging

app = Flask(__name__)

CORS(app)

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Endpoint: Revenue Trends
@app.route('/api/revenue-trends', methods=['GET'])
def get_revenue_trends():
    try:
        start_date = request.args.get('start_date', '2024-09-01')
        end_date = request.args.get('end_date', '2024-09-30')

        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT DATE(p.payment_date) AS date, SUM(p.amount) AS revenue
            FROM paymenthistory p
            WHERE DATE(p.payment_date) BETWEEN %s AND %s
            GROUP BY DATE(p.payment_date)
            ORDER BY DATE(p.payment_date);
        """
        cursor.execute(query, (start_date, end_date))
        result = [{"date": str(row[0]), "revenue": float(row[1])} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

# Other Advanced Endpoints (Payments Trend, Watch History by Genre, etc.)
@app.route('/api/payments-trend', methods=['GET'])
def get_payments_trend():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT DATE_TRUNC('week', payment_date) AS week, SUM(amount) AS total_revenue
            FROM paymenthistory
            GROUP BY DATE_TRUNC('week', payment_date)
            ORDER BY week;
        """
        cursor.execute(query)
        result = [{"week": row[0], "total_revenue": float(row[1])} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/watch-history-genre', methods=['GET'])
def get_watch_history_genre():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT c.genre, COUNT(*) AS watch_count
            FROM watchhistory w
            JOIN content c ON w.content_id = c.content_id
            GROUP BY c.genre
            ORDER BY watch_count DESC;
        """
        cursor.execute(query)
        result = [{"genre": row[0], "watch_count": row[1]} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/user-stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        watch_query = """
            SELECT c.title, w.progress, w.watched_on
            FROM watchhistory w
            JOIN content c ON w.content_id = c.content_id
            WHERE w.user_id = %s
            ORDER BY w.watched_on DESC;
        """
        cursor.execute(watch_query, (user_id,))
        watch_history = [{"title": row[0], "progress": float(row[1]), "watched_on": row[2]} for row in cursor.fetchall()]

        payment_query = """
            SELECT amount, method, payment_date
            FROM paymenthistory
            WHERE user_id = %s
            ORDER BY payment_date DESC;
        """
        cursor.execute(payment_query, (user_id,))
        payment_history = [{"amount": float(row[0]), "method": row[1], "payment_date": row[2]} for row in cursor.fetchall()]

        result = {
            "user_id": user_id,
            "watch_history": watch_history,
            "payment_history": payment_history
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

# 4. Popular Content Over Time
@app.route('/api/popular-content-trend', methods=['GET'])
def get_popular_content_trend():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT DATE_TRUNC('month', w.watched_on) AS month, c.title, COUNT(*) AS watch_count
            FROM watchhistory w
            JOIN content c ON w.content_id = c.content_id
            GROUP BY DATE_TRUNC('month', w.watched_on), c.title
            ORDER BY month, watch_count DESC;
        """
        cursor.execute(query)
        result = [{"month": row[0], "title": row[1], "watch_count": row[2]} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

# Add Payment Method Distribution Endpoint
@app.route('/api/payment-method-distribution', methods=['GET'])
def get_payment_method_distribution():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            SELECT method, COUNT(*) AS count
            FROM paymenthistory
            GROUP BY method
            ORDER BY count DESC;
        """
        cursor.execute(query)
        result = [{"method": row[0], "count": row[1]} for row in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if connection:
            cursor.close()
            connection.close()

# AWS Lambda Handler
def lambda_handler(event, context):
    try:
        # Log the received event for debugging
        print("Received event:", event)

        # Determine the HTTP method and path based on the event structure
        if "httpMethod" in event:  # REST API (v1)
            http_method = event["httpMethod"]
            event["path"] = event["path"]
        elif "requestContext" in event and "http" in event["requestContext"]:  # HTTP API (v2)
            http_method = event["requestContext"]["http"]["method"]
            event["httpMethod"] = http_method  # Add to event for compatibility
            event["path"] = event["rawPath"]  # Add to event for compatibility

            # Handle query parameters for HTTP API (v2)
            if "rawQueryString" in event and event["rawQueryString"]:
                event["queryStringParameters"] = {
                    key: value for key, value in 
                    (pair.split("=") for pair in event["rawQueryString"].split("&"))
                }
            else:
                event["queryStringParameters"] = {}

        # Ensure required keys are present in the event
        if "httpMethod" not in event or "path" not in event:
            raise KeyError("The required keys 'httpMethod' or 'path' are missing in the event.")

        # Process the event with awsgi
        return awsgi.response(app, event, context)
    except KeyError as e:
        print(f"KeyError in lambda_handler: {e}")
        return {
            "statusCode": 400,
            "body": f"Bad Request: {str(e)}",
        }
    except Exception as e:
        print(f"Exception in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": f"Internal Server Error: {str(e)}",
        }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
