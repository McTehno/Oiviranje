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
    "WHERE"
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
    "javascript": [
        r"req\.query",
        r"req\.body",
        r"req\.params"
    ],
    "php": [
        r"\$_GET",
        r"\$_POST",
        r"\$_REQUEST"
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
        r"f['\"]"
    ],
    "javascript": [
        r"\+",
        r"`"
    ],
    "php": [
        r"\."
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
    "javascript": [
        r"child_process\.exec\s*\(",
        r"exec\s*\("
    ],
    "php": [
        r"shell_exec\s*\(",
        r"system\s*\(",
        r"exec\s*\(",
        r"passthru\s*\("
    ]
}