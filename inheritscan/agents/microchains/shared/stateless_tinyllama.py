from typing import Any, Dict, List, Optional

import requests
from langchain_core.language_models.llms import LLM


class StatelessOllamaLLM(LLM):
    model: str = "tinyllama"
    host: str = "http://localhost:11434"
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = 0
    num_predict: int = 150
    stop: Optional[List[str]] = ["Explanation complete.", "\n\n"]

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "num_predict": self.num_predict,
                "stop": stop or self.stop,
            },
            "context": None,  # 💥 clears any residual memory
        }

        response = requests.post(f"{self.host}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()["response"]

    @property
    def _llm_type(self) -> str:
        return "stateless_ollama"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "host": self.host,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "num_predict": self.num_predict,
            "stop": self.stop,
        }
