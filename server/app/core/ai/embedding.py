import httpx


class EmbeddingService:
    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "nomic-embed-text"
    ):
        self.base_url = base_url
        self.model = model

    async def embed(self, text: str) -> list[float]:
        timeout = httpx.Timeout(connect=10.0, read=120.0, write=10.0, pool=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]
