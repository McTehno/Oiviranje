# safe/safe_examples.py

def safe_find_user(request, cursor):
    user_id = request.GET["id"]

    query = "SELECT * FROM users WHERE id = %s"

    cursor.execute(query, (user_id,))


def safe_update_order(request, cursor):
    order_id = request.POST["order_id"]
    status = request.POST["status"]

    query = "UPDATE orders SET status = %s WHERE id = %s"

    cursor.execute(query, (status, order_id))


def safe_static_command():
    command = "echo backup started"

    return command


def safe_mongo_query(request, users_collection):
    username = request.GET["username"]

    query = {
        "username": username
    }

    result = users_collection.find(query)

    return result