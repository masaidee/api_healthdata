import httpx
from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests
from payload import (

    flex_predict_diabetes,
    flex_analysis_data_diabetes,
    flex_recommendations_diabetes
)

app = Flask(__name__)

# โหลดโมเดลที่ใช้ทำนายโรคเบาหวาน
with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\model_dm_risk.pkl", 'rb') as model_file:
    Diabetes_classifier = pickle.load(model_file)



LINE_API_URL = "https://api.line.me/v2/bot/message/push"
#myhealth
# LINE_ACCESS_TOKEN = "1x3tE+qWFFWfG2wxF3B8iemgo4N9PSNxQ9pkXc66w+cq00iPoCgxq1XdHOVZHl+sgeWzO5TtQvYp8z/LgvUlwHrVWBCC9zp+FJrJGHeT9NoMJ9OQvpGDXAsYOuEYMRA/53Q0qkOCkRuiMa4VTENihAdB04t89/1O/w1cDnyilFU="
#sipsinse
# LINE_ACCESS_TOKEN = "NeXMAZt6QoDOwz7ryhruPZ0xrkfHbWPhQVvA9mLII8Y0CAeOTB7zXUGhzs8Q6JhT8ntAKAilCJQKjE/6rTfonbVRFTLkg7WL8rtzfHisWYBLbOCc6jkx6iePMA1VNJuqN/0B05f3+jq8d2nOeFnGQgdB04t89/1O/w1cDnyilFU="
# ้health
# LINE_ACCESS_TOKEN = "+mxXTWUhft/lds9sjCQLThOE7hSpYYa3Qc9Ex8f+/7NNB6075OpjZ0jIC/83ABlncS0BObm5K+8oDnHck6sKcILblYZv9AUU8TllWdaHWHWIE8Cp9Z1ybS0jfzi5iF6hDwggWQurGYX93oAOwwr9CQdB04t89/1O/w1cDnyilFU="
# healthgroup
LINE_ACCESS_TOKEN = "dlmMJIDuAnFTOrIxt1IjvGRihrCyyINAXB2QaTDGEUaikjefh2dZ7CFOk3hpBGSXNqCClqCGkeMULxN3tfC4DAYl/5c15dL1rTEhZ9AwyF7XSx2A7Cs4/pJhlQQWISwT2bWsyzxc9lxK8vDbAj8YnAdB04t89/1O/w1cDnyilFU="




@app.route('/', methods=['POST'])
def MainFunction():
    
    # รับข้อมูลที่ส่งมาจาก Dialogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    print("Received request:", question_from_dailogflow_raw)  # Debugging line
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    # ส่งคำตอบกลับไปยัง LINE
    response_json = {
        "fulfillmentText": answer_from_bot
    }
    print("Response to be sent:", response_json)  # Debugging line
    return jsonify(response_json)

def generating_answer(question_from_dailogflow_raw):
    # ดึง queryResult จากข้อมูลที่ได้รับ
    question_from_dailogflow_dict = question_from_dailogflow_raw.get("queryResult", {})
    intent_name = question_from_dailogflow_dict.get("intent", {}).get("displayName", "")
    question = question_from_dailogflow_dict.get("queryText", "")
    
    print("คำถาม:", question)  # Debugging line

    # ตรวจสอบค่า intent_name เพื่อเรียกใช้ฟังก์ชันที่ต้องการ 
    if intent_name == 'Check - Diabetes': #เพิ่มข้อมูล
        answer_str = send_diabetes()
    else:
        # ถ้า intent_name ไม่ตรงกับเงื่อนไขที่กำหนด ให้ใช้ฟังก์ชัน find_best_match_with_fuzzy
        answer_str = "ขอโทษครับ ฉันไม่เข้าใจคำถามของคุณ"
    return answer_str

def get_user():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId'] 
    
    return user


