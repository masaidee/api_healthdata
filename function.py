import httpx
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os
import json
import requests
from datetime import datetime
from flask import request


LINE_ACCESS_TOKEN = "dlmMJIDuAnFTOrIxt1IjvGRihrCyyINAXB2QaTDGEUaikjefh2dZ7CFOk3hpBGSXNqCClqCGkeMULxN3tfC4DAYl/5c15dL1rTEhZ9AwyF7XSx2A7Cs4/pJhlQQWISwT2bWsyzxc9lxK8vDbAj8YnAdB04t89/1O/w1cDnyilFU="
LINE_API_URL = "https://api.line.me/v2/bot/message/push"
ngrok = "https://52fe-184-22-61-212.ngrok-free.app"

# โหลดโมเดลที่ใช้ทำนายโรคเบาหวาน
with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_dm_risk.pkl", 'rb') as model_file:
    Diabetes_classifier = pickle.load(model_file)

with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_blood_fat.pkl", 'rb') as model_file:
    Bloodfat_classifier = pickle.load(model_file)

with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_stroke_risk.pkl", 'rb') as model_file:
    Stroke_classifier = pickle.load(model_file)


def get_userid():
    req = request.get_json(silent=True, force=True)
    try:
        user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
        return user
    except (KeyError, TypeError):
        print("❌ ไม่สามารถดึง userId จาก request ได้")
        return None

def data_stroke():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    print(f"user: {user}")

    userid = get_userid()
    print(f"userid: {userid}")
    params = {
        "userId": "userd647b6fc4828645341e71a8fa302b22c"
    }
    print(f"params: {params}")
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

        if not healthdata:
            return "ข้อมูลสุขภาพไม่ครบถ้วน", None, None, None, None, None, None, None, None, None


        sbp = healthdata.get('sbp', {}).get('value', "") or "10"
        dbp = healthdata.get('dbp', {}).get('value', "") or "22"
        his = healthdata.get('his', {}).get('value', "") or "32"
        smoke = healthdata.get('smoke', {}).get('value', "") or "32"
        fbs = healthdata.get('fbs', {}).get('value', "") or "22"
        HbAlc = healthdata.get('HbAlc', {}).get('value', "") or "32"
        total_Cholesterol = healthdata.get('total_Cholesterol', {}).get('value', "") or "12"
        Exe = healthdata.get('Exe', {}).get('value', "") or "2"
        bmi = healthdata.get('bmi', {}).get('value', "") or "3"
        family_his = healthdata.get('family_his', {}).get('value', "") or "12"


        # ตรวจสอบว่าข้อมูลสำคัญครบหรือไม่
        required_values = [sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his]
        if any(v in ["", None, "0"] for v in required_values):
            return "ข้อมูลสุขภาพไม่ครบถ้วน", sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his

        # แปลงค่าข้อมูลเป็น float หรือ int ตามความเหมาะสม
        sbp = float(sbp) if sbp else 0.0
        dbp = float(dbp) if dbp else 0.0
        his = int(his) if his else 0
        smoke = int(smoke) if smoke else 0
        fbs = float(fbs) if fbs else 0.0
        HbAlc = float(HbAlc) if HbAlc else 0.0
        total_Cholesterol = float(total_Cholesterol) if total_Cholesterol else 0.0
        Exe = int(Exe) if Exe else 0
        bmi = float(bmi) if bmi else 0.0
        family_his = int(family_his) if family_his else 0
        print(f"sbp: {sbp}, dbp: {dbp}, his: {his}, smoke: {smoke}, fbs: {fbs}, HbAlc: {HbAlc}, total_Cholesterol: {total_Cholesterol}, Exe: {Exe}, bmi: {bmi}, family_his: {family_his}")

        cleaned_array = [float(x) if x not in ["", None] else 0.0 for x in [sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his]]
        array_np = np.asarray([cleaned_array], dtype=np.float64)

        # ทำนายผล
        prediction = Stroke_classifier.predict(array_np)

        # กำหนดข้อความผลลัพธ์
        if prediction[0] == 0:
            reply_text = "ความเสี่ยงต่ำ"
        elif prediction[0] == 1:
            reply_text = "ความเสี่ยงปานกลาง"
        else:
            reply_text = "ความเสี่ยงสูง"

        return reply_text, sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his

    else:
        return "Payload not found or is not a list", None, None, None, None, None, None, None, None, None, None

