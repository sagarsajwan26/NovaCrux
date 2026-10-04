from app.core.vector.service import QdrantService


def main():
    service = QdrantService()

    embedding = [0.0] * 768

    service.upsert_embedding(
        point_id=1,
        embedding=embedding,
        payload={
            "tenant_id": 1,
            "document_id": 1,
            "document_version_id": 1,
            "chunk_id": 1,
            "chunk_index": 0,
        },
    )

    print("Successfully inserted test vector.")

    results = service.search(
        embedding=embedding,
        limit=5,
    )

    print("Search results:")

    for result in results:
        print(
            "ID:",
            result.id,
            "Score:",
            result.score,
            "Payload:",
            result.payload,
        )


if __name__ == "__main__":
    main()
