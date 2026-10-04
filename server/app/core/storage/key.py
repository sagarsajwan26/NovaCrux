def document_version_key(
    tenant_id: int,
    document_id: int,
    version_id: int,
    filename: str,
) -> str:
    return (
        f"tenants/{tenant_id}/"
        f"documents/{document_id}/"
        f"versions/{version_id}/"
        f"{filename}"
    )
