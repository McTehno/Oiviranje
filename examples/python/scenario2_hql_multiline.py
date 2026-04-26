# Testni primer za HQL / ORM Injection detektor
# Multiline primer: user input se najprej shrani v spremenljivko
#python -m app.main --file examples/scenario2_hql_multiline.py --lang python --db mysql


def get_account(request, session):
    user_id = request.GET["id"]
    query = "FROM accounts WHERE custID='" + user_id + "'"
    session.createQuery(query)