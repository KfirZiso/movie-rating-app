import os
import pickle
import pandas as pd
<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the trained model pipeline during server startup
=======
from flask import Flask, render_template, request

app = Flask(__name__)

>>>>>>> 93a46087ca051fa4471c6c8c3eb2b98a811795ec
MODEL_PATH = "model.pkl"
with open(MODEL_PATH, "rb") as file:
    pipeline = pickle.load(file)

<<<<<<< HEAD
def prepare_data(data_json):
    """
    Background data processing logic.
    Takes validated inputs from the JSON payload and engineers features for the model.
    """
    runtime = float(data_json.get("runtimeMinutes"))
    selected_genres = data_json.get("genres", [])
    
    # 1. Automatically calculate the total number of selected genres
    genre_count = len(selected_genres) if selected_genres else 1
    
    # 2. Automatically map runtime into duration categories based on Part 2 logic
    if runtime < 90:
        runtime_category_num = 0
    elif runtime <= 150:
        runtime_category_num = 1
    else:
        runtime_category_num = 2

    # 3. Construct the comprehensive dictionary containing all exact features expected by the pipeline
    processed_dict = {
        "runtimeMinutes": runtime,
        "genre_count": genre_count,
        "is_post_imdb": int(data_json.get("is_post_imdb")),
        "num_a_list_actors": int(data_json.get("num_a_list_actors")),
        "is_english": int(data_json.get("is_english")),
        "is_usa": int(data_json.get("is_usa")),
        "runtime_category_num": runtime_category_num,
        
        # Binary genre mapping (1 if checked, 0 otherwise)
        "genre_Action": 1 if "genre_Action" in selected_genres else 0,
        "genre_Comedy": 1 if "genre_Comedy" in selected_genres else 0,
        "genre_Drama": 1 if "genre_Drama" in selected_genres else 0,
        "genre_Thriller": 1 if "genre_Thriller" in selected_genres else 0,
        "genre_Romance": 1 if "genre_Romance" in selected_genres else 0,
        "genre_Sci-Fi": 1 if "genre_Sci-Fi" in selected_genres else 0,
        "genre_Horror": 1 if "genre_Horror" in selected_genres else 0,
        "genre_Documentary": 1 if "genre_Documentary" in selected_genres else 0
    }
    
    return pd.DataFrame([processed_dict])

@app.route("/", methods=["GET"])
def index():
    # GET method: Cleanly renders the initial empty index.html form
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data_json = request.get_json()
        if not data_json:
            return jsonify({"error": "Missing input data: No valid JSON received"}), 400
            
        # Dictionary to accumulate all validation errors across fields
        errors_dict = {}
        required_fields = ["runtimeMinutes", "num_a_list_actors", "is_post_imdb", "is_english", "is_usa"]
        
        # --- 1. FIRST PASS: VALIDATE MISSING FIELDS ---
        for field in required_fields:
            if field not in data_json or data_json[field] is None or str(data_json[field]).strip() == "":
                errors_dict[field] = "This field is required and cannot be empty."
        
        # --- 2. SECOND PASS: VALIDATE DATA TYPES (Only for fields that aren't already missing) ---
        if "runtimeMinutes" not in errors_dict:
            try:
                float(data_json["runtimeMinutes"])
            except ValueError:
                errors_dict["runtimeMinutes"] = "Invalid input value. Must contain a valid number."
                
        if "num_a_list_actors" not in errors_dict:
            try:
                int(data_json["num_a_list_actors"])
            except ValueError:
                errors_dict["num_a_list_actors"] = "Invalid input value. Must contain a valid integer."

        # If any validation errors accumulated, reject request immediately with HTTP 400 payload
        if errors_dict:
            return jsonify({
                "error": "Validation failed across multiple fields.",
                "invalid_fields": errors_dict  # Returns all field errors combined
            }), 400

        # Steps 2 & 3: Create DataFrame and run feature engineering behind the scenes
        df_input = prepare_data(data_json)
        
        # Step 4: Execute model.predict on the processed dataframe row
        pred_value = pipeline.predict(df_input)[0]
        prediction = round(float(pred_value), 2)
        
        # Step 5: Return successful prediction response payload containing predicted_rating
        return jsonify({"predicted_rating": prediction})
        
    except Exception as e:
        # Validation 3: Catch unexpected runtime crashes (Returns HTTP 500)
        return jsonify({"error": f"Internal server error: {str(e)}", "invalid_fields": None}), 500
=======
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    
    if request.method == "POST":
        try:
            # 1. קבלת רשימת הז'אנרים שהמשתמש סימן בטופס
            selected_genres = request.form.getlist("genres")
            
            # 2. בניית מילון הנתונים הבסיסי
            data = {
                "runtimeMinutes": float(request.form.get("runtimeMinutes", 0)),
                "genre_count": int(request.form.get("genre_count", 0)),
                "is_post_imdb": int(request.form.get("is_post_imdb", 0)),
                "num_a_list_actors": int(request.form.get("num_a_list_actors", 0)),
                "is_english": int(request.form.get("is_english", 0)),
                "is_usa": int(request.form.get("is_usa", 0)),
                "runtime_category_num": int(request.form.get("runtime_category_num", 0)),
                
                # תרגום אוטומטי: אם הז'אנר נמצא ברשימה שסומנה -> 1, אחרת -> 0
                "genre_Action": 1 if "genre_Action" in selected_genres else 0,
                "genre_Comedy": 1 if "genre_Comedy" in selected_genres else 0,
                "genre_Drama": 1 if "genre_Drama" in selected_genres else 0,
                "genre_Thriller": 1 if "genre_Thriller" in selected_genres else 0,
                "genre_Romance": 1 if "genre_Romance" in selected_genres else 0,
                "genre_Sci-Fi": 1 if "genre_Sci-Fi" in selected_genres else 0,
                "genre_Horror": 1 if "genre_Horror" in selected_genres else 0,
                "genre_Documentary": 1 if "genre_Documentary" in selected_genres else 0
            }
            
            # המרה ל-DataFrame וביצוע חיזוי
            df_input = pd.DataFrame([data])
            pred_value = pipeline.predict(df_input)[0]
            prediction = round(float(pred_value), 2)
            
        except Exception as e:
            prediction = f"שגיאה בחישוב הניבוי: {str(e)}"
            
    return render_template("index.html", prediction=prediction)
>>>>>>> 93a46087ca051fa4471c6c8c3eb2b98a811795ec

if __name__ == "__main__":
    app.run(debug=True, port=5000)