def format(value) -> str:
    if value is None:
        return "NULL"

    if isinstance(value, str):
        value = value.replace("'", "''")
        return f"'{value}'"

    return str(value)