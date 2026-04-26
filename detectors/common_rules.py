SQL_KEYWORDS = [
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP"
]

ORM_PATTERNS = [
    r"createQuery\s*\(",
    r"sequelize\.query\s*\(",
    r"whereRaw\s*\(",
    r"raw\s*\(",
    r"literal\s*\("
]