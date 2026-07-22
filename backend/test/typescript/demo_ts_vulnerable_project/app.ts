import {findUserByName} from './db/user_orm';
import {findUser} from './db/users_sql';
import {findUserProfile} from './mongo/mongodb_ts';
import {findMongoUser} from './mongo/users_mongo';
import {findSafeUser} from './safe/safe_examples';
import {ping} from './system/command_tools';

export async function run(db: any, prisma: any, users: any) {
    findUserByName({ body: { name: 'Alice' } }, prisma);
    findUser({ query: { id: '123' } }, db);
    findUserProfile({ query: { username: 'Bob' } }, users);
    findMongoUser({ body: { filter: 'Charlie' }, query: { operator: '!=' } }, users);
    findSafeUser({ query: { id: '456' } }, db);S
    ping({ params: { host: 'example.com' } });

}