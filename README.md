# **Streaming Data Simulation**

This repository contains a simulation project for a media streaming platform. It demonstrates the implementation of a backend system to manage subscriptions, users, content, watch history, reviews, and payment processing. The project is designed to simulate real-world streaming services and provides an extensible framework for similar applications. The project has been extended to include a **Flask API layer** and a **Streamlit dashboard** for analytics, adding complexity and showcasing practical use cases of distributed systems.

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Test Data](#test-data)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## **Overview**

This project simulates the core backend operations of a streaming service. It includes functionalities for:
- Managing user subscriptions and profiles.
- Storing and querying content metadata (movies, series, etc.).
- Tracking user activity, such as watch history and reviews.
- Handling payment transactions for subscription plans.

The project utilizes **CockroachDB**, a distributed SQL database, for scalable and resilient data storage.

---

## **Features**

- **Subscriptions Management**: Support for multiple subscription tiers with unique features and pricing.
- **User Management**: CRUD operations for users and their relationships with subscriptions.
- **Content Metadata**: Track movies, series, genres, and ratings.
- **Watch History**: Log user progress for watched content.
- **Reviews**: Allow users to rate and review content.
- **Payments**: Process and store subscription payment history.

---

## **Getting Started**

### **Prerequisites**
1. **CockroachDB Cluster**:
   - Set up a CockroachDB cluster (local or cloud) and obtain the connection string.
   - Ensure your cluster has SSL certificates if running in secure mode.

2. **Python**:
   - Install Python 3.8 or higher.

3. **Dependencies**:
   - Install required Python packages using:
     ```bash
     pip install -r requirements.txt
     ```

---

### **Setup Instructions**
1. Clone the repository:
   ```bash
   git clone https://github.com/PipKcK/streaming-data-simulation.git
   cd streaming-data-simulation
   ```
2. Configure Your Environment
  Export the DATABASE_URL environment variable with your CockroachDB connection string:
  ```bash
  export DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<database>?sslmode=verify-full"
  ```
3. Initialize the database:
  Create the database schema by running:
  ```bash
  python streaming-services.py
  ```
4. Insert test data:
  Populate the database with sample test data:
  ```bash
  python insert-data.py
  ```
5. Run the Flask API server:
  Start the Flask API server:
  ```bash
  python app.py
  ```
6. Launch the Streamlit dashboard:
  Open the dashboard in your browser:
  ```bash
  streamlit run dashboard.py
  ```

---

## **Database Schema**

The project follows a relational database design. Below are the core tables and their purposes:

- **Subscriptions**: Tracks subscription plans and features.
- **Users**: Stores user information and their associated subscription.
- **Content**: Holds metadata about movies, series, and other media.
- **WatchHistory**: Logs user progress on watched content.
- **Reviews**: Allows users to leave ratings and reviews.
- **PaymentHistory**: Records user payments for subscription plans.

---

## **Test Data**

Sample test data is provided in `test_data.json` to populate the database. It includes:
- **4 Subscription Plans**
- **10 Users**
- **4 Content Items**
- **Watch History**, **Reviews**, and **Payment History** for the users.

---

## **Usage**

### **Run Scripts**
- **Initialize Schema**: Run streaming-services.py to create all necessary tables.
- **Insert Data**: Use insert-data.py to populate the database with sample data.
- **Query the Database**: Open a SQL shell to interact with the database:
  - ```bash
    cockroach sql --url $DATABASE_URL
    ```

---

## **Interact with the API**

- **The Flask API exposes RESTful endpoints for querying analytics and operational data.**
  Example:
  - GET /api/subscriptions: Fetch subscription metrics.
  - GET /api/top-content: Fetch top-rated content.

---

## **Dashboard Features**

- **Subscription Metrics**:
    - Visualize the number of users for each subscription tier using bar charts.
- **Top-Rated Content**:
    - Display content ratings and genres using tables and scatter plots.
- **Interactive Filters**:
    - Filter content by genre or rating thresholds dynamically.

---


## **Future Enhancements**

- **Advanced Analytics**:
    - Add time-series visualizations for user activity and revenue trends.
- **User Authentication**:
    - Secure the API endpoints with authentication mechanisms.
- **Cloud Deployment**:
    - Deploy the dashboard and API using platforms like AWS, Heroku, or Streamlit Cloud.
- **Recommendation System**:
    - Build personalized recommendations based on user activity.
---

## **Contributors**

- **Sai Deeduvanu** - [GitHub Profile](https://github.com/Sai-Krishna7)

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
