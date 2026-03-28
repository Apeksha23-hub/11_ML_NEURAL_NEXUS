from pydantic import BaseModel, Field

class StudentInput(BaseModel):
    StudentName: str = "Unknown Student"
    StudyHours: float = Field(..., ge=0, le=24, description="Daily study hours")
    Attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    AssignmentCompletion: float = Field(..., ge=0, le=100, description="Assignment completion rate (%)")
    ExamScore: float = Field(..., ge=0, le=100, description="Exam score (0-100)")
    Motivation: int = Field(..., ge=0, le=3, description="Motivation level (0=Low, 1=Medium, 2=High, 3=Very High)")
    StressLevel: int = Field(..., ge=0, le=3, description="Stress level (0=Low, 1=Medium, 2=High, 3=Very High)")
    OnlineCourses: int = Field(..., ge=0, description="Number of online courses taken")
    Discussions: int = Field(..., ge=0, description="Number of discussion participations")
    Extracurricular: int = Field(..., ge=0, le=1, description="Participates in extracurricular (0=No, 1=Yes)")
    Internet: int = Field(..., ge=0, le=1, description="Has internet access (0=No, 1=Yes)")
    Resources: int = Field(..., ge=0, le=1, description="Has access to learning resources (0=No, 1=Yes)")

class PredictionResult(BaseModel):
    at_risk: bool
    risk_probability: float
    label: str
    recommendations: list[str]
    llm_insights: str = None

class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    query: str
    context: dict = None
    history: list[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str
