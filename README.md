# **Streaming Data Simulation**

This repository contains a simulation project for a media streaming platform. It demonstrates the implementation of a backend system to manage subscriptions, users, content, watch history, reviews, and payment processing. The project is designed to simulate real-world streaming services and provides an extensible framework for similar applications.

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

## **Project Structure**
```bash
streaming-data-simulation/
│
├── streaming-services.py   # Core script defining the backend services
├── insert-data.py          # Script to insert test data into the database
├── test_data.json          # Sample test dataset
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── .gitignore              # Ignored files and directories
```
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

## **Example Queries**

- **Retrieve all users and their subscriptions**:
  ```sql
  SELECT u.name, u.email, s.name AS subscription
  FROM users u
  JOIN subscriptions s ON u.subscription_id = s.subscription_id;
  ```

- **List all reviews for a specific content item**:
  ```sql
  SELECT r.review_text, r.rating, u.name AS user
  FROM reviews r
  JOIN users u ON r.user_id = u.user_id
  WHERE r.content_id = 1;
  ```

  ---

## **Future Enhancements**
- **API Integration**: Add RESTful APIs using Flask or FastAPI to expose endpoints for data access.
- **Authentication**: Implement user authentication and authorization mechanisms.
- **Data Visualization**: Create dashboards for insights like popular content, top users, or revenue.
- **Recommendation System**: Build a content recommendation system based on user preferences.

---

## **Contributors**

- **Sai Deeduvanu** - [GitHub Profile](https://github.com/Sai-Krishna7)

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
