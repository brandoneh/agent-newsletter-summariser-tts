import os
import json
import re
import requests
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path


load_dotenv()
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"


def load_system_prompt() -> str:
    path = Path(__file__).parent / "newsletter_system_prompt.md"
    return path.read_text(encoding="utf-8")


def summarise(email_text: str, url: str, model: str, api_token: str = None) -> dict:
    system_prompt = load_system_prompt()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": email_text},
        ],
        # Lower temperature = more deterministic output. Important for structured JSON.
        # 0.3 is a good starting point for summarisation tasks.
        "temperature": 0.3,
    }

    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
    response = requests.post(url, json=payload, headers=headers)

    if not response.ok:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")

    # The model's reply is nested inside choices[0].message.content
    content = response.json()["choices"][0]["message"]["content"]

    # Models often wrap JSON in markdown code fences (```json ... ```)
    # This strips them out before parsing
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
    json_str = json_match.group(1) if json_match else content

    result = json.loads(json_str)

    # Inject timestamp in Python — the model doesn't know the current time reliably
    result["processed_at"] = datetime.now().isoformat(timespec="seconds")

    return result


if __name__ == "__main__":

    model = os.getenv("MODEL")

    api_token = os.getenv("GEMINI_API_KEY")
    url = GEMINI_URL if api_token else OLLAMA_URL

    # Hardcoded test input — lets us iterate on prompt quality without running the full pipeline
    test_email = """
    Subject: The Batch - Issue 247

    Dear Reader,

    This week, Meta released Llama 3.1, a new family of open-source models including a 405B parameter
    flagship that Meta claims outperforms GPT-4o on several benchmarks. The weights are freely available
    for download, which is significant for developers wanting to run powerful models locally.

    Separately, Mistral announced a new 7B model fine-tuned specifically for code generation, showing
    strong results on HumanEval. It runs comfortably on consumer hardware with 8GB VRAM.

    In industry news, Google DeepMind published research on 'AlphaProof', a system that achieved
    silver-medal performance on the 2024 International Mathematical Olympiad — a long-standing benchmark
    for reasoning capability.

    Finally, a practical tip: if you are building RAG pipelines, the new LangChain v0.2 release
    significantly simplifies the retrieval chain API and is worth upgrading to.
    """

    result = summarise(test_email, url, model, api_token)
    print(json.dumps(result, indent=2))
