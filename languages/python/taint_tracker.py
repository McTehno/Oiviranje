import re

from detectors.pattern_utils import contains_user_input


class TaintTracker:
    """
    Basic function-level taint tracker. Trenutno implementiran samo za python,
    vendar bomo naredili posebni tracker za vsak jezik (javasript in php).

    Naloga:
        - sledi nevarnim spremenljivkam znotraj posamezne funkcije
        - ko se začne nova funkcija, resetira tainted variables
        - vrne slovar: line_number -> tainted variables visible on that line
    """

    def track(self, code_lines):
        #pridobimo code_lines in jih obdelamo vrstico po vrstico
        taint_by_line = {} # slovar, kjer je ključ številka vrstice, vrednost pa množica tainted spremenljivk vidnih na tej vrstici
        current_tainted = set() # trenutne tainted spremenljivke, ki jih spremljamo znotraj trenutne funkcije

        for code_line in code_lines:
            line = code_line.content

            # če naletimo na definicijo funkcije, resetiramo trenutne tainted spremenljivke, saj začnemo slediti novi funkciji
            if self.is_function_definition(line):
                current_tainted = set()

            variable_name = self.extract_assigned_variable(line)

            if variable_name:
                if contains_user_input(line, code_line.language):
                    current_tainted.add(variable_name)

                elif self.uses_tainted_variable(line, current_tainted):
                    current_tainted.add(variable_name)

                elif variable_name in current_tainted:
                    current_tainted.remove(variable_name)

            taint_by_line[code_line.number] = set(current_tainted)

        return taint_by_line

    # funkcija preveri, ali vrstica predstavlja definicijo funkcije (npr. "def my_function(...):" v Pythonu)
    def is_function_definition(self, line: str):
        return re.match(r"^\s*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(", line) is not None

    def extract_assigned_variable(self, line: str):
        """
        Primer:
            user_id = request.GET["id"]

        Vrne:
            user_id
        """

        #ta regex išče vzorec, kjer imamo na začetku vrstice lahko nekaj presledkov, 
        # potem ime spremenljivke (ki mora začeti z črko ali podčrtajem, 
        # lahko pa vsebuje tudi številke), potem lahko spet nekaj presledkov, 
        # potem znak enakosti in na koncu karkoli (vsebina se ne gleda)
        #primer nekaj kaj ustreza: "   user_id   = request.GET["id"]"
        match = re.match(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=", line)

        if match:
            return match.group(1)

        return None

    #ta funkcija preveri, če se v vrstici uporablja katera od tainted spremenljivk.
    def uses_tainted_variable(self, line: str, tainted_variables: set):
        #za vsako tainted spremenljivko sestavimo regex vzorec,
        # ki išče to spremenljivko kot samostojno besedo (da ne bi ujel delov drugih besed)
        for variable in tainted_variables:

            #regex vzorec, ki išče spremenljivko kot samostojno besedo primer: za spremenljivko "user_id" bo vzorec r"\buser_id\b"
            pattern = r"\b" + re.escape(variable) + r"\b"

            #če se ta vzorec najde v vrstici, 
            # pomeni, da se ta tainted spremenljivka uporablja na tej vrstici,
            #  zato vrnemo True
            if re.search(pattern, line):
                return True

        return False