def mongodb_operator_direct_example(request, users):
    username = request.args["username"]
    return users.find_one({"username": {"$ne": username}})