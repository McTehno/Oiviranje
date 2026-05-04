import re
from abc import ABC, abstractmethod
from detectors.pattern_utils import contains_user_input, contains_mongodb_operator

class BaseTaintTracker(ABC):
    """
    Osnovni (base) razred za sledenje umazanim (tainted) spremenljivkam.
    Vsak specifičen jezik (Python, PHP, JS) ga mora podedovati in 
    implementirati specifične metode za ta jezik.
    """

    def track(self, code_lines):
        """
        Glavna metoda, ki prebere vse vrstice in vrne dva slovarja:
        1. taint_by_line: line_number -> mnozica umazanih (tainted) spremenljivk
        2. operator_by_line: line_number -> mnozica spremenljivk, ki vsebujejo MongoDB operatorje
        """
        taint_by_line = {}
        operator_by_line = {} # Slovar za sledenje spremenljivkam z MongoDB operatorji
        
        current_tainted = set()
        current_operators = set() # Trenutne spremenljivke z MongoDB operatorji

        for code_line in code_lines:
            line = code_line.content

            # Če naletimo na definicijo funkcije, resetiramo trenutne spremenljivke,
            # saj začnemo slediti novi funkciji (taint tracking na nivoju funkcije)
            if self.is_function_definition(line):
                current_tainted = set()
                current_operators = set()

            variable_name = self.extract_assigned_variable(line)

            if variable_name:
                # --- 1. Sledenje Taint spremenljivkam ---
                # Preverimo, če se spremenljivki dodeljuje direkten uporabniški vnos
                if contains_user_input(line, code_line.language):
                    current_tainted.add(variable_name)

                # Preverimo, če se spremenljivki dodeljuje vrednost druge umazane spremenljivke
                elif self.uses_tainted_variable(line, current_tainted):
                    current_tainted.add(variable_name)

                # Če se spremenljivki dodeli varna vrednost, jo odstranimo iz seznama umazanih
                elif variable_name in current_tainted:
                    current_tainted.remove(variable_name)
                    
                # --- 2. Sledenje MongoDB operatorjem ---
                # Preverimo, če se spremenljivki dodeljuje direktna uporaba MongoDB operatorja
                if contains_mongodb_operator(line):
                    current_operators.add(variable_name)
                    
                # Preverimo, če se spremenljivki dodeljuje vrednost druge spremenljivke z operatorjem
                elif self.uses_tainted_variable(line, current_operators):
                    current_operators.add(variable_name)
                    
                # Če se spremenljivki dodeli navadna vrednost brez operatorja, jo odstranimo
                elif variable_name in current_operators:
                    current_operators.remove(variable_name)

            taint_by_line[code_line.number] = set(current_tainted)
            operator_by_line[code_line.number] = set(current_operators) # Shranimo stanje operatorjev za vrstico

        return taint_by_line, operator_by_line

    @abstractmethod
    def is_function_definition(self, line: str) -> bool:
        """
        Preveri, ali vrstica predstavlja definicijo funkcije.
        """
        pass

    @abstractmethod
    def extract_assigned_variable(self, line: str):
        """
        Izlušči ime spremenljivke iz prireditvene vrstice.
        Primer (Python): 'user_id = request.GET["id"]' vrne 'user_id'
        Primer (PHP): '$userId = $_GET["id"]' vrne '$userId'
        """
        pass

    def uses_tainted_variable(self, line: str, tainted_variables: set) -> bool:
        """
        Preveri, če se v vrstici uporablja katera od tained spremenljivk.
        To je privzeta (default) implementacija, ki uporablja regex \b (word boundary).
        Jeziki (kot npr. PHP za $spremenljivke) lahko to metodo povozi (override).
        """
        for variable in tainted_variables:
            # Regex vzorec, ki išče spremenljivko kot samostojno besedo (da ne bi ujel delov drugih besed)
            # Primer: za spremenljivko "user_id" bo vzorec r"\buser_id\b"
            pattern = r"\b" + re.escape(variable) + r"\b"

            if re.search(pattern, line):
                return True

        return False