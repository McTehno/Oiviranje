# app.py

from db.users_sql import find_user_by_id
from db.orders_sql import search_orders
from system.command_tools import ping_host
from mongo.mongo_queries import find_mongo_user


def run_demo(request, cursor, mongo_users_collection):
    find_user_by_id(request, cursor)
    search_orders(request, cursor)
    ping_host(request)
    find_mongo_user(request, mongo_users_collection)