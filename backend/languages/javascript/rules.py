
USER_INPUT_PATTERNS = [
    r"\b(?:req|request)\s*\.\s*query\b",
    r"\b(?:req|request)\s*\.\s*body\b",
    r"\b(?:req|request)\s*\.\s*params\b",
    r"\b(?:req|request)\s*\.\s*headers\b",
    r"\b(?:req|request)\s*\.\s*cookies\b",
    r"\b(?:req|request)\s*\.\s*(?:file|files)\b"
]

CONCAT_PATTERNS = [
        r"\+",
        r"`[^`]*\$\{[^}]+\}[^`]*`",
        r"\.concat\s*\("
    ]

COMMAND_EXECUTION_PATTERNS = [
        # child_process.exec(...)
        r"\bchild_process\s*\.\s*exec\s*\(",
        r"\bchild_process\s*\.\s*execSync\s*\(",
        r"\bchild_process\s*\.\s*spawn\s*\(",
        r"\bchild_process\s*\.\s*spawnSync\s*\(",
        r"\bchild_process\s*\.\s*execFile\s*\(",
        r"\bchild_process\s*\.\s*execFileSync\s*\(",
        r"\bchild_process\s*\.\s*fork\s*\(",
        # Destrukturirani ali neposredno uvoženi klici:
        # const { exec } = require("child_process")
        # import { exec } from "node:child_process"
        r"\b(?:exec|execSync|spawn|spawnSync|execFile|execFileSync|fork)\s*\("
    ]