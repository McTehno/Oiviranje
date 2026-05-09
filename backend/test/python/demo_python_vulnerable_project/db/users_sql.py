# db/users_sql.py

def find_user_by_id(request, cursor):
    user_id = request.GET["id"]

    query = "SELECT * FROM users WHERE id = " + user_id

    cursor.execute(query)


def find_user_by_email(request, cursor):
    email = request.GET["email"]

    query = 'SELECT * FROM users WHERE email = "' + email + '"'

    cursor.execute(query)


def find_user_with_f_string(request, cursor):
    username = request.GET["username"]

    query = f"SELECT * FROM users WHERE username = '{username}'"

    cursor.execute(query)