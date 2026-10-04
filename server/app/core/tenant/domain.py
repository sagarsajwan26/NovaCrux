def normalize_domain(domain: str) -> str:
    domain = domain.strip().lower()

    if "://" in domain:
        domain = domain.split("://", 1)[1]

    domain = domain.split("/", 1)[0]

    if ":" in domain:
        domain = domain.split(":", 1)[0]
    return domain
