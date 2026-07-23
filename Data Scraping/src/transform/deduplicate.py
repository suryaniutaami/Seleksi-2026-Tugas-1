def deduplicate_by_keys(data: list[dict], keys: tuple[str, ...],) -> list[dict]:
    """Memastikan setiap kombinasi key tertentu pada record bernilai unik"""
    result: list[dict] = []
    seen: set[tuple] = set()

    for index, item in enumerate(data):
        key = tuple(item.get(column) for column in keys)

        if any(value is None or value == "" for value in key):
            raise ValueError(
                f"Record ke-{index} memiliki key wajib kosong: {key}"
            )

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result