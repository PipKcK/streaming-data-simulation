# **Streaming Data Simulation**

This repository contains a simulation project for a media streaming platform. It demonstrates the implementation of a backend system to manage subscriptions, users, content, watch history, reviews, and payment processing. The project is designed to simulate real-world streaming services and provides an extensible framework for similar applications. The project has been extended to include a **Flask API layer** and a **Streamlit dashboard** for analytics, adding complexity and showcasing practical use cases of distributed systems.

## **Table of Contents**
- [Architecture Diagram](#architecture-diagram)
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Test Data](#test-data)
- [Usage](#usage)
- [Backend API Endpoints](#backend-api-endpoints)
- [Latest Advancements](#latest-advancements)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## **Architecture Diagram**
![architecture-diagram](https://github.com/user-attachments/assets/64d00630-74ca-488a-9d13-3d5eceeb68de)

---

## **Overview**

This project simulates the core backend operations of a streaming service. It includes functionalities for:
- Managing user subscriptions and profiles.
- Storing and querying content metadata (movies, series, etc.).
- Tracking user activity, such as watch history and reviews.
- Handling payment transactions for subscription plans.

The project utilizes **CockroachDB**, a distributed SQL database, for scalable and resilient data storage.

---

## Tech Stack

- **Frontend:** Streamlit, Plotly
- **Backend:** Flask, AWS Lambda, AWS API Gateway
- **Database:** CockroachDB
- **Hosting:**
  - **Frontend:** Streamlit Cloud
  - **Backend:** AWS Lambda, API Gateway
- **Python Libraries:** Flask, psycopg2-binary, aws-wsgi, flask-cors

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
  - Export the DATABASE_URL environment variable with your CockroachDB connection string:
    ```bash
    export DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<database>?sslmode=verify-full"
    ```
3. Connect to the Cockroach Cluster:
    ```bash
    cd analytics-dashboard
    python db_connection.py 
    ```
4. Run the Flask API server:
  - Start the Flask API server:
    ```bash
    python app.py
    ```
5. Launch the Streamlit dashboard:
  - Open the dashboard in your browser:
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

Sample test data is provided in mock_data folder using mockaroo and the upload_data.py script to populate the database. It includes:
- **4 Subscription Plans**
- **100 Users**
- **100 Content Items**
- **Watch History**, **Reviews**, and **Payment History** for the users.

---

## **Usage**

### **Run Scripts**
- **Intiialize Environment variable**: Export DATABASE_URL with the connection strig for the cockroach cluster.
- **Install Package Requirments & Run the API Layer**: Install necessary packages using the requirments.txt file in the analytics-dashboard folder and start the Flask server & the Streamlit Dashboard.
- **Query the Database**: Open a SQL shell to interact with the database:
  - ```bash
    cockroach sql --url $DATABASE_URL
    ```

### Access the Web App
The analytics dashboard is accessible via its **Streamlit Cloud** URL:

```plaintext
https://analytics-dash.streamlit.app/
```

---

## **Backend API Endpoints**

- **The Flask API is exposed through AWS API Gateway and serves as the backend for the dashboard. Below are the key endpoints**:
   | **Endpoint**                       | **Method** | **Description**                              |
   |------------------------------------|------------|----------------------------------------------|
   | `/api/subscriptions`               | `GET`      | Fetch subscription metrics.                  |
   | `/api/top-content`                 | `GET`      | Fetch top-rated content.                     |
   | `/api/revenue-trends`              | `GET`      | Fetch revenue trends.                        |
   | `/api/payments-trend`              | `GET`      | Get payment trends (weekly).                 |
   | `/api/watch-history-genre`         | `GET`      | Fetch watch history grouped by genre.        |
   | `/api/user-stats/<int:user_id>`    | `GET`      | Fetch user-specific stats.                   |
   | `/api/popular-content-trend`       | `GET`      | Fetch popular content over time.             |
   | `/api/payment-method-distribution` | `GET`      | Fetch payment method distribution.           |

---

## Latest Advancements

### Deployment of Streamlit App to Streamlit Cloud
The frontend web application for the analytics dashboard is built using **Streamlit** and has been successfully deployed to **Streamlit Cloud**, making it publicly accessible. This allows stakeholders to interact with live analytics directly through a web browser.

#### Steps:
1. The Streamlit app is hosted in a private GitHub repository.
2. It was deployed to Streamlit Cloud by connecting the GitHub repository and selecting the `main` branch.

#### Key Features:
- Interactive visualizations using Plotly.
- CORS configuration for API calls to ensure seamless integration with the backend.

---

### Deployment of Flask API to AWS Lambda
The Flask-based backend API layer has been packaged and deployed to **AWS Lambda** using a ZIP file. It is exposed via **AWS API Gateway** to allow the frontend to fetch data from the CockroachDB cluster dynamically.

#### Steps:

#### Packaging and Uploading:
1. The Flask app and its dependencies (`flask`, `psycopg2-binary`, `aws-wsgi`) were packaged into a ZIP file.
2. The ZIP file was uploaded to AWS Lambda as the runtime environment.

#### AWS Lambda:
1. The Flask app was adapted to use **AWS WSGI** (`awsgi`) for Lambda compatibility.
2. Lambda was configured with the necessary environment variables, including the database connection string and SSL certificate.

#### API Gateway:
1. Routes were defined for each endpoint (e.g., `/api/subscriptions`, `/api/revenue-trends`).
2. Integrated with Lambda to process requests and responses.

#### Database Connection:
- Flask API securely connects to **CockroachDB** using `psycopg2` and an **SSL certificate**.

#### Security and Scalability:
- **CORS settings** were added to the API Gateway to allow cross-origin requests.
- Lambda ensures **scalable** and **cost-efficient** operation.

---

## **Future Enhancements**

- **User Authentication**:
    - Secure the API endpoints with authentication mechanisms.
- **Recommendation System**:
    - Build personalized recommendations based on user activity.

---

## **Contributors**

- **Sai Deeduvanu** - [GitHub Profile](https://github.com/Sai-Krishna7)

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