def get_healthdata():
    params = {
        "userId": "user1645ac833f9e753ea4698578c6ec2cdb"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 32a9fcf38fb1aebaed'
    }

    response = httpx.post(
        "https://api.myhealthgroup.net/apiservice/line/getUserHealth", headers=headers, json=params)
    req = response.json()
    payload = req.get('payload')

    if payload and isinstance(payload, list) and len(payload) > 0:
        sorted_payload = sorted(payload, key=lambda x: x.get('clinicdate', ''), reverse=True)
        latest_item = sorted_payload[0]
        healthdata = latest_item.get('healthdata')

        # ตรวจสอบว่า healthdata มีค่าหรือไม่
        if not healthdata:
            return "ข้อมูลสุขภาพไม่ครบถ้วน", None, None, None, None, None, None, None, None, None, None

        # ดึงค่าจาก healthdata
        age = healthdata.get('age', {}).get('value', "") or ""
        bmi1 = healthdata.get('bmi1', {}).get('value', "") or ""
        visceralfat1 = healthdata.get('visceralfat1', {}).get('value', "") or ""
        wrcis1 = healthdata.get('wrcis1', {}).get('value', "") or ""
        ht = healthdata.get('ht', {}).get('value', "") or ""
        sbp1 = healthdata.get('sbp1', {}).get('value', "") or ""
        dbp1 = healthdata.get('dbp1', {}).get('value', "") or ""
        fbs1 = healthdata.get('fbs1', {}).get('value', "") or ""
        hba1c1 = healthdata.get('hba1c1', {}).get('value', "") or ""
        his = healthdata.get('his', {}).get('value', "") or ""

        print(f"aage: {age}, bmi1: {bmi1}, visceralfat1: {visceralfat1}, wrcis1: {wrcis1}, ht: {ht}, sbp1: {sbp1}, dbp1: {dbp1}, fbs1: {fbs1}, hba1c1: {hba1c1}, his: {his}")
       
        # ตรวจสอบว่าข้อมูลสำคัญครบหรือไม่
        required_values = [age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his]
        if any(v in ["", None] for v in required_values):
            return "ข้อมูลสุขภาพไม่ครบถ้วน",age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his

        # แปลงค่าข้อมูลเป็น float/int
        age = float(age) if age else 0.0
        bmi1 = float(bmi1) if bmi1 else 0.0
        visceralfat1 = float(visceralfat1) if visceralfat1 else 0.0
        wrcis1 = float(wrcis1) if wrcis1 else 0.0
        ht = int(ht) if ht else 0
        sbp1 = float(sbp1) if sbp1 else 0.0
        dbp1 = float(dbp1) if dbp1 else 0.0
        fbs1 = float(fbs1) if fbs1 else 0.0
        hba1c1 = float(hba1c1) if hba1c1 else 0.0
        his = int(his) if his else 0

        # แปลงเป็น NumPy array
        cleaned_array = [float(x) if x not in ["", None] else 0.0 for x in [age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his]]
        array_np = np.asarray([cleaned_array], dtype=np.float64)
        print(f"array{array_np}")
        # ทำนายผล
        prediction = Diabetes_classifier.predict(array_np)

        # กำหนดข้อความผลลัพธ์
        if prediction[0] == 0:
            reply_text = "ความเสี่ยงต่ำ"
        elif prediction[0] == 1:
            reply_text = "ความเสี่ยงปานกลาง"
        else:
            reply_text = "ความเสี่ยงสูง"

        return reply_text, age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his

    else:
        return "Payload not found or is not a list", None, None, None, None, None, None, None, None, None, None


