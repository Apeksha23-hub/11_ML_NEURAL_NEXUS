from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from api.schemas import StudentInput, PredictionResult
from api.predictor import predict
from api.chatbot import router as chatbot_router
from api.llm_service import get_insights
from api import database

# Initialize database
database.init_db()

app = FastAPI(
    title="Student Performance Prediction API",
    description="Predicts student at-risk status based on academic indicators.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
os.makedirs(frontend_path, exist_ok=True)
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/health")
def root():
    return {"message": "Student Performance Prediction API is running."}

@app.post("/predict", response_model=PredictionResult)
def predict_performance(student: StudentInput, db: Session = Depends(database.get_db)):
    """
    Submit student academic data and receive a risk prediction with recommendations.
    """
    # Strip name for ML prediction (only numbers allowed)
    ml_input = student.model_dump()
    ml_input.pop("StudentName", None)
    
    result = predict(ml_input)
    
    # Generate insights using Gemini
    llm_insights = get_insights(student.model_dump(), result)
    result["llm_insights"] = llm_insights
    
    # --- Persistence Block ---
    try:
        history_entry = database.PredictionHistory(
            student_name=student.StudentName,
            study_hours=student.StudyHours,
            attendance=student.Attendance,
            assignments=student.AssignmentCompletion,
            exam_score=student.ExamScore,
            at_risk=bool(result['at_risk']),
            risk_probability=float(result['risk_probability']),
            llm_insights=llm_insights
        )
        db.add(history_entry)
        db.commit()
    except Exception as e:
        print(f"Database error: {e}")
    # -------------------------
    
    return result

@app.get("/history")
async def get_history(db: Session = Depends(database.get_db)):
    """Fetch recent student records for monitoring."""
    records = db.query(database.PredictionHistory).order_by(database.PredictionHistory.timestamp.desc()).limit(20).all()
    # Simple JSON serialization for the response
    return [{
        "timestamp": r.timestamp.strftime("%H:%M:%S"),
        "student_name": r.student_name,
        "exam_score": r.exam_score,
        "at_risk": r.at_risk,
        "risk_probability": r.risk_probability
    } for r in records]
