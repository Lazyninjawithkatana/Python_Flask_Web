# Secure Flask Dashboard Application

A simple, secure web application built with Python Flask and PostgreSQL, featuring user registration, login, and a dynamic user dashboard. This project emphasizes clean code, secure password handling, and effective use of templating and database connectivity.

## 🚀 Features

* **User Authentication:** Secure user registration and login implemented using Flask, sessions, and `werkzeug.security` for password hashing (`generate_password_hash` and `check_password_hash`).
* **PostgreSQL Integration:** Uses the `psycopg2` library for robust and secure connectivity with a PostgreSQL database, managing user data (username, email, password hash).
* **Session Management:** State is maintained using Flask sessions to track logged-in users and display user-specific data (`user_name`, `user_email`).
* **Flash Messaging:** Implements dynamic flash messages to provide user feedback (e.g., success messages after registration, error messages during login) using Jinja2 templating.
* **Responsive UI:** A clean, modern, and visually appealing user interface for both the login/registration page and the dashboard, styled with CSS (including animations and a card-based layout).

## 🛠️ Technology Stack

* **Backend Framework:** Python 3 + Flask
* **Database:** PostgreSQL (with `psycopg2`)
* **Security:** `werkzeug.security` (for strong password hashing)
* **Templating:** Jinja2
* **Frontend:** HTML5, CSS3

## ⚙️ Setup and Installation

### Prerequisites

1.  **Python 3:** Ensure you have Python 3 installed.
2.  **PostgreSQL:** Ensure a PostgreSQL server is running locally or remotely.
3.  **Required Libraries:** Install the necessary Python packages:
    ```bash
    pip install Flask psycopg2-binary werkzeug
    ```

### Configuration

1.  **Database Constants:** Open `database_const.py` and set your PostgreSQL connection details:
    ```python
    HOST = 'localhost' # Your database host
    USER = 'postgres'  # Your PostgreSQL username
    PASSWORD = 'your_password' # Your PostgreSQL password
    DATABASE = 'postgres' # Initial database to connect to (usually 'postgres')
    NEW_DB_NAME = 'webproject' # The new database name to be created
    ```

2.  **Database Initialization:** Run the script to create the database and the `users` table:
    ```bash
    python main_database.py
    ```

### Running the Application

1.  **Start Flask Server:** Run the main application file:
    ```bash
    python app.py
    ```
2.  **Access:** Open your browser and navigate to the address shown in the terminal (usually `http://127.0.0.0.1:5000/` or `http://localhost:5000/`).

## 🗺️ Project Structure