from parsers.python_parser import PythonParser
from parsers.js_parser import JSParser
from parsers.php_parser import PHPParser

from detectors.injection_detector import InjectionDetector
from models.result import AnalysisResult
from models.enums import RiskLevel, AttackType


class Analyzer:
    def analyze(self, code: str, language: str, database: str = "mysql"):
        parser = self.get_parser(language)

        code_lines = parser.parse(code)

        detector = InjectionDetector()
        findings = detector.detect(code_lines, database)

        detected_scenarios = self.get_detected_scenarios(findings)

        result = AnalysisResult(
            findings=findings,
            total_findings=len(findings),
            overall_risk=self.calculate_overall_risk(detected_scenarios),
            score=self.calculate_score(detected_scenarios),
            detected_scenarios=detected_scenarios
        )

        return result

    def get_parser(self, language: str):
        if language == "python":
            return PythonParser()

        if language == "javascript":
            return JSParser()

        if language == "php":
            return PHPParser()

        raise ValueError(f"Unsupported language: {language}")

    def get_detected_scenarios(self, findings):
        scenarios = set()

        for finding in findings:
            if finding.attack_type == AttackType.SQL_INJECTION:
                scenarios.add("Scenario #1: SQL Injection")
            elif finding.attack_type == AttackType.HQL_INJECTION:
                scenarios.add("Scenario #2: HQL Injection")
            elif finding.attack_type == AttackType.COMMAND_INJECTION:
                scenarios.add("Scenario #3: Command Injection")

        return sorted(scenarios)

    def calculate_overall_risk(self, detected_scenarios):
        number_of_scenarios = len(detected_scenarios)

        if number_of_scenarios == 0:
            return RiskLevel.SAFE

        if number_of_scenarios == 3:
            return RiskLevel.CRITICAL

        return RiskLevel.HIGH

    def calculate_score(self, detected_scenarios):
        number_of_scenarios = len(detected_scenarios)

        if number_of_scenarios == 0:
            return 0
        if number_of_scenarios == 1:
            return 50
        if number_of_scenarios == 2:
            return 75
        if number_of_scenarios == 3:
            return 100

        return 100