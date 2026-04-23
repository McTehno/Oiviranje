from models.finding import Finding

class PHPParser:
    """
    PARSER ZA PHP

    Input:
        PHP koda

    Output:
        list Finding
    """

    def parse(self, code):
        findings = []

        # TODO:
        # - zaznaj "."
        # - zaznaj $_GET / $_POST
        # - zaznaj exec()

        return findings