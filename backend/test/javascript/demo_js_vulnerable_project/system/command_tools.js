// system/command_tools.ts

import { exec, execSync } from 'node:child_process';


// 1. Command Injection pri ukazu ping
export function pingHost(req) {
    const host = req.query.host;

    const command = 'ping ' + host;

    exec(command);
}


// 2. Command Injection pri prikazu datoteke
export function showFile(req) {
    const file = req.query.file;

    const command = 'cat ' + file;

    execSync(command, {stdio: 'inherit'});
}