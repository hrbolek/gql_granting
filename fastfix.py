import json

with open("systemdata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

acprograms_students = data["acprograms_students"]
for item in acprograms_students:
    user_id = item.get("student_id", None)
    if user_id:
        item["user_id"] = user_id
        item["student_id"] = user_id

with open("systemdata.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)