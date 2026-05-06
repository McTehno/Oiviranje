#python -m app.main --file test/python/all_scenarios_python.py --lang python --db mysql
def sql_example(request):
    user_id = request.GET["id"]
    query = "SELECT * FROM users WHERE id='" + user_id + "'"
    return query


def hql_example(request, session):
    user_id = request.GET["id"]
    query = "FROM accounts WHERE custID='" + user_id + "'"
    return session.createQuery(query)


def command_example(request):
    domain = request.GET["domain"]
    cmd = "nslookup " + domain
    return os.system(cmd)


def mongodb_example(request, users):
    username = request.args["username"]
    filter_query = {"username": username}
    return users.find_one(filter_query)