import re
from languages.base_taint_tracker import BaseTaintTracker

class PHPTaintTracker(BaseTaintTracker):
    """
    Taint tracker specifičen za PHP.
    Preverja ustvarjanje spremenljivk in uporabo taint podatkov (začenši z $).
    """

    def is_function_definition(self, line: str) -> bool:
        """
        Preveri, ali vrstica predstavlja definicijo funkcije ali metode v PHP-ju.
        (npr. 'function myFunction(...)' ali 'public function myMethod(...)')
        """
        return re.match(r"^\s*(?:public\s+|protected\s+|private\s+)?function\s+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*\s*\(", line) is not None

    def extract_assigned_variable(self, line: str):
        """
        Izlušči ime spremenljivke v PHP prireditveni vrstici.
        Primer:
            $user_id = $_GET['id'];
        Vrne:
            $user_id
            
        V PHP imena spremenljivk vedno začnejo z znakom dolarija ($).
        """
        match = re.match(r"^\s*(\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)\s*=", line)

        if match:
            return match.group(1)

        return None
    
    def uses_tainted_variable(self, line: str, tainted_variables: set) -> bool:
        """
        Preveri, če se v vrstici uporablja katera od umazanih (tainted) spremenljivk.
        Ker imajo spremenljivke v PHP-ju znak '$', obravnava word boundary (\b)
        ni optimalna za začetek besede.
        """
        for variable in tainted_variables:
            # Escape spremenljivko (npr. '$user_id')
            escaped_var = re.escape(variable)
            # V PHP preverimo z golim string matchingom ali regex z ne-besednimi mmejami
            pattern = escaped_var + r"(?!\w)"
            
            if re.search(pattern, line):
                return True

        return False