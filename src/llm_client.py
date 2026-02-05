"""
LLM Client for Google Gemini API (Updated for google-genai package)
"""
import os
import json
from typing import Optional, Dict, Any
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv


class LLMClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, log_file: str = "logs/genai_log.md"):
        load_dotenv()
        
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.log_file = log_file
        self._initialize_log()
    
    def _initialize_log(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("# GenAI Prompt Log\n\n")
                f.write(f"**LLM Used:** Google Gemini ({self.model_name})\n\n")
                f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
    
    def _log_interaction(self, prompt: str, response: str, purpose: str):
        with open(self.log_file, 'a') as f:
            f.write(f"## {purpose}\n\n")
            f.write(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"### Prompt:\n```\n{prompt}\n```\n\n")
            f.write(f"### Response:\n```\n{response}\n```\n\n---\n\n")
    
    def generate(self, prompt: str, purpose: str = "General", temperature: float = 0.7) -> str:
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=8000,
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            response_text = response.text
            self._log_interaction(prompt, response_text, purpose)
            return response_text
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ {error_msg}")
            self._log_interaction(prompt, f"ERROR: {error_msg}", purpose)
            raise
    
    def generate_json(self, prompt: str, purpose: str = "JSON Generation") -> Dict[str, Any]:
        json_prompt = f"{prompt}\n\nRespond with ONLY valid JSON, no markdown."
        response_text = self.generate(json_prompt, purpose, temperature=0.3)
        
        cleaned = response_text.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            return {"error": "Failed to parse JSON", "raw_response": cleaned}
