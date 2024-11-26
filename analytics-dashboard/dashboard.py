# import streamlit as st
# import requests

# # Set page title
# st.title("Streaming Service Analytics Dashboard")

# # Subscription Metrics
# st.header("Subscription Metrics")
# subscriptions = requests.get("http://localhost:5000/api/subscriptions").json()
# for sub in subscriptions:
#     st.write(f"{sub['subscription']}: {sub['user_count']} users")

# # Top Content
# st.header("Top-Rated Content")
# top_content = requests.get("http://localhost:5000/api/top-content").json()
# for content in top_content:
#     st.write(f"{content['title']} ({content['genre']}) - Rating: {content['rating']}")


import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Streaming Service Analytics Dashboard")

# Subscription Metrics
st.header("Subscription Metrics")
try:
    response = requests.get("http://localhost:5000/api/subscriptions")
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
    response = requests.get("http://localhost:5000/api/top-content")
    if response.status_code == 200:
        top_content = response.json()
        df_content = pd.DataFrame(top_content)
        if not df_content.empty:
            st.write("Table View of Top Content")
            st.table(df_content)

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

            # Add genre filter
            st.write("Filter by Genre")
            genre_filter = st.selectbox("Genre", options=df_content["genre"].unique())
            filtered_data = df_content[df_content["genre"] == genre_filter]
            if not filtered_data.empty:
                fig = px.bar(
                    filtered_data,
                    x="title",
                    y="rating",
                    title=f"Top Content in Genre: {genre_filter}",
                    labels={"title": "Title", "rating": "Rating"},
                    template="plotly"
                )
                st.plotly_chart(fig, use_container_width=True)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")