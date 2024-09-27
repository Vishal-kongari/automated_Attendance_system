import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("C:/Users/Rammohan/projects/face_attendance_system/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://bus-safety-automation-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "23241a0533":
        {
            "name":"vishal",
            "branch":"cse",
            "mobile":8639003530,
            "last_attendance_time": "2024-09-01 00:54:34"
        },
    "852741":
        {
            "name":"emily",
            "branch":"ece",
            "mobile":8639003530,
            "last_attendance_time": "2024-09-01 00:54:34"
        },
    "963852":
        {
            "name":"elon",
            "branch":"csm",
            "mobile":8639003530,
            "last_attendance_time": "2024-09-01 00:54:34"
        }

}

for key,value in data.items():
    ref.child(key).set(value)