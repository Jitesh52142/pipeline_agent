import os
import logging
import time
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class LLMInterface:
    """
    Revised LLM Interface using Gemini-2.5-flash as the primary engine.
    """
    def __init__(self, temperature=0.3):
        # 1. Primary Model: Gemini-2.5-Flash (User Request)
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=temperature
        )
        
        # 2. Fallback: Grok (Plain Requests)
        self.x_ai_key = os.getenv("X_AI_API_KEY")
        self.temperature = temperature
        if self.x_ai_key:
            logging.info("LLMInterface: Grok failover using requests initialized.")

    def _call_grok(self, prompt):
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.x_ai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok-beta",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Grok API Error ({response.status_code}): {response.text}")

    def generate(self, prompt, attempt=1):
        try:
            # 1. Try Gemini-2.5
            logging.info(f"LLMInterface (Attempt {attempt}): Using Gemini-2.5-Flash")
            return self.gemini.invoke(prompt).content
            
        except Exception as e:
            logging.warning(f"Google AI Issue: {e}")
            
            # 2. Try Grok (Via Requests)
            if self.x_ai_key:
                try:
                    logging.info(f"LLMInterface (Attempt {attempt}): Falling back to Grok (Requests)")
                    return self._call_grok(prompt)
                except Exception as grok_err:
                    logging.warning(f"Grok Issue: {grok_err}")
            
            # 3. Retry Logic
            if attempt < 3:
                wait = 15 * attempt
                logging.warning(f"All AI exhausted. Waiting {wait}s...")
                time.sleep(wait)
                return self.generate(prompt, attempt + 1)
            
            raise Exception("Critical: AI Provider Quotas Fully Exhausted.")
