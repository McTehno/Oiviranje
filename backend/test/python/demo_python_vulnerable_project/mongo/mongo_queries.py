# mongo/mongo_queries.py

def find_mongo_user(request, users_collection):
    user_filter = request.GET["filter"]

    result = users_collection.find(user_filter)

    return result


def find_mongo_user_by_body(request, users_collection):
    query_filter = request.POST["filter"]

    result = users_collection.find_one(query_filter)

    return result


def find_with_operator(request, users_collection):
    username = request.GET["username"]

    query = {
        "username": {
            "$ne": username
        }
    }

    result = users_collection.find(query)

    return result


def delete_mongo_user(request, users_collection):
    filter_data = request.GET["filter"]

    result = users_collection.delete_one(filter_data)

    return result