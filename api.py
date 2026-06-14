import pandas as pd
import os
import pickle
import pandas as pd  # שורת הייבוא המתוקנת!
from flask import Flask, render_template, request, jsonify

# תיקון קריטי: ייבוא פונקציית העיבוד המקורית מחלק 2 של המטלה למניעת כפילות קוד!
from assets_data_prep import prepare_data

app = Flask(__name__)

# Load the trained model pipeline during server startup
MODEL_PATH = "trained_model.pkl"
with open(MODEL_PATH, "rb") as file:
    pipeline = pickle.load(file)

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

        # Steps 2 & 3: Convert the JSON dict into a one-row DataFrame so prepare_data can use it
        df_input = pd.DataFrame([data_json])
        df_processed = prepare_data(df_input)
        
        # Step 4: Execute model.predict on the processed dataframe row
        pred_value = pipeline.predict(df_processed)[0]
        prediction = round(float(pred_value), 2)
        
        # Step 5: Return successful prediction response payload containing predicted_rating
        return jsonify({"predicted_rating": prediction})
        
    except Exception as e:
        # Validation 3: Catch unexpected runtime crashes (Returns HTTP 500)
        return jsonify({"error": f"Internal server error: {str(e)}", "invalid_fields": None}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
