import { findUser } from './db/users_sql.js';
import { findUserProfile } from './mongo/mongodb_js.js';
import { safeUserQuery } from './safe/safe_examples.js';
import { findUserProfile as findUserProfileMongo } from './mongo/users_mongo.js';
import { ping } from './system/command_tools.js';
import { findUserByName } from './db/user_orm.js';


export async function run(req, db) {
    await findUser(req, db);
    await findUserProfile(req, db);
    await safeUserQuery(req, db);
    await findUserProfileMongo(req, db);
    await ping(req);
    await findUserByName(req, db);
}