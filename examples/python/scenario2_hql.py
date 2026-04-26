# Testni primer za HQL / ORM Injection detektor
# Direktni primer: user input je v isti vrstici kot createQuery

#Zagon: python -m app.main --file examples/scenario2_hql.py --lang python --db mysql

def get_account(request, session):
    session.createQuery("FROM accounts WHERE custID='" + request.GET["id"] + "'")