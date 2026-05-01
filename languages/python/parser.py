from languages.base_parser import BaseParser
from models.code_line import CodeLine


class PythonParser(BaseParser):
    """
    Parser za Python kodo.

    Naloga:
        - prejme Python kodo kot string
        - razdeli jo po vrsticah
        - vrne seznam CodeLine objektov
    """

    def parse(self, code: str):
        code_lines = []

        lines = code.splitlines()

        for line_number, line in enumerate(lines, start=1):
            code_lines.append(
                CodeLine(
                    number=line_number,
                    content=line.strip(),
                    language="python"
                )
            )

        return code_lines