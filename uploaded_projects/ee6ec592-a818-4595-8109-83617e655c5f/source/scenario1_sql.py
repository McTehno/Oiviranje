"""
Scenario #1: SQL Injection

Opis:
    Ta datoteka simulira del spletne aplikacije za prikaz uporabniškega profila.
    Aplikacija prejme uporabnikov ID iz HTTP GET parametra in ga uporabi za
    sestavljanje SQL poizvedbe.

Kaj datoteka dela:
    - definira enostaven Logger
    - definira UserRepository za delo z uporabniki
    - vsebuje metodo get_user_by_id(), ki sestavi SQL query
    - vsebuje tudi nekaj varnih metod, da datoteka ni samo minimalen primer

Ranljivost:
    Uporabniški input iz request.GET["id"] se najprej shrani v spremenljivko user_id.
    Nato se user_id neposredno prilepi v SQL query z uporabo string concatenation.

Nevarna vrstica:
    query = "SELECT * FROM users WHERE id='" + user_id + "'"

Zakaj je nevarno:
    Napadalec lahko spremeni vrednost parametra id in s tem spremeni pomen SQL poizvedbe.

Pričakovan rezultat analizatorja:
    Scenario #1: SQL Injection
    Risk: HIGH
"""

class Logger:
    def info(self, message):
        print("[INFO]", message)

    def error(self, message):
        print("[ERROR]", message)


class UserFormatter:
    def format_user(self, user):
        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email")
        }

    def format_error(self, message):
        return {
            "status": "error",
            "message": message
        }


class UserRepository:
    def __init__(self, cursor, logger):
        self.cursor = cursor
        self.logger = logger

    def get_default_query(self):
        query = "SELECT * FROM users WHERE active=1"
        return query

    def list_active_users(self):
        query = self.get_default_query()
        self.logger.info("Listing active users")
        self.cursor.execute(query)

    def get_user_by_id(self, request):
        user_id = request.GET["id"]

        # VULNERABILITY: SQL Injection
        # User input is concatenated directly into the SQL query.
        query = "SELECT * FROM users WHERE id='" + user_id + "'"

        self.logger.info("Getting user by id")
        self.cursor.execute(query)

        return query

    def count_users(self):
        query = "SELECT COUNT(*) FROM users"
        self.cursor.execute(query)
        return query


class UserController:
    def __init__(self, repository, formatter):
        self.repository = repository
        self.formatter = formatter

    def show_user(self, request):
        try:
            query = self.repository.get_user_by_id(request)
            return {
                "status": "ok",
                "query": query
            }
        except Exception:
            return self.formatter.format_error("Could not load user")


def helper_clean_value(value):
    if value is None:
        return ""

    return str(value).strip()


def main():
    logger = Logger()
    formatter = UserFormatter()

    # cursor is assumed to be provided by the application
    cursor = None

    repository = UserRepository(cursor, logger)
    controller = UserController(repository, formatter)

    return controller