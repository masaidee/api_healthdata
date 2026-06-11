import re
from PIL import Image, ImageFilter, ImageOps
import pytesseract
from flask import Flask, request, jsonify
import os
import io  # <--- เพิ่มบรรทัดนี้
import pickle
import numpy as np

from deepface import DeepFace
import tempfile
import cv2

app = Flask(__name__)

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

def crop_face_from_idcard(image_path, save_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:
        return False  # ไม่เจอหน้า
    (x, y, w, h) = faces[0]
    face_img = img[y:y+h, x:x+w]
    cv2.imwrite(save_path, face_img)
    return True

@app.route('/upload-card', methods=['POST'])
def upload_idcard():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # บันทึกไฟล์ชั่วคราว
    filepath = os.path.join('tmp', file.filename)
    os.makedirs('tmp', exist_ok=True)
    file.save(filepath)
    print(f"Saved file to {filepath}")  # เพิ่มบรรทัดนี้

    # --- ปรับภาพก่อน OCR ---
    img = Image.open(filepath).convert('L')  # Grayscale
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.point(lambda x: 0 if x < 140 else 255, '1')  # Threshold

    text = pytesseract.image_to_string(img, lang='tha+eng')

    # print(text)
    return jsonify({
        "textall": text
    })

@app.route('/compare-face', methods=['POST'])
def compare_face():
    if 'selfie' not in request.files:
        return jsonify({"error": "ต้องแนบไฟล์ selfie"}), 400
    if 'thaiId' not in request.files:
        return jsonify({"error": "ต้องแนบไฟล์ thaiId"}), 400

    selfie_file = request.files['selfie']
    thaiId_file = request.files['thaiId']

    # Save selfie และบัตรประชาชนเป็นไฟล์ชั่วคราวใน tmp (และไม่ลบ)
    os.makedirs('tmp', exist_ok=True)
    selfie_path = os.path.join('tmp', selfie_file.filename)
    thaiid_path = os.path.join('tmp', thaiId_file.filename)
    selfie_file.save(selfie_path)
    thaiId_file.save(thaiid_path)
    print(f"Saved selfie to {selfie_path}")
    print(f"Saved thaiId to {thaiid_path}")

    # ตัดเฉพาะส่วนที่เป็นรูปหน้าจากบัตรประชาชน
    thaiid_face_path = os.path.join('tmp', 'face_' + thaiId_file.filename)
    found = crop_face_from_idcard(thaiid_path, thaiid_face_path)
    if not found:
        print('ไม่พบใบหน้าในบัตรประชาชน')
        return jsonify({"message": "ไม่พบใบหน้าในบัตรประชาชน"}), 400

    # ตัดเฉพาะส่วนที่เป็นรูปหน้าจาก selfie
    selfie_face_path = os.path.join('tmp', 'face_' + selfie_file.filename)
    found_selfie = crop_face_from_idcard(selfie_path, selfie_face_path)
    if not found_selfie:
        print('ไม่พบใบหน้าในรูป selfie')
        return jsonify({"message": "ไม่พบใบหน้าในรูป selfie"}), 400

    try:
        result = DeepFace.verify(
            img1_path=thaiid_face_path,
            img2_path=selfie_face_path,
            enforce_detection=True,
            model_name="ArcFace",
            detector_backend="retinaface"
        )
        print(result)
        # คำนวณความแม่นยำ (confidence) แบบง่าย: ยิ่ง distance ต่ำยิ่งแม่น
        try:
            confidence = 1 - (result["distance"] / result["threshold"])
            confidence = max(0.0, min(1.0, confidence))
        except Exception:
            confidence = None
        return jsonify({
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "confidence": confidence,
            "message": "ตรงกัน" if result["verified"] else "ไม่ตรงกัน"
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400
    # ไม่ต้องลบไฟล์

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


if __name__ == "__main__":
    # For Docker: allow host/port override via env vars
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 8088))
    app.run(host=host, port=port)
