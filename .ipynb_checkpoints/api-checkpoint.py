
import os
import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# תיקון 1: הוספת מרכאות לשם הקובץ
MODEL_PATH = "model.pkl"

with open(MODEL_PATH, "rb") as file:
    pipeline = pickle.load(file)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    
    # תיקון 2: הוספת מרכאות ל-POST
    if request.method == "POST":
        try:
            # תיקון 3: הוספת נקודתיים (:) ומרכאות לכל המפתחות והערכים במילון
            data = {
                "runtimeMinutes": float(request.form.get("runtimeMinutes", 0)),
                "genre_count": int(request.form.get("genre_count", 0)),
                "is_post_imdb": int(request.form.get("is_post_imdb", 0)),
                "num_a_list_actors": int(request.form.get("num_a_list_actors", 0)),
                "is_english": int(request.form.get("is_english", 0)),
                "is_usa": int(request.form.get("is_usa", 0)),
                "runtime_category_num": int(request.form.get("runtime_category_num", 0)),
                "genre_Action": int(request.form.get("genre_Action", 0)),
                "genre_Comedy": int(request.form.get("genre_Comedy", 0)),
                "genre_Drama": int(request.form.get("genre_Drama", 0)),
                "genre_Thriller": int(request.form.get("genre_Thriller", 0)),
                "genre_Romance": int(request.form.get("genre_Romance", 0)),
                "genre_Sci-Fi": int(request.form.get("genre_Sci-Fi", 0)),
                "genre_Horror": int(request.form.get("genre_Horror", 0)),
                "genre_Documentary": int(request.form.get("genre_Documentary", 0))
            }
            
            # 2. המרה ל-DataFrame
            df_input = pd.DataFrame([data])
            
            # 3. ביצוע החיזוי באמצעות ה-pipeline
            pred_value = pipeline.predict(df_input)[0]
            prediction = round(float(pred_value), 2)
            
        # תיקון 4: הוספת נקודתיים בסוף ה-except
        except Exception as e:
            # תיקון 5: הוספת מרכאות סביב מחרוזת ה-f-string
            prediction = f"שגיאה בחישוב הניבוי: {str(e)}"
            
    # תיקון 6: הוספת מרכאות לשם קובץ ה-HTML
    return render_template("index.html", prediction=prediction)

# תיקון 7: הוספת מרכאות ל-__main__ ונקודתיים בסוף השורה
if __name__ == "__main__":
    app.run(debug=True, port=5000)