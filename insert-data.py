import os, json
import psycopg2

# Function to connect to the database
def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

# Insert data into a table and fetch IDs
def insert_and_fetch_ids(table_name, data, returning_column):
    connection = get_connection()
    cursor = connection.cursor()
    ids = []

    try:
        for row in data:
            columns = ", ".join(row.keys())
            placeholders = ", ".join(["%s"] * len(row))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING {returning_column}"
            cursor.execute(query, list(row.values()))
            ids.append(cursor.fetchone()[0])

        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return ids

# Main function to insert data and resolve dependencies
def load_data_from_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Insert subscriptions and fetch subscription_ids
    subscription_ids = insert_and_fetch_ids("subscriptions", data["subscriptions"], "subscription_id")

    # Update users data with actual subscription_ids
    for i, user in enumerate(data["users"]):
        user["subscription_id"] = subscription_ids[i % len(subscription_ids)]

    # Insert users and fetch user_ids
    user_ids = insert_and_fetch_ids("users", data["users"], "user_id")

    # Insert content and fetch content_ids
    content_ids = insert_and_fetch_ids("content", data["content"], "content_id")

    # Update watchhistory, reviews, and paymenthistory with actual user_ids and content_ids
    for watch in data["watchhistory"]:
        watch["user_id"] = user_ids[watch["user_id"] - 1]
        watch["content_id"] = content_ids[watch["content_id"] - 1]

    for review in data["reviews"]:
        review["user_id"] = user_ids[review["user_id"] - 1]
        review["content_id"] = content_ids[review["content_id"] - 1]

    for payment in data["paymenthistory"]:
        payment["user_id"] = user_ids[payment["user_id"] - 1]

    # Insert dependent data
    insert_and_fetch_ids("watchhistory", data["watchhistory"], "watch_id")
    insert_and_fetch_ids("reviews", data["reviews"], "review_id")
    insert_and_fetch_ids("paymenthistory", data["paymenthistory"], "payment_id")

# Call the function
json_file = "dataset.json"
load_data_from_json(json_file)
