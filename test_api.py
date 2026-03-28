import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "StudyHours": 3,
    "Attendance": 70,
    "AssignmentCompletion": 60,
    "ExamScore": 45,
    "Motivation": 1,
    "StressLevel": 2,
    "OnlineCourses": 1,
    "Discussions": 2,
    "Extracurricular": 0,
    "Internet": 1,
    "Resources": 1
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
