# Testni primer za SQL Injection detektor
# Direktni primer: user input je v isti vrstici kot SQL query

#python -m app.main --file examples/scenario1_sql.py --lang python --db mysql
def get_user(request):
    query = "SELECT * FROM users WHERE id='" + request.GET["id"] + "'"
    return query