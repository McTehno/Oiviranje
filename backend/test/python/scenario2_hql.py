"""
Scenario #2: HQL / ORM Injection

Opis:
    Ta datoteka simulira del aplikacije za iskanje uporabniškega računa.
    Namesto klasične SQL poizvedbe uporablja ORM/HQL-style poizvedbo prek createQuery().

Kaj datoteka dela:
    - definira Logger
    - definira AccountRepository za delo z računi
    - vsebuje metodo get_account_from_request(), ki sestavi HQL/ORM query
    - query se nato posreduje v session.createQuery()

Ranljivost:
    Uporabniški input iz request.GET["id"] se shrani v customer_id.
    Nato se customer_id neposredno prilepi v HQL/ORM query.
    Ta query se nato izvede prek createQuery().

Nevarne vrstice:
    query = "FROM accounts WHERE custID='" + customer_id + "'"
    return self.session.createQuery(query)

Zakaj je nevarno:
    Če je uporabniški input neposredno vključen v ORM/HQL query,
    lahko napadalec spremeni logiko poizvedbe in pridobi nepooblaščen dostop do podatkov.

Pričakovan rezultat analizatorja:
    Scenario #2: HQL Injection
    Risk: HIGH
"""

class Logger:
    def info(self, message):
        print("[INFO]", message)


class AccountFormatter:
    def format_account(self, account):
        return {
            "id": account.get("id"),
            "owner": account.get("owner"),
            "balance": account.get("balance")
        }

    def empty_response(self):
        return {
            "status": "empty",
            "data": None
        }


class AccountRepository:
    def __init__(self, session, logger):
        self.session = session
        self.logger = logger

    def get_all_accounts_query(self):
        return "FROM accounts"

    def list_accounts(self):
        query = self.get_all_accounts_query()
        self.logger.info("Listing accounts")
        return self.session.createQuery(query)

    def get_account_from_request(self, request):
        customer_id = request.GET["id"]

        # VULNERABILITY: HQL / ORM Injection
        # User input is concatenated directly into the ORM query.
        query = "FROM accounts WHERE custID='" + customer_id + "'"

        self.logger.info("Loading account from request")
        return self.session.createQuery(query)

    def get_demo_account(self):
        query = "FROM accounts WHERE custID='demo'"
        return self.session.createQuery(query)


class AccountController:
    def __init__(self, repository, formatter):
        self.repository = repository
        self.formatter = formatter

    def show_account(self, request):
        account = self.repository.get_account_from_request(request)

        if account is None:
            return self.formatter.empty_response()

        return {
            "status": "ok",
            "data": account
        }


def normalize_customer_id(value):
    if value is None:
        return "0"

    return str(value).strip()


def main():
    logger = Logger()
    formatter = AccountFormatter()

    # session is assumed to be provided by ORM framework
    session = None

    repository = AccountRepository(session, logger)
    controller = AccountController(repository, formatter)

    return controller