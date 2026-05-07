from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, source_code: str, language: str):
        pass