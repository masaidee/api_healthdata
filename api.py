import httpx
from flask import Flask, request, jsonify
import numpy as np
import requests
from payload import (

    flex_predict_diabetes,
    flex_analysis_data_diabetes,
    flex_recommendations_diabetes,

    flex_predict_bloodfat,
    flex_analysis_data_bloodfat,
    flex_recommendations_bloodfat,
    
    flex_predict_stroke,
    flex_analysis_data_stroke,
    flex_recommendations_stroke
)
from function import(
    data_diabetes,
    data_bloodfat,
    data_stroke
) 

app = Flask(__name__)



LINE_API_URL = "https://api.line.me/v2/bot/message/push"
#myhealth
LINE_ACCESS_TOKEN = "1x3tE+qWFFWfG2wxF3B8iemgo4N9PSNxQ9pkXc66w+cq00iPoCgxq1XdHOVZHl+sgeWzO5TtQvYp8z/LgvUlwHrVWBCC9zp+FJrJGHeT9NoMJ9OQvpGDXAsYOuEYMRA/53Q0qkOCkRuiMa4VTENihAdB04t89/1O/w1cDnyilFU="
#sipsinse
# LINE_ACCESS_TOKEN = "NeXMAZt6QoDOwz7ryhruPZ0xrkfHbWPhQVvA9mLII8Y0CAeOTB7zXUGhzs8Q6JhT8ntAKAilCJQKjE/6rTfonbVRFTLkg7WL8rtzfHisWYBLbOCc6jkx6iePMA1VNJuqN/0B05f3+jq8d2nOeFnGQgdB04t89/1O/w1cDnyilFU="
# ้health
# LINE_ACCESS_TOKEN = "+mxXTWUhft/lds9sjCQLThOE7hSpYYa3Qc9Ex8f+/7NNB6075OpjZ0jIC/83ABlncS0BObm5K+8oDnHck6sKcILblYZv9AUU8TllWdaHWHWIE8Cp9Z1ybS0jfzi5iF6hDwggWQurGYX93oAOwwr9CQdB04t89/1O/w1cDnyilFU="
# healthgroup
# LINE_ACCESS_TOKEN = "dlmMJIDuAnFTOrIxt1IjvGRihrCyyINAXB2QaTDGEUaikjefh2dZ7CFOk3hpBGSXNqCClqCGkeMULxN3tfC4DAYl/5c15dL1rTEhZ9AwyF7XSx2A7Cs4/pJhlQQWISwT2bWsyzxc9lxK8vDbAj8YnAdB04t89/1O/w1cDnyilFU="




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
    elif intent_name == 'Check - Bloodfat': #
        answer_str = send_bloodfat()
    elif intent_name == 'Check - Stroke': #
        answer_str = send_stroke()
    else:
        # ถ้า intent_name ไม่ตรงกับเงื่อนไขที่กำหนด ให้ใช้ฟังก์ชัน find_best_match_with_fuzzy
        answer_str = "ขอโทษครับ ฉันไม่เข้าใจคำถามของคุณ"
    return answer_str

def get_user():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId'] 
    
    return user

def send_stroke():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    reply_text, sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his = data_stroke()
    print(f"aaareply_text: {reply_text}, sbp: {sbp}, dbp: {dbp}, his: {his}, smoke: {smoke}, fbs: {fbs}, HbAlc: {HbAlc}, total_Cholesterol: {total_Cholesterol}, Exe: {Exe}, bmi: {bmi}, family_his: {family_his}")
    if reply_text == "ข้อมูลสุขภาพไม่ครบถ้วน" or reply_text == "Payload not found or is not a list":
        headers = {
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Identify missing data
        missing_data = []
        if sbp == "":
            missing_data.append("sbp")
        if dbp == "":
            missing_data.append("dbp")
        if his == "":
            missing_data.append("his")
        if smoke == "":
            missing_data.append("smoke")
        if fbs == "":
            missing_data.append("fbs")
        if HbAlc == "":
            missing_data.append("HbAlc")
        if total_Cholesterol == "":
            missing_data.append("total_Cholesterol")
        if Exe == "":
            missing_data.append("exe")
        if bmi == "":
            missing_data.append("BMI")
        if family_his == "":
            missing_data.append("family_his")

        message_text = f"ไม่สามารถประเมินความเสี่ยงได้ เนื่องจากข้อมูลสุขภาพของคุณไม่ครบถ้วน \n -{ '\n -'.join(missing_data)} \nกรุณาอัปเดตข้อมูลของคุณ"

        payload = {
            "to": user,
            "messages": [{"type": "text", "text": message_text}]
        }

        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "error", "message": "ข้อมูลสุขภาพไม่ครบถ้วน"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}

    # Continue processing when data is complete
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Define colors based on health data
    colors = {
        "sbp": "#008000" if sbp < 120 else "#FF0000",
        "dbp": "#008000" if dbp < 80 else "#FF0000",
        "his": "#008000" if his == "ไม่" else "#FF0000",
        "smoke": "#008000" if smoke == "ไม่" else "#FF0000",
        "fbs": "#008000" if fbs < 126 else "#FF0000",
        "HbAlc": "#008000" if HbAlc < 7 else "#FF0000",
        "total_Cholesterol": "#008000" if total_Cholesterol < 200 else "#FF0000",
        "Exe": "#008000" if Exe == "ไม่" else "#FF0000",
        "bmi": "#008000" if bmi < 25 else "#FF0000",
        "family_his": "#008000" if family_his == "ไม่" else "#FF0000"
    }

    # Create recommendations
    recommendations = []
    if reply_text == "ความเสี่ยงต่ำ":
        recommendations.append("- ควรรักษาสุขภาพให้แข็งแรง ออกกำลังกายสม่ำเสมอ และควบคุมปัจจัยเสี่ยงต่างๆ")
    elif reply_text == "ความเสี่ยงปานกลาง":
        recommendations.append("- ควรปรับเปลี่ยนพฤติกรรมสุขภาพ ควบคุมความดันโลหิตและระดับน้ำตาลในเลือด และพบแพทย์เพื่อตรวจสุขภาพประจำปี")
    else:
        recommendations.append("- ควรพบแพทย์โดยด่วนเพื่อประเมินความเสี่ยงอย่างละเอียด และรับคำแนะนำในการป้องกันโรคหลอดเลือดสมอง")

    # Create Flex Messages
    Flex_message = []
    predict = flex_predict_stroke(reply_text, "#008000" if reply_text == "ความเสี่ยงต่ำ" else "#FFD700" if reply_text == "ความเสี่ยงปานกลาง" else "#FF0000")
    if predict:
        Flex_message.append(predict)

    analysis_data = flex_analysis_data_stroke(sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his, colors)
    if analysis_data:
        Flex_message.append(analysis_data)

    recommendations = flex_recommendations_stroke(recommendations)
    if recommendations:
        Flex_message.append(recommendations)

    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "success", "message": "ส่งข้อความสำเร็จโรคหลอดเลือดสมอง"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}
    else:
        return {"status": "error", "message": "ไม่มีข้อความที่ต้องส่ง"}


