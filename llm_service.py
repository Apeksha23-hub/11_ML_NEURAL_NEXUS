import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
    print(f"Loaded .env from {env_path}")
else:
    print(f"Warning: .env file not found at {env_path}")

# Configure Gemini with API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_api_key_here":
    genai.configure(api_key=api_key)

def is_configured():
    key = os.getenv("GEMINI_API_KEY")
    return bool(key and key != "your_api_key_here" and len(key) > 20)

def get_insights(student_data: dict, prediction_result: dict) -> str:
    """Uses Gemini to generate personalized feedback based on ML prediction."""
    if not is_configured():
        return "LLM integration is currently disabled. Please configure your GEMINI_API_KEY in the .env file."
        
    try:
        # Using the specific model identified via list_models.py
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        student_name = student_data.get("StudentName", "the student")
        status = "At Risk" if prediction_result['at_risk'] else "Not At Risk"
        
        prompt = f"""
        You are an empathetic and supportive academic advisor AI.
        A student named {student_name} has the following academic indicators:
        {student_data}
        
        Risk Prediction: {status}
        
        Requirements for your response:
        - Keep it very concise (1-2 very short paragraphs max).
        - Use simple, non-technical language (no ML jargon).
        - Be encouraging and actionable.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating insights: {e}")
        traceback.print_exc()
        return "An error occurred while generating AI insights."

def chat_response(query: str, context: dict = None, history: list = None) -> str:
    """Handles chatbot conversation using Gemini."""
    if not is_configured():
        return "LLM integration is currently disabled. Please configure your GEMINI_API_KEY in the .env file."
        
    try:
        # Using the specific model identified via list_models.py
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Build conversation history if provided (optional for simplistic version)
        # For a full chat model, we could use model.start_chat(history=...)
        # Here we manually prepend context for a stateless-style prompt.
        
        prompt = "You are a helpful academic advisor chatbot for a Student Performance Prediction system.\n"
        if context:
            prompt += f"Context about the current student taking the test: {context}\n"
            
        if history and len(history) > 0:
            prompt += "Recent conversation history:\n"
            for msg in history[-4:]: # Keep last 4 messages to save tokens
                prompt += f"{msg.role}: {msg.content}\n"
                
        prompt += f"\nUser: {query}\nAdvisor:"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in chat response: {e}")
        traceback.print_exc()
        return "I'm sorry, I am currently experiencing technical difficulties."
