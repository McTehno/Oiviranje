import ast
from models.finding import Finding

class PythonParser:
    """
    PARSER ZA PYTHON

    Input:
        python koda (string)

    Output:
        list Finding objektov
    """

    def parse(self, code):
        tree = ast.parse(code)
        findings = []

        for node in ast.walk(tree):

            # TODO: zaznaj string concatenation
            # TODO: zaznaj input() usage

            pass

        return findings