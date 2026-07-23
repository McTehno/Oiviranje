export async function safeUserQuery(req, db) {
    const userId = Number(req.query.id);
   return db.query('SELECT * FROM users WHERE id = ?', [userId]);
}

// safe/safe_examples.ts

import { execFile } from 'node:child_process';

export function safeStaticCommand() {
    const command = 'echo backup started';

    return command;
}
// 4. Varno izvajanje fiksnega programa in fiksnih argumentov
export function safeCommandExecution() {
    execFile('echo', ['backup started']);
}
