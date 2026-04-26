import re

from detectors.pattern_utils import contains_user_input

'''
class PythonTaintTracker:
    """
    Basic function-level taint tracker.

    Naloga:
        - sledi nevarnim spremenljivkam znotraj posamezne funkcije
        - ko se začne nova funkcija, resetira tainted variables
        - vrne slovar: line_number -> tainted variables visible on that line
    """

    def track(self, code_lines):
        taint_by_line = {}
        current_tainted = set()

        for code_line in code_lines:
            line = code_line.content

            if self.is_function_definition(line):
                current_tainted = set()

            variable_name = self.extract_assigned_variable(line)

            if variable_name:
                if contains_user_input(line, python_rules):
                    current_tainted.add(variable_name)

                elif self.uses_tainted_variable(line, current_tainted):
                    current_tainted.add(variable_name)

                elif variable_name in current_tainted:
                    current_tainted.remove(variable_name)

            taint_by_line[code_line.number] = set(current_tainted)

        return taint_by_line

    def is_function_definition(self, line: str):
        return re.match(
            r"^\s*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(",
            line
        ) is not None

    def extract_assigned_variable(self, line: str):
        match = re.match(
            r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=",
            line
        )

        if match:
            return match.group(1)

        return None

    def uses_tainted_variable(self, line: str, tainted_variables: set):
        for variable in tainted_variables:
            pattern = r"\b" + re.escape(variable) + r"\b"

            if re.search(pattern, line):
                return True

        return False
'''