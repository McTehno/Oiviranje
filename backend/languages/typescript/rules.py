USER_INPUT_PATTERNS =[
        # Express / Fastify HTTP request
        r"\b(?:req|request)\s*\.\s*query\b",
        r"\b(?:req|request)\s*\.\s*body\b",
        r"\b(?:req|request)\s*\.\s*params\b",
        r"\b(?:req|request)\s*\.\s*headers\b",
        r"\b(?:req|request)\s*\.\s*cookies\b",
        r"\b(?:req|request)\s*\.\s*(?:file|files)\b",
        # Branje posamezne glave
        r"\b(?:req|request)\s*\.\s*(?:get|header)\s*\(",
        # Bracket notation:
        # req["body"], req['query']
        r"""\b(?:req|request)\s*\[\s*["'](?:query|body|params|headers|cookies|file|files)["']\s*\]""",
        # NestJS dekoratorji
        r"@Body\s*\(",
        r"@Query\s*\(",
        r"@Param\s*\(",
        r"@Headers\s*\(",
        r"@Req\s*\(",
        r"@Request\s*\(",
        r"@UploadedFile\s*\(",
        r"@UploadedFiles\s*\(",
        # Koa
        r"\bctx\s*\.\s*request\s*\.\s*body\b",
        r"\bctx\s*\.\s*request\s*\.\s*query\b",
        r"\bctx\s*\.\s*params\b",
        r"\bctx\s*\.\s*headers\b",
        r"\bctx\s*\.\s*cookies\b",
        # URL parametri
        r"\bsearchParams\s*\.\s*get\s*\(",
        r"\bURLSearchParams\s*\(",
        # Standardni vhod
        r"\bprocess\s*\.\s*stdin\b",
        r"\breadline\s*\.\s*question\s*\("
    ]

CONCAT_PATTERNS = [
        # Splošna konkatenacija z operatorjem +
        r"\+",
        # Template literal z interpolacijo:
        # `SELECT * FROM users WHERE id = ${id}`
        r"`[^`]*\$\{[^}]+\}[^`]*`",
        # String.concat(...)
        r"\.concat\s*\(",
        # Sestavljanje niza iz seznama
        r"\.join\s*\("
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
        # Neposredno uvožene funkcije:
        # import { exec } from "node:child_process"
        # const { exec } = require("child_process")
        r"\bexec\s*\(",
        r"\bexecSync\s*\(",
        r"\bspawn\s*\(",
        r"\bspawnSync\s*\(",
        r"\bexecFile\s*\(",
        r"\bexecFileSync\s*\(",
        r"\bfork\s*\(",
        # Bun
        r"\bBun\s*\.\s*spawn\s*\(",
        r"\bBun\s*\.\s*spawnSync\s*\(",
        # Deno
        r"\bDeno\s*\.\s*Command\s*\(",
        r"\bDeno\s*\.\s*run\s*\("
    ]