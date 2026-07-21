from languages.base_parser import BaseParser
from models.code_line import CodeLine

#base parser for Java code

class JavaParser(BaseParser):
    def parse(self, code: str):
        code_lines = []

        for line_number, line in enumerate(code.splitlines(), start=1):
            code_lines.append(
                CodeLine(
                    number=line_number,
                    content=line.strip(),
                    language="java"
                )
            )

        return code_lines