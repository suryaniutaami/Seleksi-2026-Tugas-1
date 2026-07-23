def parse_grips(raw_grips: str | None) -> list[str]:
    """
    Memecah atribut grips yang dipisahkan dengan koma.
    """
    if raw_grips is None:
        return []

    result: list[str] = []

    for grip in raw_grips.split(","):
        grip = grip.strip()

        if grip:
            result.append(grip)

    return result
