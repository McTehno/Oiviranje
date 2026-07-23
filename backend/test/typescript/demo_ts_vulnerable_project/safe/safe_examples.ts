// safe/safe_examples.ts

import { execFile } from 'node:child_process';


// 1. Varno iskanje uporabnika s parametrizirano SQL-poizvedbo
export async function safeFindUser(req: any, db: any) {
    const userId: string = String(req.query.id ?? '');

    const query = 'SELECT * FROM users WHERE id = ?';

    return db.execute(query, [userId]);
}



// 3. Statičen ukaz brez uporabniškega vnosa
export function safeStaticCommand() {
    const command = 'echo backup started';

    return command;
}


// 4. Varno izvajanje fiksnega programa in fiksnih argumentov
export function safeCommandExecution() {
    execFile('echo', ['backup started']);
}


// 5. Navaden niz ne interpolira spremenljivke
export async function safeSingleQuotedLiteral(req: any, db: any) {
    const userId: string = String(req.query.id ?? '');

    // Enojni narekovaji v TypeScriptu ne izvajajo interpolacije.
    // V poizvedbo se zapiše dobesedno besedilo "$userId".
    const query = 'SELECT * FROM users WHERE id = $userId';

    return db.query(query);
}