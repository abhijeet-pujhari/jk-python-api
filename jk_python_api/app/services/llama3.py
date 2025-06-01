# Llama3 integration logic

import httpx
from app.core.config import settings

async def generate_summary(text: str) -> str:
    """
    Generate a summary using a local Llama3 (Ollama) model.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.LLAMA3_API_URL,
                json={"model": "llama3", "prompt": text, "stream": False}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
    except Exception as e:
        return f"Error generating summary: {str(e)}"
