import requests
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("OllamaClient")

class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434", model: str = "qwen2.5-coder:7b"):
        self.host = host
        self.model = model
        self.api_url = f"{self.host}/api/generate"
        self.chat_url = f"{self.host}/api/chat"
        
    def check_health(self) -> bool:
        """Ping the local Ollama server to ensure it is running."""
        try:
            resp = requests.get(self.host)
            return resp.status_code == 200
        except requests.ConnectionError:
            return False

    def generate_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Send a ChatML formatted message array to the local model."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
            "options": {
                "num_ctx": 4096, # Expanded context window for RAG seeds
                "top_p": 0.95
            }
        }
        
        try:
            response = requests.post(self.chat_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except requests.Timeout:
            logger.error("Ollama generation timed out. Is the GPU overloaded?")
            return ""
        except Exception as e:
            logger.error(f"Failed to communicate with Ollama: {e}")
            return ""
