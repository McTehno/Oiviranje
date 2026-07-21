import re

from languages.base_taint_tracker import BaseTaintTracker


class JavaTaintTracker(BaseTaintTracker):
    """
    Preprost taint tracker za Javo.
    """

    def is_function_definition(self, line: str) -> bool:
        return re.search(
            r"^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?"
            r"[A-Za-z_$][\w$<>\[\], ?.]*\s+[A-Za-z_$][\w$]*\s*\([^;]*\)\s*\{?\s*$",
            line,
        ) is not None

    def extract_assigned_variable(self, line: str):
        declaration = re.match(
            r"^\s*(?:final\s+)?[A-Za-z_$][\w$<>\[\], ?.]*\s+([A-Za-z_$][\w$]*)\s*=",
            line,
        )

        if declaration:
            return declaration.group(1)

        reassignment = re.match(r"^\s*([A-Za-z_$][\w$]*)\s*=", line)

        if reassignment:
            return reassignment.group(1)

        return None
