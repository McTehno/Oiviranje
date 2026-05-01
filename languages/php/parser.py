from models.code_line import CodeLine
from languages.base_parser import BaseParser

class PHPParser(BaseParser):
    def parse(self, code: str):
        code_lines = []

        for line_number, line in enumerate(code.splitlines(), start=1):
            code_lines.append(
                CodeLine(
                    number=line_number,
                    content=line.strip(),
                    language="php"
                )
            )

        return code_lines