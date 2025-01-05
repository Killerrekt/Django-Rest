import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=str(os.getenv('GEMINI_KEY')))
model = genai.GenerativeModel("gemini-1.5-flash")

def GenApi(prompt): 
    response = model.generate_content(prompt)
    return response.text