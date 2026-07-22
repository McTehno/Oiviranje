export async function findUserProfile(req: any, users: any) {
    const username: string = req.query.username;
    return users.findOne({ username });
}