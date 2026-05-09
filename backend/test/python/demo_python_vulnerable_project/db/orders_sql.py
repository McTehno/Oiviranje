# db/orders_sql.py

def search_orders(request, cursor):
    user_id = request.GET["user_id"]
    status = request.GET["status"]
    sort_by = request.GET["sort_by"]

    selected_user = user_id
    selected_status = status
    order_column = sort_by

    table_name = "orders"
    base_query = "SELECT * FROM " + table_name

    where_clause = (
        " WHERE user_id = " + selected_user +
        " AND status = '" + selected_status + "'"
    )

    order_clause = " ORDER BY " + order_column

    query = base_query + where_clause + order_clause

    cursor.execute(query)


def update_order_status(request, cursor):
    order_id = request.POST["order_id"]
    new_status = request.POST["status"]

    query = "UPDATE orders SET status = '" + new_status + "' WHERE id = " + order_id

    cursor.execute(query)


def delete_order(request, cursor):
    order_id = request.GET["order_id"]

    query = "DELETE FROM orders WHERE id = " + order_id

    cursor.execute(query)