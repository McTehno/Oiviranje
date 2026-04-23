# vsi scenariji (3) tukaj

"""
DEFINICIJA VSEH ATTACK SCENARIOV
"""

RULES = [

    # SQL Injection
    {
        "name": "SQL_INJECTION",
        "keywords": ["SELECT", "INSERT", "UPDATE", "DELETE"],
        "concat_required": True,
        "input_required": True,
        "risk": "HIGH"
    },

    # HQL Injection
    {
        "name": "HQL_INJECTION",
        "keywords": ["createQuery"],
        "concat_required": True,
        "input_required": True,
        "risk": "HIGH"
    },

    # Command Injection
    {
        "name": "COMMAND_INJECTION",
        "keywords": ["exec", "Runtime.getRuntime"],
        "concat_required": True,
        "input_required": True,
        "risk": "CRITICAL"
    }
]