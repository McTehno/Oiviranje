from dataclasses import dataclass


@dataclass
class CodeLine:
    """
    Predstavlja eno vrstico kode.

    Parser vrne seznam CodeLine objektov.
    Detector potem pregleda te vrstice.
    
    primer kaj bi vrnil parser:
    CodeLine(
        number=4,
        content='query = "SELECT * FROM users WHERE id=" + user_id',
        language="python"
    )
    """

    number: int
    content: str
    language: str