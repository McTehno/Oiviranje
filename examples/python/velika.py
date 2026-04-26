# Large test file for SQL Injection Analyzer
# This file simulates a bigger Python application.
# It intentionally contains one SQL Injection vulnerability.

class Logger:
    def info(self, message):
        print("[INFO]", message)

    def error(self, message):
        print("[ERROR]", message)


class FakeRequest:
    def __init__(self):
        self.GET = {}
        self.POST = {}


class FakeCursor:
    def execute(self, query):
        print("Executing:", query)


class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "email": self.email
        }


class UserService:
    def __init__(self, cursor, logger):
        self.cursor = cursor
        self.logger = logger

    def validate_username(self, username):
        if username is None:
            return False

        if len(username) < 3:
            return False

        if len(username) > 50:
            return False

        return True

    def validate_email(self, email):
        if email is None:
            return False

        if "@" not in email:
            return False

        if "." not in email:
            return False

        return True

    def create_user_object(self, row):
        user_id = row.get("id")
        username = row.get("username")
        email = row.get("email")

        return User(user_id, username, email)

    def format_user_response(self, user):
        data = user.to_dict()

        response = {
            "status": "success",
            "data": data
        }

        return response

    def get_default_user(self):
        user = User(
            user_id=0,
            username="guest",
            email="guest@example.com"
        )

        return user

    def log_user_action(self, action, username):
        message = "User action: " + action + " by " + username
        self.logger.info(message)

    def normalize_id(self, value):
        if value is None:
            return "0"

        return str(value).strip()

    def get_user_by_static_id(self):
        query = "SELECT * FROM users WHERE id='1'"
        self.logger.info("Running static user query")
        self.cursor.execute(query)

    def get_user_by_safe_default(self):
        default_id = "1"
        query = "SELECT * FROM users WHERE id='" + default_id + "'"
        self.logger.info("Running query with internal default id")
        self.cursor.execute(query)

    def list_users(self):
        query = "SELECT * FROM users"
        self.logger.info("Listing all users")
        self.cursor.execute(query)

    def count_users(self):
        query = "SELECT COUNT(*) FROM users"
        self.logger.info("Counting users")
        self.cursor.execute(query)

    def search_by_username_static(self):
        username = "admin"
        query = "SELECT * FROM users WHERE username='" + username + "'"
        self.logger.info("Searching static username")
        self.cursor.execute(query)

    def get_user_from_request(self, request):
        # Vulnerable block starts here
        user_id = request.GET["id"]
        query = "SELECT * FROM users WHERE id='" + user_id + "'"
        self.logger.info("Running user lookup from request")
        self.cursor.execute(query)
        # Vulnerable block ends here

    def update_last_login_static(self):
        user_id = "1"
        query = "UPDATE users SET last_login=NOW() WHERE id='" + user_id + "'"
        self.logger.info("Updating last login")
        self.cursor.execute(query)

    def delete_test_user_static(self):
        user_id = "999"
        query = "DELETE FROM users WHERE id='" + user_id + "'"
        self.logger.info("Deleting test user")
        self.cursor.execute(query)

    def build_profile(self, username, email):
        profile = {
            "username": username,
            "email": email,
            "active": True
        }

        return profile

    def calculate_user_score(self, login_count, comment_count):
        score = 0
        score += login_count * 2
        score += comment_count * 5

        if score > 100:
            score = 100

        return score

    def is_admin(self, username):
        admins = ["admin", "root", "manager"]

        if username in admins:
            return True

        return False

    def get_permissions(self, username):
        if self.is_admin(username):
            return ["read", "write", "delete"]

        return ["read"]

    def render_user_card(self, user):
        card = ""
        card += "User ID: " + str(user.user_id) + "\n"
        card += "Username: " + user.username + "\n"
        card += "Email: " + user.email + "\n"

        return card

    def export_user(self, user):
        data = user.to_dict()
        lines = []

        for key, value in data.items():
            lines.append(str(key) + ": " + str(value))

        return "\n".join(lines)

    def send_welcome_message(self, user):
        message = "Welcome, " + user.username
        self.logger.info(message)

    def deactivate_user_static(self):
        user_id = "10"
        query = "UPDATE users SET active=0 WHERE id='" + user_id + "'"
        self.logger.info("Deactivating static user")
        self.cursor.execute(query)

    def activate_user_static(self):
        user_id = "10"
        query = "UPDATE users SET active=1 WHERE id='" + user_id + "'"
        self.logger.info("Activating static user")
        self.cursor.execute(query)


class AuditService:
    def __init__(self, logger):
        self.logger = logger

    def audit_login(self, username):
        message = "Login event for user: " + username
        self.logger.info(message)

    def audit_logout(self, username):
        message = "Logout event for user: " + username
        self.logger.info(message)

    def audit_error(self, error_message):
        self.logger.error(error_message)

    def build_audit_record(self, event_type, username):
        record = {
            "event": event_type,
            "username": username,
            "created_at": "now"
        }

        return record

    def save_audit_record(self, record):
        self.logger.info("Saving audit record")
        return True


class Application:
    def __init__(self):
        self.logger = Logger()
        self.cursor = FakeCursor()
        self.user_service = UserService(self.cursor, self.logger)
        self.audit_service = AuditService(self.logger)

    def setup(self):
        self.logger.info("Application setup started")
        self.logger.info("Database connection initialized")
        self.logger.info("Services loaded")

    def handle_home(self):
        response = {
            "page": "home",
            "status": "ok"
        }

        return response

    def handle_profile(self, request):
        self.logger.info("Handling profile request")
        self.user_service.get_user_from_request(request)

    def handle_users(self):
        self.logger.info("Handling users list")
        self.user_service.list_users()

    def handle_login(self, username):
        self.audit_service.audit_login(username)

        response = {
            "status": "logged_in",
            "username": username
        }

        return response

    def handle_logout(self, username):
        self.audit_service.audit_logout(username)

        response = {
            "status": "logged_out",
            "username": username
        }

        return response

    def handle_error(self, message):
        self.audit_service.audit_error(message)

        response = {
            "status": "error",
            "message": message
        }

        return response

    def run_demo(self):
        self.setup()

        request = FakeRequest()
        request.GET["id"] = "5"

        self.handle_home()
        self.handle_users()
        self.handle_profile(request)

        self.handle_login("admin")
        self.handle_logout("admin")


def helper_format_date(value):
    return str(value)


def helper_clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def helper_is_empty(value):
    if value is None:
        return True

    if value == "":
        return True

    return False


def helper_build_response(status, data):
    return {
        "status": status,
        "data": data
    }


def helper_print_banner():
    print("==============================")
    print(" Large SQL Test Application")
    print("==============================")


def main():
    helper_print_banner()

    app = Application()
    app.run_demo()


if __name__ == "__main__":
    main()