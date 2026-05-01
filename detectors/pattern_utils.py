import re

from rules.injection_rules import (
    SQL_KEYWORDS,
    USER_INPUT_PATTERNS,
    CONCAT_PATTERNS,
    ORM_PATTERNS,
    COMMAND_EXECUTION_PATTERNS,
    MONGODB_OPERATION_PATTERNS,
    MONGODB_OPERATOR_PATTERNS
)


def contains_sql_keyword(line: str):
    upper_line = line.upper()

    return any(
        keyword in upper_line
        for keyword in SQL_KEYWORDS
    )


def contains_user_input(line: str, language: str):
    patterns = USER_INPUT_PATTERNS.get(language, [])

    return any(
        re.search(pattern, line)
        for pattern in patterns
    )


def contains_concatenation(line: str, language: str):
    patterns = CONCAT_PATTERNS.get(language, [])

    return any(
        re.search(pattern, line)
        for pattern in patterns
    )


def contains_orm_pattern(line: str):
    return any(
        re.search(pattern, line)
        for pattern in ORM_PATTERNS
    )


def contains_command_execution(line: str, language: str):
    patterns = COMMAND_EXECUTION_PATTERNS.get(language, [])

    return any(
        re.search(pattern, line)
        for pattern in patterns
    )


def contains_tainted_variable(line: str, tainted_variables: set):
    for variable in tainted_variables:
        # (?<!\w) in (?!\w) delujeta podobno kot \b (word boundary), ampak ustrezno 
        # podpirata tudi z dolarjem ($) začeta imena spremenljivk (za PHP).
        pattern = r"(?<!\w)" + re.escape(variable) + r"(?!\w)"

        if re.search(pattern, line):
            return True

    return False


def contains_mongodb_operation(line: str, language: str):
    patterns = MONGODB_OPERATION_PATTERNS.get(language, [])

    return any(
        re.search(pattern, line)
        for pattern in patterns
    )


def contains_mongodb_operator(line: str):
    return any(
        re.search(pattern, line)
        for pattern in MONGODB_OPERATOR_PATTERNS
    )

