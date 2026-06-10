from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes so React Native can access it

# Load models safely
try:
    with open(r"model_dm_risk.pkl", 'rb') as f:
        diabetes_model = pickle.load(f)
    print("Loaded Diabetes Model")
except Exception as e:
    print(f"Error loading Diabetes Model: {e}")
    diabetes_model = None

try:
    with open(r"model_blood_fat.pkl", 'rb') as f:
        bloodfat_model = pickle.load(f)
    print("Loaded Blood Fat Model")
except Exception as e:
    print(f"Error loading Blood Fat Model: {e}")
    bloodfat_model = None

try:
    with open(r"model_stroke_risk.pkl", 'rb') as f:
        stroke_model = pickle.load(f)
    print("Loaded Stroke Model")
except Exception as e:
    print(f"Error loading Stroke Model: {e}")
    stroke_model = None

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    disease_type = data.get('type')
    features = data.get('features')

    if not disease_type or not features:
        return jsonify({'status': 'error', 'message': 'Missing type or features'}), 400

    try:
        # Convert all features to float (fill empty with 0.0)
        cleaned_features = [float(x) if x not in ["", None] else 0.0 for x in features]
        array_np = np.asarray([cleaned_features], dtype=np.float64)

        prediction = None
        if disease_type == 'diabetes':
            if not diabetes_model:
                return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
            prediction = diabetes_model.predict(array_np)
        
        elif disease_type == 'bloodfat':
            if not bloodfat_model:
                return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
            prediction = bloodfat_model.predict(array_np)
        
        elif disease_type == 'stroke':
            if not stroke_model:
                return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
            prediction = stroke_model.predict(array_np)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid disease type'}), 400

        # Map prediction to text
        pred_value = prediction[0]
        if pred_value == 0:
            risk_text = "ความเสี่ยงต่ำ"
        elif pred_value == 1:
            risk_text = "ความเสี่ยงปานกลาง"
        else:
            risk_text = "ความเสี่ยงสูง"

        return jsonify({
            'status': 'success',
            'riskLevel': int(pred_value),
            'message': risk_text
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Run on port 5000, accessible from anywhere
    app.run(host='0.0.0.0', port=5000, debug=True)
