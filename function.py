import httpx
import pickle
import numpy as np

# โหลดโมเดลที่ใช้ทำนายโรคเบาหวาน
with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_dm_risk.pkl", 'rb') as model_file:
    Diabetes_classifier = pickle.load(model_file)

with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_blood_fat.pkl", 'rb') as model_file:
    Bloodfat_classifier = pickle.load(model_file)

with open(r"/Users/masaideedoka/PROJECT/api_healthdata/model_stroke_risk.pkl", 'rb') as model_file:
    Stroke_classifier = pickle.load(model_file)

def data_stroke():
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
            return "ข้อมูลสุขภาพไม่ครบถ้วน", None, None, None, None, None, None, None, None, None


        sbp = healthdata.get('sbp', {}).get('value', "") or ""
        dbp = healthdata.get('dbp', {}).get('value', "") or ""
        his = healthdata.get('his', {}).get('value', "") or ""
        smoke = healthdata.get('smoke', {}).get('value', "") or ""
        fbs = healthdata.get('fbs', {}).get('value', "") or ""
        HbAlc = healthdata.get('HbAlc', {}).get('value', "") or ""
        total_Cholesterol = healthdata.get('total_Cholesterol', {}).get('value', "") or ""
        Exe = healthdata.get('Exe', {}).get('value', "") or ""
        bmi = healthdata.get('bmi', {}).get('value', "") or ""
        family_his = healthdata.get('family_his', {}).get('value', "") or ""


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
