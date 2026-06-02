import os
import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# טעינת המודל (ה-Pipeline שכולל preprocessor ומודל ניבוי)
MODEL_PATH = model.pkl
with open(MODEL_PATH, rb) as file
    pipeline = pickle.load(file)

@app.route(, methods=[GET, POST])
def index()
    prediction = None
    
    if request.method == POST
        try
            # 1. שליפת הנתונים מהטופס ב-HTML והמרתם לסוגי הנתונים המתאימים
            data = {
                runtimeMinutes float(request.form.get(runtimeMinutes, 0)),
                genre_count int(request.form.get(genre_count, 0)),
                is_post_imdb int(request.form.get(is_post_imdb, 0)),
                num_a_list_actors int(request.form.get(num_a_list_actors, 0)),
                is_english int(request.form.get(is_english, 0)),
                is_usa int(request.form.get(is_usa, 0)),
                runtime_category_num int(request.form.get(runtime_category_num, 0)),
                genre_Action int(request.form.get(genre_Action, 0)),
                genre_Comedy int(request.form.get(genre_Comedy, 0)),
                genre_Drama int(request.form.get(genre_Drama, 0)),
                genre_Thriller int(request.form.get(genre_Thriller, 0)),
                genre_Romance int(request.form.get(genre_Romance, 0)),
                genre_Sci-Fi int(request.form.get(genre_Sci-Fi, 0)),
                genre_Horror int(request.form.get(genre_Horror, 0)),
                genre_Documentary int(request.form.get(genre_Documentary, 0))
            }
            
            # 2. המרה ל-DataFrame (המודל שלכם אומן על סמך שמות העמודות האלו)
            df_input = pd.DataFrame([data])
            
            # 3. ביצוע החיזוי באמצעות ה-pipeline שדואג להכל
            pred_value = pipeline.predict(df_input)[0]
            prediction = round(float(pred_value), 2)
            
        except Exception as e
            prediction = fשגיאה בחישוב הניבוי {str(e)}
            
    # החזרת דף הבית יחד עם תוצאת הניבוי (אם קיימת)
    return render_template(index.html, prediction=prediction)

if __name__ == __main__
    app.run(debug=True, port=5000)