def send_bloodfat():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    reply_text, Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl = data_bloodfat()
    print(f"aaareply_text: {reply_text}, Gender: {Gender}, Weight: {Weight}, Height: {Height}, Cholesterol: {Cholesterol}, Triglycerider: {Triglycerider}, Hdl: {Hdl}, Ldl: {Ldl}")

    if reply_text == "ข้อมูลสุขภาพไม่ครบถ้วน" or reply_text == "Payload not found or is not a list":
        headers = {
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Identify missing data
        missing_data = []
        if Gender == "":
            missing_data.append("เพศ")
        if Weight == "":
            missing_data.append("น้ำหนัก")
        if Height == "":
            missing_data.append("ส่วนสูง")
        if Cholesterol == "":
            missing_data.append("คอเลสเตอรอล")
        if Triglycerider == "":
            missing_data.append("ไตรกลีเซอไรด์")
        if Hdl == "":
            missing_data.append("HDL")
        if Ldl == "":
            missing_data.append("LDL")

        message_text = f"ไม่สามารถประเมินความเสี่ยงได้ เนื่องจากข้อมูลสุขภาพของคุณไม่ครบถ้วน \n -{ '\n -'.join(missing_data)} \nกรุณาอัปเดตข้อมูลของคุณ"

        payload = {
            "to": user,
            "messages": [{"type": "text", "text": message_text}]
        }

        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "error", "message": "ข้อมูลสุขภาพไม่ครบถ้วน"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}

    # Continue processing when data is complete
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Define colors based on health data
    colors = {
        "Cholesterol": "#008000" if Cholesterol < 200 else "#FF0000",
        "Triglycerider": "#008000" if Triglycerider < 150 else "#FF0000",
        "Hdl": "#008000" if Hdl > 40 else "#FF0000",
        "Ldl": "#008000" if Ldl < 100 else "#FF0000"
    }

    # Create recommendations
    recommendations = []
    if reply_text == "ความเสี่ยงต่ำ":
        recommendations.append("- ควรรักษาระดับไขมันในเลือดให้อยู่ในเกณฑ์ปกติ โดยการควบคุมอาหารและออกกำลังกายอย่างสม่ำเสมอ")
    elif reply_text == "ความเสี่ยงปานกลาง":
        recommendations.append("- ควรปรับเปลี่ยนพฤติกรรมการรับประทานอาหารและออกกำลังกายอย่างสม่ำเสมอ พร้อมทั้งตรวจระดับไขมันในเลือดอย่างน้อยปีละ 1 ครั้ง")
    else:
        recommendations.append("- ควรพบแพทย์เพื่อรับคำแนะนำในการควบคุมระดับไขมันในเลือด ปรับเปลี่ยนพฤติกรรมการรับประทานอาหาร ออกกำลังกายอย่างสม่ำเสมอ และอาจต้องพิจารณาการใช้ยาลดไขมันในเลือดตามคำแนะนำของแพทย์")

    # Create Flex Messages
    Flex_message = []
    predict = flex_predict_bloodfat(reply_text, "#008000" if reply_text == "ความเสี่ยงต่ำ" else "#FFD700" if reply_text == "ความเสี่ยงปานกลาง" else "#FF0000")
    if predict:
        Flex_message.append(predict)

    analysis_data = flex_analysis_data_bloodfat(Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl, colors)
    if analysis_data:
        Flex_message.append(analysis_data)

    recommendations = flex_recommendations_bloodfat(recommendations)
    if recommendations:
        Flex_message.append(recommendations)

    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return {"status": "success", "message": "ส่งข้อความสำเร็จโรคไขมันในเลือด"}
        else:
            return {"status": "error", "message": f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}"}
    else:
        return {"status": "error", "message": "ไม่มีข้อความที่ต้องส่ง"}

def send_diabetes():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    reply_text, age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his = data_diabetes()

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

        message_text = f"ไม่สามารถประเมินความเสี่ยงได้ เนื่องจากข้อมูลสุขภาพของคุณไม่ครบถ้วน \n -{ '\n -'.join(missing_data)} \nกรุณาอัปเดตข้อมูลของคุณ"

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
    app.run(port=8000)
