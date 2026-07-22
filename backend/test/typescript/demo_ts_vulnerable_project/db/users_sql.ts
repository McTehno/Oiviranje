export async function findUser(req: any, db: any) {
    const userId: string = req.query.id;
    return db.query(`SELECT * FROM users WHERE id = '${userId}'`);
}