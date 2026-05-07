"""
Scenario #3: Command Injection

Opis:
    Ta datoteka simulira del aplikacije za preverjanje DNS/domene.
    Aplikacija prejme ime domene iz HTTP GET parametra in sestavi sistemski ukaz nslookup.

Kaj datoteka dela:
    - definira Logger
    - definira DomainValidator
    - definira NetworkService za izvajanje omrežnih operacij
    - vsebuje metodo lookup_domain(), ki sestavi ukaz in ga izvede z os.system()

Ranljivost:
    Uporabniški input iz request.GET["domain"] se shrani v domain.
    Nato se domain neposredno prilepi v sistemski ukaz.
    Ukaz se izvede prek os.system(cmd).

Nevarne vrstice:
    cmd = "nslookup " + domain
    self.os.system(cmd)

Zakaj je nevarno:
    Napadalec lahko v parameter domain vstavi dodatne ukaze in tako povzroči izvajanje
    neželenih sistemskih ukazov na strežniku.

Pričakovan rezultat analizatorja:
    Scenario #3: Command Injection
    Risk: HIGH
"""
class Logger:
    def info(self, message):
        print("[INFO]", message)

    def error(self, message):
        print("[ERROR]", message)


class DomainValidator:
    def is_empty(self, value):
        return value is None or value == ""

    def normalize(self, value):
        if value is None:
            return ""

        return str(value).strip()


class NetworkService:
    def __init__(self, logger, os_module):
        self.logger = logger
        self.os = os_module

    def ping_static_host(self):
        cmd = "ping example.com"
        self.logger.info("Running static ping")
        self.os.system(cmd)

    def lookup_domain(self, request):
        domain = request.GET["domain"]

        # VULNERABILITY: Command Injection
        # User input is concatenated directly into the OS command.
        cmd = "nslookup " + domain

        self.logger.info("Running domain lookup")
        self.os.system(cmd)

    def show_help(self):
        return "Use domain parameter to perform lookup"


class NetworkController:
    def __init__(self, service, validator):
        self.service = service
        self.validator = validator

    def lookup(self, request):
        domain = request.GET["domain"]

        if self.validator.is_empty(domain):
            return {
                "status": "error",
                "message": "Missing domain"
            }

        self.service.lookup_domain(request)

        return {
            "status": "ok",
            "domain": domain
        }


def build_response(status, message):
    return {
        "status": status,
        "message": message
    }


def main():
    logger = Logger()
    validator = DomainValidator()

    # os module is assumed to be injected by application
    os_module = None

    service = NetworkService(logger, os_module)
    controller = NetworkController(service, validator)

    return controller