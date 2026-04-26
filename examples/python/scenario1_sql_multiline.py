# Testni primer za SQL Injection detektor
# Multiline primer: user input se najprej shrani v spremenljivko

#python -m app.main --file examples/scenario1_sql_multiline.py --lang python --db mysql
def get_user(request):
    user_id = request.GET["id"]
    query = "SELECT * FROM users WHERE id='" + user_id + "'"
    return query