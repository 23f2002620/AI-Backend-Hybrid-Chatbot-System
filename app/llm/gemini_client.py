from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def gemini_generate(prompt):
    model = "gemini-2.5-flash"  
    response = client.models.generate_content(  
        model=model,
        contents=prompt 
    )
    return response.text
