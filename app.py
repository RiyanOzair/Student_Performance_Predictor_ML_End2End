from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else: 
        data = CustomData(
            gender=request.form['gender'],
            race_ethnicity=request.form['ethnicity'],
            parental_level_of_education=request.form['parental_level_of_education'],
            lunch=request.form['lunch'],
            test_preparation_course=request.form['test_preparation_course'],
            reading_score=int(request.form['reading_score']),
            writing_score=int(request.form['writing_score'])
        )

        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results=results[0])

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.json

        custom_data = CustomData(
            gender=data['gender'],
            race_ethnicity=data['race_ethnicity'],
            parental_level_of_education=data['parental_level_of_education'],
            lunch=data['lunch'],
            test_preparation_course=data['test_preparation_course'],
            reading_score=int(data['reading_score']),
            writing_score=int(data['writing_score'])
        )

        pred_df = custom_data.get_data_as_dataframe()

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)

        return jsonify({
            "prediction": float(result[0])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })    

@app.route('/health')
def health():
    return {"status": "running"}

if __name__ == "__main__":
    print("\nLocalhost running at: http://127.0.0.1:5000/\n")
    app.run(host='0.0.0.0', debug=True)