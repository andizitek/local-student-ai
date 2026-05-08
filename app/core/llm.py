import requests

OLLAMA_URL = "http://localhost:11434"


def embed_text(text: str, model: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": model, "input": text},
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()
    embeddings = data.get("embeddings", [])
    if not embeddings:
        raise RuntimeError("Keine Embeddings von Ollama erhalten.")
    return embeddings[0]


def chat_with_ollama(
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature},
        },
        timeout=900,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]