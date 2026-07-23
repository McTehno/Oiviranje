export async function findUser(req, db) {
    const userId = req.query.id;
    return db.query(`SELECT * FROM users WHERE id = '${userId}'`);
}

// db/users_sql.ts

// 1. SQL Injection z uporabo template literala
export async function findUserById(req,db) {
    const userId= req.query.id;

    const query = `SELECT * FROM users WHERE id = '${userId}'`;

    return db.query(query);
}


// 2. SQL Injection z operatorjem +
export async function findUserByEmail(req,db) {
    const email= req.query.email;

    const query =
        'SELECT * FROM users WHERE email = "' + email + '"';

    return db.query(query);
}


// 3. SQL Injection s template literal interpolacijo
export async function findUserByUsername(req,db) {
    const username= req.query.username;

    const query =
        `SELECT * FROM users WHERE username = '${username}'`;

    return db.query(query);
}


// 4. Neposredno podajanje uporabniškega vnosa v query
export async function findUserDirectly(req,db) {
    return db.query(
        `SELECT * FROM users WHERE id = '${req.query.id}'`
    );
}


// 5. SQL Injection v pogoju LIKE
export async function searchUsers(req,db) {
    const search= req.query.search;

    const query =
        `SELECT * FROM users WHERE username LIKE '%${search}%'`;

    return db.query(query);
}


// 6. SQL Injection v ORDER BY
export async function sortUsers(req,db) {
    const sortField= req.query.sort;

    const query =
        `SELECT * FROM users ORDER BY ${sortField}`;

    return db.query(query);
}