def send_diabetes():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    reply_text, age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his = get_healthdata()

    if reply_text == "ข้อมูลสุขภาพไม่ครบถ้วน" or reply_text == "Payload not found or is not a list":
        headers = {
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Identify missing data
        missing_data = []
        if age == "":
            missing_data.append("อายุ")
        if bmi1 == "":
            missing_data.append("BMI")
        if visceralfat1 == "":
            missing_data.append("ไขมันในช่องท้อง")
        if wrcis1 == "":
            missing_data.append("อัตราส่วนเอวต่อสะโพก")
        if ht == "":
            missing_data.append("ประวัติความดันโลหิตสูง")
        if sbp1 == "":
            missing_data.append("ความดันโลหิตตัวบน")
        if dbp1 == "":
            missing_data.append("ความดันโลหิตตัวล่าง")
        if fbs1 == "":
            missing_data.append("ระดับน้ำตาลในเลือดขณะอดอาหาร")
        if hba1c1 == "":
            missing_data.append("ระดับน้ำตาลสะสม")
        if his == "":
            missing_data.append("ประวัติครอบครัว")

        print(f"age: {age}, bmi1: {bmi1}, visceralfat1: {visceralfat1}, wrcis1: {wrcis1}, ht: {ht}, sbp1: {sbp1}, dbp1: {dbp1}, fbs1: {fbs1}, hba1c1: {hba1c1}, his: {his}")
        print(f"missing_data: {missing_data}")

        message_text = f"ไม่สามารถประเมินความเสี่ยงได้ เนื่องจากข้อมูลสุขภาพของคุณไม่ครบถ้วน \n({', '.join(missing_data)}) \nกรุณาอัปเดตข้อมูลของคุณ"

        payload = {
            "to": user,
            "messages": [{"type": "text", "text": message_text}]
        }

        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "error", "message": "ข้อมูลสุขภาพไม่ครบถ้วน"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}

    # **ดำเนินการต่อเฉพาะเมื่อข้อมูลครบถ้วน**
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Define colors based on health data
    colors = {
        "bmi": "#008000" if bmi1 < 24.9 else "#FF0000",
        "visceral": "#008000" if visceralfat1 < 9 else "#FF0000",
        "wc": "#008000" if wrcis1 <= 0.50 else "#FF0000",
        "ht": "#008000" if ht == 0 else "#FF0000",
        "sbp": "#008000" if sbp1 <= 120 else "#FF0000",
        "dbp": "#008000" if dbp1 <= 80 else "#FF0000",
        "fbs": "#008000" if fbs1 <= 80 else "#FF0000",
        "HbAlc": "#008000" if hba1c1 < 5.6 else "#FF0000",
        "family_his": "#008000" if his == 0 else "#FF0000"
    }

    # สร้างรายการคำแนะนำเพิ่มเติม
    recommendations = []
    if reply_text == "ความเสี่ยงต่ำ":
        recommendations.append("- เพื่อป้องกันการเกิดโรคเบาหวานในอนาคต ควรออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความ ดันโลหิตโดยไม่ควรเกิน 140/90 มม.ปรอท")
    elif reply_text == "ความเสี่ยงปานกลาง":
        recommendations.append("- เพื่อป้องกันการเกิดโรคเบาหวานในอนาคต ควรออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความ คันโลหิตโดยไม่ควรเกิน 140/90 มม.ปรอท และตรวจน้ำตาลในเลือด อย่างน้อยปีละ 1 ครั้ง ทุกปี")
    else:
        recommendations.append("- ด้วยมีโอกาสสูงมากที่จะเกิดโรคเบาหวานในอนาคต ควรควบคุมอาหารอย่างเคร่งครัดโดยเฉพาะเกี่ยวกับปริมาณคาร์โบไฮเดรตหรือคาร์บในอาหารซึ่งเป็นสารอาหารที่มีผลต่อระดับตาลในเลือด มากที่สุดเมื่อเทียบกับสารอาหารชนิดอื่น ๆมากที่สุดเมื่อเทียบกับสารอาหารชนิดอื่น ๆ ออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความันโลหิตไม่ควรเกิน 140/90 มม.ปรอท และตรวจติดตามระดับน้ำตาลในเลือดอย่างน้อยปีละ 1 ครั้ง ทุกปี")

    # ตรวจสอบและสร้างข้อความสำหรับ Flex Message
    Flex_message = []
    predict = flex_predict_diabetes(reply_text, "#008000" if reply_text == "ความเสี่ยงต่ำ" else "#FFD700" if reply_text == "ความเสี่ยงปานกลาง" else "#FF0000")
    if predict:
        Flex_message.append(predict)

    analysis_data = flex_analysis_data_diabetes(age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his, colors)
    if analysis_data:
        Flex_message.append(analysis_data)

    recommendations = flex_recommendations_diabetes(recommendations)
    if recommendations:
        Flex_message.append(recommendations)

    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "success", "message": "ส่งข้อความสำเร็จโรคเบาหวาน"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}
    else:
        return {"status": "error", "message": "ไม่มีข้อความที่ต้องส่ง"}

    


# @app.get("/healthdata")
# def get():
#     all = get_healthdata()
#     print(all)
#     return {"healthdatafull": all}

    
if __name__ == "__main__":
    app.run()