import re

from languages.base_taint_tracker import BaseTaintTracker


class JavaScriptTaintTracker(BaseTaintTracker):
    """
    Preprost taint tracker za JavaScript.
    """

    def is_function_definition(self, line: str) -> bool:
        """
        Primeri:
            function saveUser(user) {
            async function loadData() {
            const saveUser = (user) => {
            saveUser(user) {
        """
        pattern = (
            r"^\s*(?:"
            r"(?:async\s+)?function\s+[A-Za-z_$][A-Za-z0-9_$]*\s*\([^)]*\)"
            r"|"
            r"(?:const|let|var)\s+[A-Za-z_$][A-Za-z0-9_$]*"
            r"\s*=\s*(?:async\s+)?(?:\([^)]*\)|[A-Za-z_$][A-Za-z0-9_$]*)\s*=>"
            r"|"
            r"(?:async\s+)?[A-Za-z_$][A-Za-z0-9_$]*\s*\([^)]*\)\s*\{"
            r")"
        )

        return re.match(pattern, line) is not None

    def extract_assigned_variable(self, line: str):
        """
        Primeri:
            const userId = req.query.id;
            let command = req.body.command;
            userId = value;
            this.username = username;

        Vrne:
            userId
            command
            username
        """
        pattern = (
            r"^\s*"
            r"(?:(?:const|let|var)\s+)?"
            r"(?:this\s*\.\s*)?"
            r"([A-Za-z_$][A-Za-z0-9_$]*)"
            r"\s*=(?!=|>)"
        )

        match = re.match(pattern, line)

        if match:
            return match.group(1)

        return None

    def uses_tainted_variable(
        self,
        line: str,
        tainted_variables: set
    ) -> bool:
        """
        Preveri uporabo tainted spremenljivke.
        """
        for variable in tainted_variables:
            pattern = (
                r"(?<![A-Za-z0-9_$])"
                + re.escape(variable)
                + r"(?![A-Za-z0-9_$])"
            )

            if re.search(pattern, line):
                return True

        return False