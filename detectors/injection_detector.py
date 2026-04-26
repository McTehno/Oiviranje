from analysis.taint_tracker import TaintTracker

from detectors.sql_detector import SQLDetector
from detectors.hql_detector import HQLDetector
from detectors.command_detector import CommandDetector


class InjectionDetector:
    def __init__(self):
        self.taint_tracker = TaintTracker()

        self.hql_detector = HQLDetector()
        self.sql_detector = SQLDetector()
        self.command_detector = CommandDetector()

    def detect(self, code_lines, database="mysql"):
        findings = []

        taint_by_line = self.taint_tracker.track(code_lines)

        for code_line in code_lines:
            tainted_variables = taint_by_line.get(code_line.number, set())

            hql_finding = self.hql_detector.detect_line(
                code_line,
                tainted_variables
            )

            if hql_finding:
                findings.append(hql_finding)
                continue

            sql_finding = self.sql_detector.detect_line(
                code_line,
                database,
                tainted_variables
            )

            if sql_finding:
                findings.append(sql_finding)

            command_finding = self.command_detector.detect_line(
                code_line,
                tainted_variables
            )

            if command_finding:
                findings.append(command_finding)

        return findings