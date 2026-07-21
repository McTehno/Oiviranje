USER_INPUT_PATTERNS = [
    r"\b\w+\s*\.\s*getParameter\s*\(",
    r"\b\w+\s*\.\s*getParameterValues\s*\(",
    r"\b\w+\s*\.\s*getParameterMap\s*\(",
    r"\b\w+\s*\.\s*getHeader\s*\(",
    r"\b\w+\s*\.\s*getCookies\s*\(",
    r"\b\w+\s*\.\s*getReader\s*\(",
    r"\b\w+\s*\.\s*getInputStream\s*\(",
    r"@RequestParam\b",
    r"@PathVariable\b",
    r"@RequestBody\b",
    r"@QueryParam\b",
    r"@PathParam\b",
    r"@FormParam\b"
]

CONCAT_PATTERNS = [
        r"\+",
        r"\bString\s*\.\s*format\s*\(",
        r"\.formatted\s*\(",
        r"\.append\s*\("
]

COMMAND_EXECUTION_PATTERNS = [
        # Runtime.getRuntime().exec(...)
        r"\bRuntime\s*\.\s*getRuntime\s*\(\s*\)\s*\.\s*exec\s*\(",
        # runtime.exec(...) pri prej ustvarjenem objektu Runtime
        r"\b\w+\s*\.\s*exec\s*\(",
        # ProcessBuilder
        r"\bnew\s+ProcessBuilder\s*\(",
        r"\bProcessBuilder\s*\(",
        r"\b\w+\s*\.\s*command\s*\(",
        r"\b\w+\s*\.\s*start\s*\("
    ]