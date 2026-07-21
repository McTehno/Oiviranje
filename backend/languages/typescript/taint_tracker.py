import re

from languages.base_taint_tracker import BaseTaintTracker


class TypeScriptTaintTracker(BaseTaintTracker):
    """
    Taint tracker za TypeScript.

    Prepoznava:
    - običajne funkcije,
    - arrow funkcije,
    - metode razredov,
    - prirejanje spremenljivk,
    - uporabo tainted spremenljivk.
    """

    def is_function_definition(self, line: str) -> bool:
        """
        Primeri:
            function test(value: string) {
            const test = (value: string) => {
            async findUser(id: number): Promise<User> {
            constructor(repository: UserRepository) {
        """
        return re.match(
            r"""
            ^\s*
            (?:
                # function test(...)
                (?:export\s+)?(?:default\s+)?(?:async\s+)?
                function\s+[A-Za-z_$][A-Za-z0-9_$]*
                \s*\([^)]*\)
                (?:\s*:\s*[^{=]+)?
                \s*\{

                |

                # const test = (...) =>
                (?:export\s+)?
                (?:const|let|var)\s+
                [A-Za-z_$][A-Za-z0-9_$]*
                (?:\s*:\s*[^=]+)?
                \s*=\s*
                (?:async\s+)?
                (?:\([^)]*\)|[A-Za-z_$][A-Za-z0-9_$]*)
                \s*=>

                |

                # Metoda razreda ali konstruktor
                (?:(?:public|private|protected|static|readonly|abstract)\s+)*
                (?:async\s+)?
                (?!if\b|for\b|while\b|switch\b|catch\b)
                (?:constructor|[A-Za-z_$][A-Za-z0-9_$]*)
                \s*\([^)]*\)
                (?:\s*:\s*[^{=]+)?
                \s*\{
            )
            """,
            line,
            re.VERBOSE
        ) is not None

    def extract_assigned_variable(self, line: str):
        """
        Primeri:
            const userId: string = req.query.id;
            let command = req.body.command;
            userId = value;
            this.username = username;

        Vrne:
            userId
            command
            username
        """
        match = re.match(
            r"""
            ^\s*
            (?:(?:const|let|var)\s+)?
            (?:this\s*\.\s*)?
            ([A-Za-z_$][A-Za-z0-9_$]*)
            (?:\s*[?!]?\s*:\s*[^=]+)?
            \s*=
            (?!=|>)
            """,
            line,
            re.VERBOSE
        )

        if match:
            return match.group(1)

        return None

    def uses_tainted_variable(
        self,
        line: str,
        tainted_variables: set
    ) -> bool:
        """
        Preveri, ali vrstica uporablja tainted spremenljivko.
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