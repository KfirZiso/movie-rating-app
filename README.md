# Movie Rating Prediction App 🎬

This project is a web-based application built with Flask that predicts movie ratings using a trained Machine Learning model. The application features a user-friendly frontend with input validation, dynamic error handling (including custom templates for HTTP 400 and HTTP 500 errors), and a robust backend integration.

## Authors & Team Members 👥
* **Kfir Ziso 322883091**
* **Yael Bukris 324050138**

---

## 1. Project Description 📝

The application provides an interface for users to input movie characteristics such as runtime, number of A-list actors, language, country, IMDb period, and genres.  
After submitting the form, the Flask server processes the data, prepares it for the trained machine learning model, and returns an instant predicted movie rating.
* **Backend:** Flask API (`api.py`) that handles JSON payloads, performs data preprocessing, and serves model predictions using a Scikit-Learn trained model.
* **Frontend:** Interactive HTML webpage (`templates/index.html`) featuring input fields, genre checkboxes, asynchronous fetch requests, and dynamic result/error display.

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

## 5. Input Fields & Expected Values 📊

The model expects the following input fields via the UI form:

| Field Name | Data Type | Expected Values / Options | Description |
| :--- | :--- | :--- | :--- |
| **runtimeMinutes** | Number | Example: `120` | Total duration of the movie in minutes. |
| **num_a_list_actors** | Integer | Example: `2` | Number of A-list actors in the movie. |
| **is_post_imdb** | Binary | `1` = Yes, `0` = No | Indicates whether the movie was produced after IMDb was founded. |
| **is_english** | Binary | `1` = Yes, `0` = No | Indicates whether the main language is English. |
| **is_usa** | Binary | `1` = Yes, `0` = No | Indicates whether the movie was produced in the USA. |
| **genres** | Checkboxes | Action, Comedy, Drama, Thriller, Romance, Sci-Fi, Horror, Documentary | One or more genres associated with the movie. |

### Error Handling & Validations:
* **HTTP 400 (Bad Request):** Returned when required fields are missing, empty, or contain invalid values, such as text instead of a number.
* **HTTP 500 (Internal Server Error):** Returned when an unexpected server-side error occurs.
### Error Handling & Validations:
* **HTTP 400 (Bad Request):** Triggered if required fields are missing, empty, or fall outside the valid ranges listed above.
* **HTTP 500 (Internal Server Error):** Triggered if an unexpected internal server crash occurs (e.g., a missing `trained_model.pkl` file or a runtime version/mathematical anomaly).
