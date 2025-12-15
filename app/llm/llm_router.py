from app.llm.openai_client import openai_generate
from app.llm.gemini_client import gemini_generate

def generate_llm_response(prompt):
    try:
        return openai_generate(prompt)
    except Exception as e:
        print("OpenAI failed, switching to Gemini:", e)
        return gemini_generate(prompt)
