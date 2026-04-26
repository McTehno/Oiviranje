from detectors.base import BaseDetector
from detectors.pattern_utils import (
    contains_user_input,
    contains_concatenation,
    contains_tainted_variable
)

from models.finding import Finding
from models.enums import RiskLevel, AttackType, FindingType


class SQLDetector(BaseDetector):
    def detect(self, code_lines, database="mysql"):
        findings = []

        for code_line in code_lines:
            finding = self.detect_line(code_line, database)

            if finding:
                findings.append(finding)

        return findings

    def detect_line(self, code_line, database="mysql", tainted_variables=None):
        if tainted_variables is None:
            tainted_variables = set()

        line = code_line.content

        has_sql_keyword = self.contains_strong_sql_keyword(line)
        has_user_input = contains_user_input(line, code_line.language)
        has_tainted_variable = contains_tainted_variable(line, tainted_variables)
        has_concat = contains_concatenation(line, code_line.language)

        if has_sql_keyword and has_concat and (has_user_input or has_tainted_variable):
            return Finding(
                line=code_line.number,
                type=FindingType.CONCAT,
                code=line,
                variables=list(tainted_variables),
                language=code_line.language,
                risk=RiskLevel.HIGH,
                attack_type=AttackType.SQL_INJECTION,
                description="SQL query is constructed using untrusted user input.",
                recommendation="Use parameterized queries or prepared statements."
            )

        return None

    def contains_strong_sql_keyword(self, line: str):
        strong_sql_keywords = [
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP"
        ]

        upper_line = line.upper()

        return any(
            keyword in upper_line
            for keyword in strong_sql_keywords
        )