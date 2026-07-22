const { exec } = require('child_process');

export function ping(req) {
  exec('ping -c 1 ' + req.params.host);
}