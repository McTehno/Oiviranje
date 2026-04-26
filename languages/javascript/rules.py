USER_INPUT_PATTERNS = [
    r"req\.query",
    r"req\.body",
    r"req\.params"
]

CONCAT_PATTERNS = [
    r"\+",
    r"`"
]

COMMAND_EXECUTION_PATTERNS = [
    r"child_process\.exec\s*\(",
    r"exec\s*\("
]