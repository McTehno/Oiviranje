# test/python/test_python_multi_taint_sql.py

def search_orders(request, cursor):
    # User input sources
    user_id = request.GET["user_id"]
    status = request.GET["status"]
    sort_by = request.GET["sort_by"]

    # Tainted variables are copied into new variables
    selected_user = user_id
    selected_status = status
    order_column = sort_by

    # Static safe values
    table_name = "orders"
    base_query = "SELECT * FROM " + table_name

    # Vulnerable query construction with multiple tainted variables
    where_clause = (
        " WHERE user_id = " + selected_user +
        " AND status = '" + selected_status + "'"
    )

    order_clause = " ORDER BY " + order_column

    query = base_query + where_clause + order_clause

    cursor.execute(query)


def safe_search_orders(request, cursor):
    # User input is still read, but used safely as parameters
    user_id = request.GET["user_id"]
    status = request.GET["status"]

    query = "SELECT * FROM orders WHERE user_id = %s AND status = %s"

    cursor.execute(query, (user_id, status))