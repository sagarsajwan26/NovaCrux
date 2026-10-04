import asyncio

from app.core.ai.embedding import EmbeddingService


async def main():
    service = EmbeddingService()

    embedding = await service.embed("NovaCrux is a multi-tenant AI business platform.")

    print("Embedding dimension:", len(embedding))
    print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    asyncio.run(main())
