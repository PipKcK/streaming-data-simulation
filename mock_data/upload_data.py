import json, os
import psycopg2

# Function to connect to the database
def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

# ----------------------------Function to upload watchhistory data---------------------------------
def upload_watchhistory(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Connect to the database
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Fetch all user_ids from the users table
        cursor.execute("SELECT user_id FROM users ORDER BY user_id ASC")
        user_ids = [row[0] for row in cursor.fetchall()]

        # Fetch all content_ids from the content table
        cursor.execute("SELECT content_id FROM content ORDER BY content_id ASC")
        content_ids = [row[0] for row in cursor.fetchall()]

        # Resolve user_id and content_id relationships in watchhistory mock data
        for watch in data["watchhistory"]:
            user_index = watch["user_id"] - 1  # Adjusting for 0-based index
            content_index = watch["content_id"] - 1  # Adjusting for 0-based index

            if user_index < len(user_ids) and content_index < len(content_ids):
                watch["user_id"] = user_ids[user_index]
                watch["content_id"] = content_ids[content_index]
            else:
                raise IndexError(
                    f"User ID {watch['user_id']} or Content ID {watch['content_id']} in mock data exceeds the number of users or content in the database."
                )

        # Insert watchhistory data into the database
        for watch in data["watchhistory"]:
            cursor.execute("""
                INSERT INTO watchhistory (user_id, content_id, watched_on, progress)
                VALUES (%s, %s, %s, %s)
            """, (watch["user_id"], watch["content_id"], watch["watched_on"], watch["progress"]))

        # Commit the transaction
        connection.commit()
        print("Watch history data uploaded successfully!")
    except (Exception, psycopg2.Error) as error:
        print(f"Error uploading watch history data: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Call the function
json_file = "watchhistory_mock_data2.json"  # Replace with the correct JSON file path
upload_watchhistory(json_file)

# # ------------------------Insert data into the `paymenthistory` table---------------------------
# def upload_paymenthistory(json_file):
#     with open(json_file, "r") as file:
#         data = json.load(file)

#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         # Fetch all user_ids from the database
#         cursor.execute("SELECT user_id FROM users ORDER BY user_id ASC")
#         user_ids = [row[0] for row in cursor.fetchall()]

#         # Update user_ids in the mock data to match actual user_ids in the database
#         for payment in data["paymenthistory"]:
#             payment["user_id"] = user_ids[payment["user_id"] - 1]  # Adjust for 0-based indexing

#         # Insert new paymenthistory data
#         for payment in data["paymenthistory"]:
#             cursor.execute("""
#                 INSERT INTO paymenthistory (user_id, amount, payment_date, method)
#                 VALUES (%s, %s, %s, %s)
#             """, (payment["user_id"], payment["amount"], payment["payment_date"], payment["method"]))

#         connection.commit()
#         print("Payment history data uploaded successfully!")
#     except Exception as e:
#         print(f"Error uploading payment history data: {e}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# # Call the function
# upload_paymenthistory("paymenthistory_mock_data2.json")


# # ---------------------------Function to upload reviews data-------------------------------------
# def upload_reviews(json_file):
#     with open(json_file, "r") as file:
#         data = json.load(file)

#     # Connect to the database
#     connection = get_connection()
#     cursor = connection.cursor()

#     try:
#         # Fetch all user_ids from the users table
#         cursor.execute("SELECT user_id FROM users ORDER BY user_id ASC")
#         user_ids = [row[0] for row in cursor.fetchall()]

#         # Fetch all content_ids from the content table
#         cursor.execute("SELECT content_id FROM content ORDER BY content_id ASC")
#         content_ids = [row[0] for row in cursor.fetchall()]

#         # Resolve user_id and content_id relationships in reviews mock data
#         for review in data["reviews"]:
#             user_index = review["user_id"] - 1  # Adjusting for 0-based index
#             content_index = review["content_id"] - 1  # Adjusting for 0-based index

#             if user_index < len(user_ids) and content_index < len(content_ids):
#                 review["user_id"] = user_ids[user_index]
#                 review["content_id"] = content_ids[content_index]
#             else:
#                 raise IndexError(
#                     f"User ID {review['user_id']} or Content ID {review['content_id']} in mock data exceeds the number of users or content in the database."
#                 )

#         # Insert reviews data into the database
#         for review in data["reviews"]:
#             cursor.execute("""
#                 INSERT INTO reviews (user_id, content_id, rating, review_text)
#                 VALUES (%s, %s, %s, %s)
#             """, (review["user_id"], review["content_id"], review["rating"], review["review_text"]))

#         # Commit the transaction
#         connection.commit()
#         print("Reviews data uploaded successfully!")
#     except (Exception, psycopg2.Error) as error:
#         print(f"Error uploading reviews data: {error}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# # Call the function
# json_file = "reviews_mock_data.json"  # Replace with the correct JSON file path
# upload_reviews(json_file)
