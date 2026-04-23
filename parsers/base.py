class BaseParser:
    """
    ABSTRACT PARSER

    Namen:
        Skupni interface za vse parserje

    Input:
        code (string)

    Output:
        list[Finding]
    """

    def parse(self, code: str):
        # TODO: implementacija v child class
        pass