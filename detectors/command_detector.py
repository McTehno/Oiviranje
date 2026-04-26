from detectors.base import BaseDetector
from detectors.pattern_utils import (
    contains_command_execution,
    contains_user_input,
    contains_tainted_variable
)

from models.finding import Finding
from models.enums import RiskLevel, AttackType, FindingType


class CommandDetector(BaseDetector):
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

        has_command_execution = contains_command_execution(line, code_line.language)
        has_user_input = contains_user_input(line, code_line.language)
        has_tainted_variable = contains_tainted_variable(line, tainted_variables)

        if has_command_execution and (has_user_input or has_tainted_variable):
            return Finding(
                line=code_line.number,
                type=FindingType.EXEC,
                code=line,
                variables=list(tainted_variables),
                language=code_line.language,
                risk=RiskLevel.HIGH,
                attack_type=AttackType.COMMAND_INJECTION,
                description="User input is passed directly to an operating system command.",
                recommendation="Avoid passing user input directly to system commands."
            )

        return None