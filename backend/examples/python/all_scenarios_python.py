# Testni primer, ki vsebuje vse 3 scenarije:
# Scenario #1: SQL Injection
# Scenario #2: HQL / ORM Injection
# Scenario #3: Command Injection

#python -m app.main --file examples/all_scenarios_python.py --lang python --db mysql

def get_user(request):
    user_id = request.GET["id"]
    query = "SELECT * FROM users WHERE id='" + user_id + "'"
    return query


def get_account(request, session):
    customer_id = request.GET["customer_id"]
    query = "FROM accounts WHERE custID='" + customer_id + "'"
    session.createQuery(query)


def lookup_domain(request, os):
    domain = request.GET["domain"]
    cmd = "nslookup " + domain
    os.system(cmd)