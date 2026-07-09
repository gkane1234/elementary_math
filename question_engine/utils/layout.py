def resolve_column_count(question_count: int, setting: str | int | float) -> int:
    if question_count <= 1:
        return 1

    if isinstance(setting, str) and setting.lower() == "auto":
        if question_count <= 4:
            return 1
        if question_count <= 10:
            return min(2, question_count)
        return min(3, question_count)

    requested = max(1, min(3, int(setting)))
    return min(requested, question_count)
