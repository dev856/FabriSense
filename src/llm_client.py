"""Vision LLM client abstraction for Gemini, OpenAI, and Ollama."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

from PIL import Image

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - depends on local environment

    def load_dotenv() -> None:
        return None


from src.image_preprocessor import ImagePreprocessor

load_dotenv()


class LLMClient:
    """Unified client for supported multimodal providers."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower()
        self.model = None
        self.client = None
        self.model_name = None
        self.gemini_model_candidates: list[str] = []
        self._setup_client()

    def _setup_client(self) -> None:
        if self.provider == "gemini":
            import google.generativeai as genai

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY is not configured.")

            genai.configure(api_key=api_key)
            self.client = genai

            configured = os.getenv("GEMINI_MODEL", "").strip()
            candidates = [
                configured,
                "gemini-2.5-flash",
                "gemini-flash-latest",
                "gemini-2.0-flash",
                "gemini-1.5-flash-latest",
            ]
            self.gemini_model_candidates = []
            for candidate in candidates:
                if candidate and candidate not in self.gemini_model_candidates:
                    self.gemini_model_candidates.append(candidate)
            self.model_name = self.gemini_model_candidates[0]
            return

        if self.provider == "openai":
            from openai import OpenAI

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is not configured.")
            self.client = OpenAI(api_key=api_key)
            self.model_name = "gpt-4o-mini"
            return

        if self.provider == "ollama":
            import ollama

            self.client = ollama.Client(
                host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
            self.model_name = "llava:13b"
            return

        raise ValueError(f"Unsupported provider: {self.provider}")

    def analyze_image(
        self, image: Image.Image, prompt: str, max_retries: int = 3
    ) -> Dict[str, Any]:
        last_error: Optional[str] = None
        attempt_prompt = prompt

        for attempt in range(max_retries):
            try:
                raw_response = self._call_api(image, attempt_prompt)
                return self._parse_json_response(raw_response)
            except json.JSONDecodeError as exc:
                last_error = f"JSON parse error: {exc}"
                attempt_prompt += "\n\nReturn valid JSON only. Do not wrap the response in code fences."
            except Exception as exc:
                last_error = str(exc)
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)

        raise RuntimeError(
            f"LLM analysis failed after {max_retries} attempts. Last error: {last_error}"
        )

    def _call_api(self, image: Image.Image, prompt: str) -> str:
        if self.provider == "gemini":
            last_error: Optional[Exception] = None
            for candidate in self.gemini_model_candidates:
                try:
                    model = self.client.GenerativeModel(candidate)
                    response = model.generate_content(
                        [prompt, image],
                        generation_config={
                            "temperature": 0.2,
                            "max_output_tokens": 4096,
                            "response_mime_type": "application/json",
                        },
                    )
                    self.model_name = candidate
                    return response.text
                except Exception as exc:
                    last_error = exc
                    continue

            raise RuntimeError(
                "No working Gemini model was accepted. Set GEMINI_MODEL in .env to a valid vision model for your account. "
                f"Tried: {', '.join(self.gemini_model_candidates)}. Last error: {last_error}"
            )

        if self.provider == "openai":
            image_b64 = ImagePreprocessor.image_to_base64(image)
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=0.2,
                max_tokens=4096,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                ],
            )
            return response.choices[0].message.content or "{}"

        if self.provider == "ollama":
            image_b64 = ImagePreprocessor.image_to_base64(image)
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_b64],
                    }
                ],
                options={"temperature": 0.2},
            )
            return response["message"]["content"]

        raise ValueError(f"Unsupported provider: {self.provider}")

    def _parse_json_response(self, raw_response: str) -> Dict[str, Any]:
        text = raw_response.strip()

        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text.strip())
