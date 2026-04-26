from abc import ABC, abstractmethod

#abc pomeni da je to abstract base class, kar pomeni da 
# ne moremo ustvariti instance tega razreda, 
# ampak ga moramo podedovati in implementirati njegove metode. 
# To je uporabno, ker želimo definirati skupen interface za vse parserje,
# ki bodo dedovali od BaseParserja.

class BaseParser(ABC):
    """
    Skupni interface za vse parserje.

    Input:
        code: string

    Output:
        list[CodeLine]
    """

    @abstractmethod
    def parse(self, code: str):
        raise NotImplementedError("Parser must implement parse()")