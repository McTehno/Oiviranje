USER_INPUT_PATTERNS = [
    r"\$_GET",
    r"\$_POST",
    r"\$_REQUEST"
]

CONCAT_PATTERNS = [
    r"\."
]

COMMAND_EXECUTION_PATTERNS = [
    r"shell_exec\s*\(",
    r"system\s*\(",
    r"exec\s*\(",
    r"passthru\s*\("
]