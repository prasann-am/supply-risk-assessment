# -*- coding: utf-8 -*-
"""

"""
from google import genai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize Gemini API client (assuming you have a key for Google Gemini)

GOOGLEAI_API_KEY = os.getenv("GOOGLEAI_API_KEY")
client = genai.Client(api_key=GOOGLEAI_API_KEY)

def process_with_gemini(prompt):


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response