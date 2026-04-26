from detectors.base import BaseDetector
from detectors.pattern_utils import (
    contains_orm_pattern,
    contains_user_input,
    contains_concatenation,
    contains_tainted_variable
)

from models.finding import Finding
from models.enums import RiskLevel, AttackType, FindingType


class HQLDetector(BaseDetector):
    def detect(self, code_lines, database="mysql"):
        findings = []

        for code_line in code_lines:
            finding = self.detect_line(code_line)

            if finding:
                findings.append(finding)

        return findings

    def detect_line(self, code_line, tainted_variables=None):
        if tainted_variables is None:
            tainted_variables = set()

        line = code_line.content

        has_orm = contains_orm_pattern(line)
        has_user_input = contains_user_input(line, code_line.language)
        has_tainted_variable = contains_tainted_variable(line, tainted_variables)
        has_concat = contains_concatenation(line, code_line.language)

        if has_orm and (
            (has_user_input and has_concat)
            or has_tainted_variable
        ):
            return Finding(
                line=code_line.number,
                type=FindingType.RAW_QUERY,
                code=line,
                variables=list(tainted_variables),
                language=code_line.language,
                risk=RiskLevel.HIGH,
                attack_type=AttackType.HQL_INJECTION,
                description="ORM/HQL query is constructed using untrusted user input.",
                recommendation="Use safe ORM parameters instead of string concatenation."
            )

        return None