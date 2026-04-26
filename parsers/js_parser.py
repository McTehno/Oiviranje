from parsers.base import BaseParser
from models.code_line import CodeLine


class JSParser(BaseParser):
    """
    Parser za JavaScript kodo.
    """

    def parse(self, code: str):
        code_lines = []

        lines = code.splitlines()

        for line_number, line in enumerate(lines, start=1):
            code_lines.append(
                CodeLine(
                    number=line_number,
                    content=line.strip(),
                    language="javascript"
                )
            )

        return code_lines