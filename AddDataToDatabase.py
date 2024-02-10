import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facerecognition-f3cd2-default-rtdb.asia-southeast1.firebasedatabase.app/"})

ref = db.reference('Students')

data = {
    "Somil":
        {
            "Name":"Somil Kumar",
            "rollno":"102203221",
            "Department":"computer",
            "MobileNumber":"7838610837"
        },
    "Sanidhiya":
        {
            "Name":"Sanidhiya Gupta",
            "rollno":"102203605",
            "Department":"computer",
            "MobileNumber":"9518846447"
        },
    "pratyush":
        {
            "Name":"Pratyush Sharma",
            "rollno":"102203958",
            "Department":"computer",
            "MobileNumber":"8082022274"
        },
    "mannat":
        {
            "Name":"Mannat Sharma",
            "rollno":"102217229",
            "Department":"cse",
            "MobileNumber":"9086998768"
        }
}

for key,value in data.items():
    ref.child(key).set(value)