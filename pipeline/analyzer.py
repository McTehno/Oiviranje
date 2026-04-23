from parsers.python_parser import PythonParser
from parsers.js_parser import JSParser
from parsers.php_parser import PHPParser
from detectors.injection_detector import InjectionDetector
from reporting.report import Report

class Analyzer:
    """
    GLAVNI ORCHESTRATOR

    Input:
        code (string)
        lang (python/js/php)

    Output:
        report string
    """

    def run(self, code, lang):

        # TODO: izberi parser glede na lang

        parser = None

        # TODO: parse code
        findings = parser.parse(code)

        detector = InjectionDetector()
        findings = detector.detect(findings)

        report = Report()
        return report.generate(findings)