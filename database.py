from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Database logic
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students_v2.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Identification
    student_name = Column(String)
    
    # Input Data
    study_hours = Column(Float)
    attendance = Column(Float)
    assignments = Column(Float)
    exam_score = Column(Float)
    
    # Results
    at_risk = Column(Boolean)
    risk_probability = Column(Float)
    llm_insights = Column(String)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