def data_bloodfat():
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

        if not healthdata:
            return "ข้อมูลสุขภาพไม่ครบถ้วน", None, None, None, None, None, None, None

        # ดึงค่าจาก healthdata สำหรับไขมันในเลือด
        Gender = healthdata.get('gender', {}).get('value', "") or ""
        Weight = healthdata.get('weight', {}).get('value', "") or ""
        Height = healthdata.get('height', {}).get('value', "") or ""
        Cholesterol = healthdata.get('cholesterol', {}).get('value', "") or ""
        Triglycerider = healthdata.get('triglyceride', {}).get('value', "") or ""
        Hdl = healthdata.get('hdl', {}).get('value', "") or ""
        Ldl = healthdata.get('ldl', {}).get('value', "") or ""

        print(f"Gender: {Gender}, Weight: {Weight}, Height: {Height}, Cholesterol: {Cholesterol}, Triglycerider: {Triglycerider}, Hdl: {Hdl}, Ldl: {Ldl}")

        # ตรวจสอบว่าข้อมูลสำคัญครบหรือไม่
        required_values = [Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl]
        if any(v in ["", None, "0"] for v in required_values):
            return "ข้อมูลสุขภาพไม่ครบถ้วน", Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl

        # แปลงค่าข้อมูลเป็น float
        Gender = int(Gender) if Gender else 0
        Weight = float(Weight) if Weight else 0.0
        Height = float(Height) if Height else 0.0
        Cholesterol = float(Cholesterol) if Cholesterol else 0.0
        Triglycerider = float(Triglycerider) if Triglycerider else 0.0
        Hdl = float(Hdl) if Hdl else 0.0
        Ldl = float(Ldl) if Ldl else 0.0

        cleaned_array = [float(x) if x not in ["", None] else 0.0 for x in [Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl]]
        array_np = np.asarray([cleaned_array], dtype=np.float64)

        # ทำนายผล
        prediction = Bloodfat_classifier.predict(array_np)

        # กำหนดข้อความผลลัพธ์
        if prediction[0] == 0:
            reply_text = "ความเสี่ยงต่ำ"
        elif prediction[0] == 1:
            reply_text = "ความเสี่ยงปานกลาง"
        else:
            reply_text = "ความเสี่ยงสูง"

        return reply_text, Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl
    

    else:
        return "Payload not found or is not a list", None, None, None, None, None, None, None

def data_diabetes():
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

        print(f"age: {age}, bmi1: {bmi1}, visceralfat1: {visceralfat1}, wrcis1: {wrcis1}, ht: {ht}, sbp1: {sbp1}, dbp1: {dbp1}, fbs1: {fbs1}, hba1c1: {hba1c1}, his: {his}")
       
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


def send_line_message(user, text):
    """ ฟังก์ชันส่งข้อความแจ้งเตือนกลับไปที่ LINE """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    message = {
        "to": user,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }
    requests.post(LINE_API_URL, headers=headers, data=json.dumps(message))

#การเปรียบเทียบ
def calculate_average(data_list):
    averages = {}
    count = len(data_list)

    for data in data_list:
        for key, value in data.items():
            if isinstance(value, (int, float)):  # เฉพาะค่าตัวเลข
                if key not in averages:
                    averages[key] = 0
                averages[key] += value

    for key in averages:
        averages[key] /= count

    return averages

def translate_keys(data, key_mapping):
    translated_data = {}
    for key, value in data.items():
        translated_key = key_mapping.get(key, key)
        translated_data[translated_key] = value
    return translated_data

# #การเปรียบเทียบโรคเบาหวาน
# def compare_and_visualize_diabetes_data():
#     req = request.get_json(silent=True, force=True)

