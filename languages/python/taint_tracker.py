import re

from languages.base_taint_tracker import BaseTaintTracker
from detectors.pattern_utils import contains_user_input


class TaintTracker(BaseTaintTracker):
    """
    Taint tracker specifičen za Python.
    Dedi od BaseTaintTracker in implementira Python logiko za funkcije in spremenljivke.
    """

    def is_function_definition(self, line: str) -> bool:
        """
        Ta funkcija preveri, ali vrstica predstavlja definicijo funkcije 
        (npr. 'def my_function(...):' v Pythonu)
        """
        return re.match(r"^\s*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(", line) is not None

    def extract_assigned_variable(self, line: str):
        """
        Primer:
            user_id = request.GET["id"]
        Vrne:
            user_id
        
        Ta regex išče vzorec, kjer imamo na začetku vrstice lahko nekaj presledkov, 
        potem ime spremenljivke (ki mora začeti s črko ali podčrtajem, 
        lahko pa vsebuje tudi številke), potem lahko spet nekaj presledkov, 
        potem znak enakosti in na koncu karkoli.
        """
        match = re.match(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=", line)

        if match:
            return match.group(1)

        return None