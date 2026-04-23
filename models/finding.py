from dataclasses import dataclass

@dataclass
class Finding:
    """
    REPREZENTIRA EN PROBLEM V KODI

    Input:
        parser (AST / regex analiza)

    Output:
        strukturiran objekt za detector

    Attributes:
        line -> vrstica v kodi
        type -> tip problema (concat, exec)
        code -> dejanska koda
        variables -> user input spremenljivke
    """

    line: int
    type: str
    code: str
    variables: list
    language: str

    risk: str = "LOW"
    attack_type: str = "NONE"