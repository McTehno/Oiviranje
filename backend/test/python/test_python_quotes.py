# test/python/test_python_quotes.py

def vulnerable_sql_double_quotes(request, cursor):
    user_id = request.GET["id"]
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)


def vulnerable_sql_single_quotes(request, cursor):
    user_id = request.GET['id']
    query = 'SELECT * FROM users WHERE id = ' + user_id
    cursor.execute(query)


def vulnerable_sql_f_string_double_quotes(request, cursor):
    user_id = request.GET["id"]
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)


def vulnerable_sql_f_string_single_quotes(request, cursor):
    user_id = request.GET['id']
    query = f'SELECT * FROM users WHERE id = {user_id}'
    cursor.execute(query)


def vulnerable_sql_upper_f_string_double_quotes(request, cursor):
    user_id = request.GET["id"]
    query = F"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)


def vulnerable_sql_upper_f_string_single_quotes(request, cursor):
    user_id = request.GET['id']
    query = F'SELECT * FROM users WHERE id = {user_id}'
    cursor.execute(query)


def safe_sql_parameterized_query(request, cursor):
    user_id = request.GET["id"]
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))