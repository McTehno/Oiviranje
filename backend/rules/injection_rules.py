#Rules - definirajo, kaj je sumljivo.
#Detector -uporabi ta pravila.


#besede, ki pogosto pomenijo SQL ali query.
SQL_KEYWORDS = [
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "FROM",
    "WHERE",
    "ORDER BY"
]

#vzorci, ki predstavljajo uporabniški input.
USER_INPUT_PATTERNS = {
    "python": [
        r"request\.GET",
        r"request\.POST",
        r"request\.args",
        r"request\.form",
        r"input\s*\("
    ],
    "php": [
        r"\$_GET\b",
        r"\$_POST\b",
        r"\$_REQUEST\b"
    ],

    "javascript": [
    r"\b(?:req|request)\s*\.\s*query\b",
    r"\b(?:req|request)\s*\.\s*body\b",
    r"\b(?:req|request)\s*\.\s*params\b",
    r"\b(?:req|request)\s*\.\s*headers\b",
    r"\b(?:req|request)\s*\.\s*cookies\b",
    r"\b(?:req|request)\s*\.\s*(?:file|files)\b"
],

    "java": [
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
    ],
    "typescript": [
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
}

#načini sestavljanja stringov.
'''
Python:

"SELECT ..." + user_input
"SELECT {}".format(user_input)
f"SELECT {user_input}"

JavaScript:

"SELECT " + req.query.id
`SELECT ${req.query.id}`

PHP:

"SELECT " . $_GET["id"]
'''

CONCAT_PATTERNS = {
    "python": [
        r"\+",
        r"\.format\s*\(",
        r"[fF]['\"]"
    ],
    "javascript": [
        r"\+",
        r"`[^`]*\$\{[^}]+\}[^`]*`",
        r"\.concat\s*\("
    ],
    "php": [
        r"\.",
        r'"[^"]*\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*[^"]*"',
        r'"\s*.*\{\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*\}.*"'
    ],
    "java": [
        r"\+",
        r"\bString\s*\.\s*format\s*\(",
        r"\.formatted\s*\(",
        r"\.append\s*\("
    ],
    "typescript": [
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

}

#vzorci za ORM/HQL/raw query.
ORM_PATTERNS = [
    r"createQuery\s*\(",
    r"sequelize\.query\s*\(",
    r"whereRaw\s*\(",
    r"raw\s*\(",
    r"literal\s*\("
]

#funkcije, ki lahko izvajajo sistemske ukaze
'''
Primer:

os.system(...)
subprocess.run(...)

PHP:

shell_exec(...)
system(...)

JavaScript:

child_process.exec(...)
'''


COMMAND_EXECUTION_PATTERNS = {
    "python": [
        r"os\.system\s*\(",
        r"subprocess\.run\s*\(",
        r"subprocess\.call\s*\(",
        r"subprocess\.Popen\s*\(",
        r"exec\s*\("
    ],
    "php": [
        r"shell_exec\s*\(",
        r"system\s*\(",
        r"exec\s*\(",
        r"passthru\s*\("
    ],
    "javascript": [
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
    ],

    "java": [
        # Runtime.getRuntime().exec(...)
        r"\bRuntime\s*\.\s*getRuntime\s*\(\s*\)\s*\.\s*exec\s*\(",
        # runtime.exec(...) pri prej ustvarjenem objektu Runtime
        r"\b\w+\s*\.\s*exec\s*\(",
        # ProcessBuilder
        r"\bnew\s+ProcessBuilder\s*\(",
        r"\bProcessBuilder\s*\(",
        r"\b\w+\s*\.\s*command\s*\(",
        r"\b\w+\s*\.\s*start\s*\("
    ],
    "typescript": [
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
}


MONGODB_OPERATION_PATTERNS = {
    "python": [
        r"\.find\s*\(",
        r"\.find_one\s*\(",
        r"\.aggregate\s*\(",
        r"\.update_one\s*\(",
        r"\.update_many\s*\(",
        r"\.delete_one\s*\(",
        r"\.delete_many\s*\(",
        r"\.replace_one\s*\("
    ],
    "javascript": [
        # MongoDB Native Driver in Mongoose
        r"\.find\s*\(",
        r"\.findOne\s*\(",
        r"\.findById\s*\(",
        r"\.aggregate\s*\(",
        r"\.distinct\s*\(",
        r"\.countDocuments\s*\(",
        r"\.estimatedDocumentCount\s*\(",
        # Vstavljanje
        r"\.insertOne\s*\(",
        r"\.insertMany\s*\(",
        r"\.create\s*\(",
        # Posodabljanje
        r"\.updateOne\s*\(",
        r"\.updateMany\s*\(",
        r"\.replaceOne\s*\(",
        r"\.findOneAndUpdate\s*\(",
        r"\.findByIdAndUpdate\s*\(",
        r"\.findOneAndReplace\s*\(",
        # Brisanje
        r"\.deleteOne\s*\(",
        r"\.deleteMany\s*\(",
        r"\.findOneAndDelete\s*\(",
        r"\.findByIdAndDelete\s*\(",
        # Paketne operacije
        r"\.bulkWrite\s*\("
    ],

    "java": [
        # MongoDB Java Driver
        r"\.find\s*\(",
        r"\.aggregate\s*\(",
        r"\.distinct\s*\(",
        r"\.countDocuments\s*\(",
        r"\.insertOne\s*\(",
        r"\.insertMany\s*\(",
        r"\.updateOne\s*\(",
        r"\.updateMany\s*\(",
        r"\.replaceOne\s*\(",
        r"\.findOneAndUpdate\s*\(",
        r"\.findOneAndReplace\s*\(",
        r"\.deleteOne\s*\(",
        r"\.deleteMany\s*\(",
        r"\.findOneAndDelete\s*\(",
        r"\.bulkWrite\s*\("
    ],
    "php": [
        r"->find\s*\(",
        r"->findOne\s*\(",
        r"->aggregate\s*\(",
        r"->updateOne\s*\(",
        r"->updateMany\s*\(",
        r"->deleteOne\s*\(",
        r"->deleteMany\s*\(",
        r"->replaceOne\s*\("
    ],
    "typescript": [
        # Branje
        r"\.find\s*\(",
        r"\.findOne\s*\(",
        r"\.findById\s*\(",
        r"\.aggregate\s*\(",
        r"\.distinct\s*\(",
        r"\.countDocuments\s*\(",
        r"\.estimatedDocumentCount\s*\(",
        r"\.exists\s*\(",
        # Vstavljanje
        r"\.insertOne\s*\(",
        r"\.insertMany\s*\(",
        r"\.create\s*\(",
        r"\.save\s*\(",
        # Posodabljanje
        r"\.updateOne\s*\(",
        r"\.updateMany\s*\(",
        r"\.replaceOne\s*\(",
        r"\.findOneAndUpdate\s*\(",
        r"\.findByIdAndUpdate\s*\(",
        r"\.findOneAndReplace\s*\(",
        # Brisanje
        r"\.deleteOne\s*\(",
        r"\.deleteMany\s*\(",
        r"\.findOneAndDelete\s*\(",
        r"\.findByIdAndDelete\s*\(",
        r"\.remove\s*\(",
        # Paketne operacije
        r"\.bulkWrite\s*\("
    ]
}

MONGODB_OPERATOR_PATTERNS = [
    r"\$ne",
    r"\$gt",
    r"\$gte",
    r"\$lt",
    r"\$lte",
    r"\$regex",
    r"\$where",
    r"\$or",
    r"\$and",
    r"\$in",
    r"\$nin",
    r"\$exists"
]

#MongoDB detector lahko uporablja obstoječi USER_INPUT_PATTERNS.