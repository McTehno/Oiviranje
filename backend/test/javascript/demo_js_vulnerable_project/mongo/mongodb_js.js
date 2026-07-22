export async function findUserProfile(req, users) {
    const username = req.query.username;
    return users.findOne({ username: username });
}