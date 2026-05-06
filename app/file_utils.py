import os

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",
    ".tsx": "javascript",
    ".php": "php",
}

SUPPORTED_EXTENSIONS = set(EXTENSION_LANGUAGE_MAP.keys())

IGNORED_DIRS = {
    "node_modules",
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


def detect_language_from_file(file_path: str):
    _, extension = os.path.splitext(file_path)
    return EXTENSION_LANGUAGE_MAP.get(extension.lower())


def is_supported_code_file(file_path: str):
    _, extension = os.path.splitext(file_path)
    return extension.lower() in SUPPORTED_EXTENSIONS