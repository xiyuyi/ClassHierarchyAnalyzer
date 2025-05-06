from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)

from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from together import Together

load_dotenv()  # This will load variables from the .env file into os.environ


class TogetherQwenCoder(LLM):
    model: str = "Qwen2.5-Coder-32B-Instruct"
    max_tokens: int = (2048,)
    temperature: int = (0,)
    top_p: float = (0.95,)
    min_p: float = (0.05,)
    top_k: int = (40,)
    repetition_penalty: float = (1.1,)
    presence_penalty: int = (0,)
    frequency_penalty: int = (0,)
    seed: int = 42

    def __init__(self, **data: Any):
        super().__init__(**data)
        # anything thing that takes a string input, spits out str output put.
        self._client = Together()

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # tasek in prompt, return str output
        # the method under *._llm should vary depends on the llm definition in __init__
        response = self._client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            min_p=self.min_p,
            top_k=self.top_k,
            repetition_penalty=self.repetition_penalty,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            seed=42,
        )
        out_str = response.choices[0].message.content
        return out_str

    @property
    def _llm_type(self) -> str:
        return "template"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "min_p": self.min_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "seed": self.seed,
        }