#     # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
#     try:
#         user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
#     except (KeyError, TypeError):
#         print("❌ ไม่สามารถดึง userId จาก request ได้")
#         return None, None, None, None

#     # ดึงข้อมูลจาก MongoDB ตาม user_id
#     latest_data = Diabetes_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

#     if not latest_data:
#         print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
#         send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
#         return None, None, None, None

#     previous_data = list(Diabetes_collection.find(
#         {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
#         sort=[("timestamp", -1)]
#     ))

#     print(f"✅ ข้อมูลล่าสุด: {latest_data}")
#     print(f"📌 ข้อมูลเก่า: {previous_data}")

#     if not previous_data:
#         print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
#         send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
#         return None, None, None, None


#     # คำนวณค่าเฉลี่ย
#     previous_avg = calculate_average(previous_data)
#     latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

#     # แผนที่การแปลคีย์
#     key_mapping = {
#         "age": "อายุ",
#         "bmi": "ดัชนีมวลกาย",
#         "visceral": "ไขมันในช่องท้อง",
#         "wc": "รอบเอว",
#         "ht": "ความสูง",
#         "sbp": "ความดันตัวบน",
#         "dbp": "ความดันตัวล่าง",
#         "fbs": "น้ำตาลในเลือด",
#         "HbAlc": "ฮีโมโกลบิน A1c",
#         "family_his": "ประวัติครอบครัว"
#     }

#     # แปลคีย์ในข้อมูล
#     latest_avg = translate_keys(latest_avg, key_mapping)
#     previous_avg = translate_keys(previous_avg, key_mapping)

#     # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
#     font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"

#     # โหลดฟอนต์ที่ระบุ
#     prop = fm.FontProperties(fname=font_path)
#     prop.set_size(20)

#     # สร้างกราฟ
#     labels = [key for key in latest_avg.keys() if key != "อายุ"]
#     latest_values = [latest_avg[key] for key in labels]
#     previous_values = [previous_avg[key] for key in labels]

#     plt.figure(figsize=(8, 6))
#     plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
#     plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
#     plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
#     plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
#     plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
#     plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
#     plt.legend(prop=prop)
#     plt.tight_layout()

#     now = datetime.now()
#     formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
#     user_dir = os.path.join(f"static/{user}")
#     os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
#     graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
#     plt.savefig(graph_path)
#     plt.close()

#     print(formatted_time)
#     image_url = f"{ngrok}/{graph_path}"

#     return user, latest_avg, previous_avg, image_url

# #การเปรียบเทียบโรคไขมันในเลือด
# def compare_and_visualize_blood_fat_data():
#     req = request.get_json(silent=True, force=True)
#     # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
#     try:
#         user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
#     except (KeyError, TypeError):
#         print("❌ ไม่สามารถดึง userId จาก request ได้")
#         return None, None, None, None

#     # ดึงข้อมูลจาก MongoDB ตาม user_id
#     latest_data = blood_fat_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

#     if not latest_data:
#         print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
#         send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
#         return None, None, None, None

#     previous_data = list(blood_fat_collection.find(
#         {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
#         sort=[("timestamp", -1)]
#     ))

#     print(f"✅ ข้อมูลล่าสุด: {latest_data}")
#     print(f"📌 ข้อมูลเก่า: {previous_data}")

#     if not previous_data:
#         print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
#         send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
#         return None, None, None, None

#     # คำนวณค่าเฉลี่ย
#     previous_avg = calculate_average(previous_data)
#     latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

#     # แผนที่การแปลคีย์
#     key_mapping = {
#         "Gender": "เพศ",
#         "Weight": "น้ำหนัก",
#         "Height": "ส่วนสูง",
#         "Cholesterol": "คอเลสเตอรอล",
#         "Triglycerider": "ไตรกลีเซอไรด์",
#         "Hdl": "เอชดีแอล",
#         "Ldl": "แอลดีแอล"
#     }

#     # แปลคีย์ในข้อมูล
#     latest_avg = translate_keys(latest_avg, key_mapping)
#     previous_avg = translate_keys(previous_avg, key_mapping)

