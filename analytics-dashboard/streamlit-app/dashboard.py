import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Streaming Service Advanced Analytics Dashboard")

# Interactive date filters
st.sidebar.header("Revenue Timeline Filter (Aug 19 - Nov 28th) data")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Function to fetch data from API
def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return []

# Revenue Trends
st.header("Revenue Trends Over Time")
revenue_data = fetch_data("revenue-trends", {"start_date": start_date, "end_date": end_date})
if revenue_data:
    revenue_df = pd.DataFrame(revenue_data)
    fig = px.line(
        revenue_df,
        x="date",
        y="revenue",
        title="Revenue Trends",
        labels={"date": "Date", "revenue": "Revenue (USD)"},
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No revenue data available for the selected date range.")


# Subscription Metrics
st.header("Subscription Metrics")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/subscriptions")
    if response.status_code == 200:
        subscriptions = response.json()
        df = pd.DataFrame(subscriptions)
        if not df.empty:
            # Plot subscription metrics
            fig = px.bar(
                df,
                x="subscription",
                y="user_count",
                title="Subscription Metrics",
                labels={"subscription": "Subscription Plan", "user_count": "Number of Users"},
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch subscription metrics.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# Top Content
st.header("Top-Rated Content")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/top-content")
    if response.status_code == 200:
        top_content = response.json()
        df_content = pd.DataFrame(top_content)
        if not df_content.empty:
            # Add a rank column starting from 1
            df_content["Rank"] = range(1, len(df_content) + 1)

            # Display the table view with rankings
            st.write("Table View of Top Content (Ranked)")
            st.table(df_content[["Rank", "title", "rating", "genre"]])  # Customize columns as needed

            # Plot content ratings
            fig = px.bar(
                df_content,
                x="title",
                y="rating",
                title="Top Content Ratings",
                labels={"title": "Title", "rating": "Rating"},
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
            
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# ---------------------------------------
# Payment Trend Visualization
# ---------------------------------------
st.header("Revenue Trends Over Time")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/payments-trend")
    if response.status_code == 200:
        payments = response.json()
        df_payments = pd.DataFrame(payments)
        if not df_payments.empty:
            fig = px.line(
                df_payments,
                x="week",
                y="total_revenue",
                title="Weekly Revenue Trends",
                labels={"week": "Week", "total_revenue": "Total Revenue ($)"},
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch payment trends.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# ---------------------------------------
# Watch History by Genre Visualization
# ---------------------------------------
st.header("Watch History by Genre")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/watch-history-genre")
    if response.status_code == 200:
        genres = response.json()
        df_genres = pd.DataFrame(genres)
        if not df_genres.empty:
            fig = px.pie(
                df_genres,
                names="genre",
                values="watch_count",
                title="Watch History Distribution by Genre",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch watch history by genre.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# ---------------------------------------
# Popular Content Over Time Visualization
# ---------------------------------------
st.header("Popular Content Trends Over Time")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/popular-content-trend")
    if response.status_code == 200:
        popular_content = response.json()
        df_popular = pd.DataFrame(popular_content)
        if not df_popular.empty:
            # Convert month format to human-readable (e.g., "August")
            df_popular["month"] = pd.to_datetime(df_popular["month"]).dt.strftime("%B")

            # Add a simplified month filter
            st.write("Select a Month")
            month_filter = st.selectbox("Month", options=df_popular["month"].unique())
            filtered_content = df_popular[df_popular["month"] == month_filter]

            if not filtered_content.empty:
                # Sort by watch count and select the top 10
                top_10_content = filtered_content.nlargest(10, "watch_count")

                # Plot graph for top 10 popular content
                fig = px.bar(
                    top_10_content,
                    x="title",
                    y="watch_count",
                    title=f"Top 10 Popular Content in {month_filter}",
                    labels={"title": "Title", "watch_count": "Watch Count"},
                    template="plotly",
                    text="watch_count"
                )
                fig.update_traces(textposition="outside")  # Display values above bars
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write(f"No content data available for {month_filter}.")
    else:
        st.error("Failed to fetch popular content trends.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# ---------------------------------------
# Payment Method Distribution Visualization
# ---------------------------------------
st.header("Payment Method Distribution")
try:
    response = requests.get("https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/payment-method-distribution")
    if response.status_code == 200:
        payment_methods = response.json()
        df_methods = pd.DataFrame(payment_methods)
        if not df_methods.empty:
            fig = px.pie(
                df_methods,
                names="method",
                values="count",
                title="Payment Method Distribution",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch payment method distribution.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")

# ---------------------------------------
# User-Specific Stats Visualization
# ---------------------------------------
st.header("User-Specific Stats")

# Use text input to handle large user IDs
user_id_input = st.text_input("Enter User ID (e.g., 1024380905186918401)")

if user_id_input:
    try:
        # Validate that the input is a valid integer
        if not user_id_input.isdigit():
            st.error("Invalid User ID. Please enter a numeric value.")
        else:
            user_id = int(user_id_input)  # Convert to integer for API call
            response = requests.get(f"https://424vyr3g82.execute-api.us-east-1.amazonaws.com/api/user-stats/{user_id}")
            if response.status_code == 200:
                user_stats = response.json()

                # Display Watch History
                st.subheader("Watch History")
                if user_stats.get("watch_history"):
                    df_watch_history = pd.DataFrame(user_stats["watch_history"])
                    st.table(df_watch_history)
                else:
                    st.write("No watch history found for this user.")

                # Display Payment History
                st.subheader("Payment History")
                if user_stats.get("payment_history"):
                    df_payment_history = pd.DataFrame(user_stats["payment_history"])
                    st.table(df_payment_history)
                else:
                    st.write("No payment history found for this user.")
            else:
                st.error(f"Failed to fetch stats for User ID {user_id}.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")