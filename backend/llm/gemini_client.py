import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class GeminiClient:
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found")
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"Gemini client initialized with model: {model_name}")

    def generate_content(self, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                logger.info("Successfully generated content")
                return response.text
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return f"Error after {max_retries} attempts: {str(e)}"