#     # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
#     font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"  # แก้ไขเส้นทางไปยังฟอนต์ไทยที่คุณใช้งาน

#     # โหลดฟอนต์ที่ระบุ
#     prop = fm.FontProperties(fname=font_path)
#     prop.set_size(20)  # ตั้งค่าขนาดตัวอักษร

#     # สร้างกราฟ
#     labels = [key for key in latest_avg.keys() if key != "อายุ"]
#     latest_values = [latest_avg[key] for key in labels]
#     previous_values = [previous_avg[key] for key in labels]

#     plt.figure(figsize=(8, 6))
#     plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
#     plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
#     plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
#     plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
#     plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
#     plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
#     plt.legend(prop=prop)
#     plt.tight_layout()
#     now = datetime.now()
#     # แสดงวันที่และเวลาในรูปแบบที่ต้องการ
#     formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
#     user_dir = os.path.join(f"static/{user}")
#     os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
#     graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
#     plt.savefig(graph_path)
#     plt.close()

#     image_url = f"{ngrok}/{graph_path}"

#     return user, latest_avg, previous_avg, image_url

# #การเปรียบเทียบโรคสมอง
# def compare_and_visualize_staggers_data():
#     req = request.get_json(silent=True, force=True)
#     # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
#     try:
#         user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
#     except (KeyError, TypeError):
#         print("❌ ไม่สามารถดึง userId จาก request ได้")
#         return None, None, None, None

#     # ดึงข้อมูลจาก MongoDB ตาม user_id
#     latest_data = Staggers_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

#     if not latest_data:
#         print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
#         send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
#         return None, None, None, None

#     previous_data = list(Staggers_collection.find(
#         {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
#         sort=[("timestamp", -1)]
#     ))

#     print(f"✅ ข้อมูลล่าสุด: {latest_data}")
#     print(f"📌 ข้อมูลเก่า: {previous_data}")

#     if not previous_data:
#         print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
#         send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
#         return None, None, None, None

#     # คำนวณค่าเฉลี่ย
#     previous_avg = calculate_average(previous_data)
#     latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

#     # แผนที่การแปลคีย์
#     key_mapping = {
#         "sbp": "ความดันตัวบน",
#         "dbp": "ความดันตัวล่าง",
#         "his": "ประวัติการรักษา",
#         "smoke": "การสูบบุหรี่",
#         "fbs": "น้ำตาลในเลือด",
#         "HbAlc": "ฮีโมโกลบิน A1c",
#         "total_Cholesterol": "คอเลสเตอรอลรวม",
#         "Exe": "การออกกำลังกาย",
#         "bmi": "ดัชนีมวลกาย",
#         "family_his": "ประวัติครอบครัว"
#     }

#     # แปลคีย์ในข้อมูล
#     latest_avg = translate_keys(latest_avg, key_mapping)
#     previous_avg = translate_keys(previous_avg, key_mapping)

#     # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
#     font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"  # แก้ไขเส้นทางไปยังฟอนต์ไทยที่คุณใช้งาน

#     # โหลดฟอนต์ที่ระบุ
#     prop = fm.FontProperties(fname=font_path)
#     prop.set_size(20)  # ตั้งค่าขนาดตัวอักษร

#     # สร้างกราฟ
#     labels = [key for key in latest_avg.keys()]
#     latest_values = [latest_avg[key] for key in labels]
#     previous_values = [previous_avg[key] for key in labels]

#     plt.figure(figsize=(8, 6))
#     plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
#     plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
#     plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
#     plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
#     plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
#     plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
#     plt.legend(prop=prop)
#     plt.tight_layout()
#     now = datetime.now()
#     # แสดงวันที่และเวลาในรูปแบบที่ต้องการ
#     formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
#     user_dir = os.path.join(f"static/{user}")
#     os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
#     graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
#     plt.savefig(graph_path)
#     plt.close()

#     image_url = f"{ngrok}/{graph_path}"

#     return user, latest_avg, previous_avg, image_url

