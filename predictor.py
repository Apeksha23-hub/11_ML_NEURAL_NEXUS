import joblib
import numpy as np
import pandas as pd

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "model", "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "model", "scaler.pkl"))
FEATURES = joblib.load(os.path.join(BASE_DIR, "model", "features.pkl"))

# Lower threshold to improve recall on at-risk students
AT_RISK_THRESHOLD = 0.20

def get_recommendations(data: dict, at_risk: bool) -> list[str]:
    recs = []
    if data["Attendance"] < 75:
        recs.append("Attendance is below 75% — try to attend more classes consistently.")
    if data["AssignmentCompletion"] < 70:
        recs.append("Complete more assignments; aim for at least 70% completion rate.")
    if data["ExamScore"] < 50:
        recs.append("Exam score is low — consider joining study groups or seeking tutoring.")
    if data["StudyHours"] < 4:
        recs.append("Increase daily study hours to at least 4 hours for better retention.")
    if data["Motivation"] == 0:
        recs.append("Low motivation detected — set short-term goals and reward progress.")
    if data["StressLevel"] >= 2:
        recs.append("High stress level — explore stress management techniques or counseling.")
    if data["Internet"] == 0:
        recs.append("No internet access — visit campus labs or library for online resources.")
    if data["Resources"] == 0:
        recs.append("Lack of learning resources — request materials from your institution.")
    if not recs and at_risk:
        recs.append("Consult with your academic advisor for a personalized improvement plan.")
    if not at_risk and not recs:
        recs.append("Great performance — keep up your current study habits.")
    return recs

def predict(input_data: dict) -> dict:
    X = pd.DataFrame([input_data], columns=FEATURES)
    X_scaled = scaler.transform(X)
    prob = float(model.predict_proba(X_scaled)[0][1])
    at_risk = prob >= AT_RISK_THRESHOLD
    return {
        "at_risk": at_risk,
        "risk_probability": round(prob, 4),
        "label": "At Risk (Fail)" if at_risk else "Not At Risk (Pass)",
        "recommendations": get_recommendations(input_data, at_risk)
    }
