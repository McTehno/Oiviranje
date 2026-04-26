from abc import ABC, abstractmethod


class BaseDetector(ABC):
    """
    Skupni interface za vse detectorje.
        Input: list[CodeLine]
        Output: list[Finding]
    """

    @abstractmethod
    def detect(self, code_lines, database="mysql"):
        raise NotImplementedError("Detector must implement detect()")