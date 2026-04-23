from dataclasses import dataclass

@dataclass
class Result:
    """
    KONČNI REZULTAT ANALIZE

    Input:
        seznam findings + risk score

    Output:
        report layer

    """

    findings: list
    score: int
    risk: str