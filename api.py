import os
import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

MODEL_PATH = "model.pkl"
with open(MODEL_PATH, "rb") as file:
    pipeline = pickle.load(file)

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)