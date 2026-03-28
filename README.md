# P-02: Student Performance Prediction & Monitoring System

## Setup

```bash
pip install -r requirements.txt
```

## Steps

### 1. Generate synthetic data
```bash
python data/generate_data.py
```

### 2. Train the model
```bash
python model/train.py
```

### 3. Run the API
```bash
uvicorn api.main:app --reload
```

Then open http://localhost:8000/docs for the interactive Swagger UI.

## API Usage

POST `/predict`

```json
{
  "StudyHours": 3.5,
  "Attendance": 65,
  "AssignmentCompletion": 50,
  "ExamScore": 45,
  "Motivation": 1,
  "StressLevel": 2,
  "OnlineCourses": 1,
  "Discussions": 5,
  "Extracurricular": 0,
  "Internet": 1,
  "Resources": 0
}
```

Response:
```json
{
  "at_risk": true,
  "risk_probability": 0.87,
  "label": "At Risk",
  "recommendations": [
    "Improve attendance — aim for at least 75%.",
    "Complete all assignments; consider forming a study group.",
    "Seek tutoring or extra help sessions for exam preparation."
  ]
}
```
