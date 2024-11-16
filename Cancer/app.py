from flask import Flask, jsonify, render_template, request
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# Load your pre-trained model
cancer_prediction_model = joblib.load('model.pkl')  # Ensure 'model.pkl' is in the project folder
scaler = joblib.load('scaler.pkl')

print('app.py started')
# Render the HTML form
@app.route('/')
def home():
    return render_template('index.html')  # HTML form is 'index.html' in 'templates' folder

# Handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Collect the form data
    features = [
        float(request.form['radius_mean']),
        float(request.form['texture_mean']),
        float(request.form['perimeter_mean']),
        float(request.form['area_mean']),
        float(request.form['smoothness_mean']),
        float(request.form['compactness_mean']),
        float(request.form['concavity_mean']),
        float(request.form['concave_points_mean']),
        float(request.form['symmetry_mean']),
        float(request.form['fractal_dimension']),
        
        float(request.form['radius_se']),
        float(request.form['texture_se']),
        float(request.form['perimeter_se']),
        float(request.form['area_se']),
        float(request.form['smoothness_se']),
        float(request.form['compactness_se']),
        float(request.form['concavity_se']),
        float(request.form['concave_points_se']),
        float(request.form['symmetry_se']),
        float(request.form['fractal_dimension_se']),
        
        float(request.form['radius_worst']),
        float(request.form['texture_worst']),
        float(request.form['texture_worst_1']),
        float(request.form['area_worst']),
        float(request.form['smoothness_worst']),
        float(request.form['compactness_worst']),
        float(request.form['concavity_worst']),
        float(request.form['concave_points_worst']),
        float(request.form['symmetry_worst']),
        float(request.form['fractal_dimension_worst']),
    ]

    # Adding encoded values for categorical inputs
    n_stage = request.form['n_stage']
    N1, N2, N3 = (1, 0, 0) if n_stage == "N1" else (0, 1, 0) if n_stage == "N2" else (0, 0, 1)

    sixth_stage = request.form['sixth_stage']
    IIA, IIB, IIIA, IIIC, IIIB = (1, 0, 0, 0, 0) if sixth_stage == "IIA" else \
                                 (0, 1, 0, 0, 0) if sixth_stage == "IIB" else \
                                 (0, 0, 1, 0, 0) if sixth_stage == "IIIA" else \
                                 (0, 0, 0, 1, 0) if sixth_stage == "IIIC" else (0, 0, 0, 0, 1)

    differentiate = request.form['differentiate']
    diff_moderately, diff_poorly, diff_well, diff_undifferentiated = (1, 0, 0, 0) if differentiate == "Moderately differentiated" else \
                                                                     (0, 1, 0, 0) if differentiate == "Poorly differentiated" else \
                                                                     (0, 0, 1, 0) if differentiate == "Well differentiated" else (0, 0, 0, 1)

    # Append categorical values to features
    features.extend([N1, N2, N3, IIA, IIB, IIIA, IIIC, IIIB, diff_moderately, diff_poorly, diff_well, diff_undifferentiated])

    feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave_points_mean', 'symmetry_mean', 'fractal_dimension',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave_points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'texture_worst.1', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst', 'N1', 'N2',
       'N3', 'IIA', 'IIB', 'IIIA', 'IIIC', 'IIIB', 'Moderately differentiated',
       'Poorly differentiated', 'Well differentiated', 'Undifferentiated']
    input_df = pd.DataFrame([features], columns=feature_names)
    input_scaled = scaler.transform(input_df)
    
    print([features])
    # Make prediction and print result in terminal
    prediction = cancer_prediction_model.predict(input_scaled)
    print("Prediction:", prediction[0])  # Print the prediction result in terminal

    # Prepare result to display on the webpage
    result = "Malignant" if prediction[0] == 1 else "Benign"  # Adjust this logic as per model output

    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
