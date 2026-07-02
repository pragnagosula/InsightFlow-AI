import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content("Hello")
    print(response.text)
except Exception as e:
    print(e)