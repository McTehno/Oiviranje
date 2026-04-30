from languages.python.taint_tracker import TaintTracker as PythonTaintTracker
from languages.php.taint_tracker import PHPTaintTracker
from languages.javascript.taint_tracker import JavaScriptTaintTracker

from detectors.sql_detector import SQLDetector
from detectors.hql_detector import HQLDetector
from detectors.command_detector import CommandDetector


class InjectionDetector:
    def __init__(self):
        # Zadetektorje inicializiramo tukaj (TaintTracker sedaj inicializiramo kasneje, 
        # ko dejansko vemo kateri jezik uporabljamo).
        self.hql_detector = HQLDetector()
        self.sql_detector = SQLDetector()
        self.command_detector = CommandDetector()

    def get_taint_tracker(self, language: str):
        """
        Tovarna (factory) za pridobivanje pravilnega TaintTracker-ja 
        glede na jezik kode.
        """
        if language == "python":
            return PythonTaintTracker()
        elif language == "php":
            return PHPTaintTracker()
        elif language == "javascript":
            return JavaScriptTaintTracker()
        else:
            raise ValueError(f"Taint tracker ne podpora jezika: {language}")

    def detect(self, code_lines, database="mysql"):
        findings = []

        if not code_lines:
            return findings

        # Dobimo jezik iz prve vrstice, ali pa privzeto python
        language = code_lines[0].language if code_lines else "python"
        
        # Ustvarimo pravega taint trackerja za ta jezik
        taint_tracker = self.get_taint_tracker(language)
        
        # Pridobimo umazane (tainted) spremenljivke za vsako vrstico
        taint_by_line = taint_tracker.track(code_lines)

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