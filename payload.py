#เช็คโรคเบาหวาน
def flex_predict_diabetes(reply_text, reply_text_color):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "ความเสี่ยงโรคเบาหวาน",
                    "size": "lg"
                    },
                    {
                    "type": "text",
                    "text": reply_text,
                    "color": reply_text_color,
                    "weight": "bold",
                    "size": "lg",
                    "offsetStart": "md"
                    }
                ],
                "margin": "md"
                }
            ],
            "margin": "none"
            }
        }
    }

def flex_analysis_data_diabetes(age, bmi1, visceralfat1, wrcis1, ht, sbp1, dbp1, fbs1, hba1c1, his, colors):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "เพศ:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{age}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ดัชนีมวลกาย:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{bmi1}", "color": f"{colors['bmi']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "Visceral Fat:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{visceralfat1}", "color": f"{colors['visceral']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "รอบเอาต่อความสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{wrcis1}", "color": f"{colors['wc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "โรคความดันโลหิตสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{ht}", "color": f"{colors['ht']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงบน:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{sbp1}", "color": f"{colors['sbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงล่าง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{dbp1}", "color": f"{colors['dbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำตาลในเลือดก่อนอาหาร:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{fbs1}", "color": f"{colors['fbs']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ระดับน้ำตาลสะสมนเลือด:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{hba1c1}", "color": f"{colors['HbAlc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ประวัติเบาหวานในครอบครัว:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{his}", "color": f"{colors['family_his']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_diabetes(recommendations):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อแนะนำ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
            }
        }
    }



def flex_predict_bloodfat(reply_text, reply_text_color):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "ความเสี่ยงไขมันในเลือดสูง",
                    "size": "lg"
                    },
                    {
                    "type": "text",
                    "text": reply_text,
                    "color": reply_text_color,
                    "weight": "bold",
                    "size": "lg",
                    "offsetStart": "md"
                    }
                ],
                "margin": "md"
                }
            ],
            "margin": "none"
            }
        }
    }

def flex_analysis_data_bloodfat(Gender, Weight, Height, Cholesterol, Triglycerider, Hdl, Ldl, colors):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "เพศ:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Gender}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำหนัก:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Weight}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ส่วนสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Height}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "คอเลสเตอรอล:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Cholesterol}", "color": f"{colors['Cholesterol']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ไตรกลีเซอไรด์:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Triglycerider}", "color": f"{colors['Triglycerider']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "HDL:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Hdl}", "color": f"{colors['Hdl']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "LDL:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Ldl}", "color": f"{colors['Ldl']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_bloodfat(recommendations):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อแนะนำ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
            }
        }
    }



def flex_predict_stroke(reply_text, reply_text_color):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "ความเสี่ยงโรคหลอดเลือดสมอง",
                    "size": "lg"
                    },
                    {
                    "type": "text",
                    "text": reply_text,
                    "color": reply_text_color,
                    "weight": "bold",
                    "size": "lg",
                    "offsetStart": "md"
                    }
                ],
                "margin": "md"
                }
            ],
            "margin": "none"
            }
        }
    }

def flex_analysis_data_stroke(sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his, colors):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงบน:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{sbp}", "color": f"{colors['sbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงล่าง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{dbp}", "color": f"{colors['dbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ประวัติการรักษา", "wrap": True, "flex": 3}, {"type": "text", "text": f"{his}", "color": f"{colors['his']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "การสูบบุหรี่", "wrap": True, "flex": 3}, {"type": "text", "text": f"{smoke}", "color": f"{colors['smoke']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำตาลในเลือด", "wrap": True, "flex": 3}, {"type": "text", "text": f"{fbs}", "color": f"{colors['fbs']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ฮีโมโกลบิน A1c:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{HbAlc}", "color": f"{colors['HbAlc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "คอเลสเตอรอลรวม:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{total_Cholesterol}", "color": f"{colors['total_Cholesterol']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "การออกกำลังกาย", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Exe}", "color": f"{colors['Exe']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ดัชนีมวลกาย:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{bmi}", "color": f"{colors['bmi']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ประวัติครอบครัว", "wrap": True, "flex": 3}, {"type": "text", "text": f"{family_his}", "color": f"{colors['family_his']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_stroke(recommendations):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อแนะนำ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
            }
        }
    }
