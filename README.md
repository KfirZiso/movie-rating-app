# Movie Rating Prediction App 🎬

This project is a web-based application built with Flask that predicts movie ratings using a trained Machine Learning model. The application features a user-friendly frontend with input validation, dynamic error handling (including custom templates for HTTP 400 and HTTP 500 errors), and a robust backend integration.

## Authors & Team Members 👥
* **Kfir Ziso 322883091**
* **Yael Bukris 324050138**

---

## 1. Project Description 📝
The application provides an interface for users to input various characteristics of a movie (such as release year, runtime, and number of A-list actors) and get an instant predicted rating based on an advanced regression pipeline.
* **Backend:** Flask API (`api.py`) that handles JSON payloads, performs data preprocessing, and serves model predictions using a Scikit-Learn pipeline.
* **Frontend:** Interactive HTML webpage (`templates/index.html`) featuring real-time input fields, checkbox selections for genres, and asynchronous AJAX requests with beautiful CSS status indicators.

---

## 2. Installation Instructions 🛠️

To set up and run this project locally, you need to create an isolated Python virtual environment using Anaconda and install the necessary dependencies.

### Step 1: Clone or Open the Project Directory
Open your **Anaconda Prompt** and navigate to the project directory:
cd "path/to/your/movie-rating-app"

### Step 2: Create a Virtual Environment
Create a new virtual environment named `movie_env` with Python 3.11:
conda create --name movie_env python=3.11 -y

### Step 3: Activate the Environment
Activate the newly created environment:
conda activate movie_env

### Step 4: Install Dependencies from `requirements.txt`
Install all required libraries (Flask, Pandas, NumPy, Scikit-Learn v1.6.1, and Cloudpickle) using the provided requirements file:
pip install -r requirements.txt

---

## 3. How to Run the Server 🚀

Once the installation is complete and your environment is active, you can launch the Flask web server by running the following command:

python api.py

Upon successful startup, the terminal will display that the server is active and listening for local requests.

---

## 4. Application Access URL 🌐

Once the server is running, open your preferred web browser (e.g., Google Chrome) and navigate to the following address:

👉 http://localhost:5000

---

## 5. Input Fields & Expected Value Ranges 📊

The model expects the following input fields via the UI form. The frontend and backend validate these inputs to ensure proper data ranges before processing:

| Field Name | Data Type | Expected Range / Options | Description |
| :--- | :--- | :--- | :--- |
| **Runtime (Minutes)** | Integer | `1 - 500` | Total duration of the movie in minutes. |
| **A-List Actors** | Integer | `0 - 20` | Number of top-tier (A-list) actors in the main cast. |
| **Is Post IMDb?** | Select / Binary | `Yes (1) / No (0)` | Indicates if the movie was produced after the launch of IMDb. |
| **Is English?** | Select / Binary | `Yes (1) / No (0)` | Indicates if the primary language of the movie is English. |
| **Is USA?** | Select / Binary | `Yes (1) / No (0)` | Indicates if the movie was produced in the USA. |
| **Genres** | Checkboxes | Multiple choice (Action, Comedy, Drama, Sci-Fi, Thriller, etc.) | One or more genres associated with the movie. |

### Error Handling & Validations:
* **HTTP 400 (Bad Request):** Triggered if required fields are missing, empty, or fall outside the valid ranges listed above.
* **HTTP 500 (Internal Server Error):** Triggered if an unexpected internal server crash occurs (e.g., a missing `trained_model.pkl` file or a runtime version/mathematical anomaly).