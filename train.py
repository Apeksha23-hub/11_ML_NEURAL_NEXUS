"""
Trains a Random Forest classifier on student_performance_enhanced.xlsx
Run: python model/train.py
"""
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

FEATURES = [
    "StudyHours", "Attendance", "AssignmentCompletion", "ExamScore",
    "Motivation", "StressLevel", "OnlineCourses", "Discussions",
    "Extracurricular", "Internet", "Resources"
]
TARGET = "at_risk"  # 1 = Fail (at risk), 0 = Pass

df = pd.read_excel("student_performance_enhanced.xlsx")

# Derive target: Fail => at_risk = 1
df[TARGET] = (df["Pass_Fail"] == "Fail").astype(int)

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Oversample minority class (Fail) to handle imbalance
sm = SMOTE(random_state=42)
X_train_scaled, y_train = sm.fit_resample(X_train_scaled, y_train)
print(f"After SMOTE — Pass: {(y_train==0).sum()}, Fail: {(y_train==1).sum()}")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred, target_names=["Pass (Not At Risk)", "Fail (At Risk)"]))

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(FEATURES, "model/features.pkl")
print("Model, scaler, and feature list saved to model/")
