USER_INPUT_PATTERNS = [
    r"request\.GET",
    r"request\.POST",
    r"request\.args",
    r"request\.form",
    r"input\s*\("
]

CONCAT_PATTERNS = [
    r"\+",
    r"\.format\s*\(",
    r"f['\"]"
]

COMMAND_EXECUTION_PATTERNS = [
    r"os\.system\s*\(",
    r"subprocess\.run\s*\(",
    r"subprocess\.call\s*\(",
    r"subprocess\.Popen\s*\(",
    r"exec\s*\("
]