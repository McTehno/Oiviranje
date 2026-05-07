def get_user(request, users):
    username = request.args["username"]
    filter_query = {"username": username}
    return users.find_one(filter_query)