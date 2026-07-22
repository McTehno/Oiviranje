import { exec } from 'node:child_process';

export function ping(req: any) {
  const host = req.params.host as string;
  exec(`ping -c 1 ${host}`);
}
